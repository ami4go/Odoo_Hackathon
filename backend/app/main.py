from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, Session, relationship
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Optional, List, Dict
import uuid
import os
from database import engine, SessionLocal, Base, get_db
from sqlalchemy import or_, and_, case
from fastapi import Query
from fastapi import status
from fastapi import BackgroundTasks
import google.generativeai as genai
from dotenv import load_dotenv
import os
from sqlalchemy import func  # For average rating
from pydantic import Field
from enum import Enum
from fastapi import Form, File, UploadFile, Request
from fastapi.staticfiles import StaticFiles




# Load env vars manually (or use dotenv if needed)
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set specific origin for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

from enum import Enum
class ItemCondition(str, Enum):
    NEW = "new"
    GOOD = "good"
    FAIR = "fair"

class ItemType(str, Enum):
    SWAP = "swap"
    REDEEM = "redeem"


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: Optional[str] = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

@app.post("/items")
async def create_item(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    category_id: str = Form(...),
    size: Optional[str] = Form(None),
    condition: ItemCondition = Form(...),
    item_type: ItemType = Form(...),
    brand: Optional[str] = Form(None),
    color: Optional[str] = Form(None),
    material: Optional[str] = Form(None),
    points_value: Optional[int] = Form(0),
    tags: Optional[str] = Form(""),
    images: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Check if spam using AI
        is_flagged = check_if_spam_with_ai(title, description or "")
        
        # Create Item
        item = Item(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            category_id=category_id,
            size=size,
            condition=condition.value,
            item_type=item_type.value,
            brand=brand,
            color=color,
            material=material,
            points_value=points_value,
            user_id=current_user.id,
            is_flagged_by_ai=is_flagged
        )
        db.add(item)
        db.commit()
        db.refresh(item)

        # Save Images
        for idx, img in enumerate(images):
            img_bytes = await img.read()
            filename = f"{uuid.uuid4()}.jpg"
            filepath = f"static/uploads/{filename}"
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, "wb") as f:
                f.write(img_bytes)

            image = ItemImage(
                id=str(uuid.uuid4()),
                item_id=item.id,
                image_url=f"/static/uploads/{filename}",
                is_primary=(idx == 0)
            )
            db.add(image)

        # Tags
        tag_list = [t.strip() for t in (tags or "").split(",") if t.strip()]
        for tag_name in tag_list:
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(id=str(uuid.uuid4()), name=tag_name)
                db.add(tag)
                db.flush()
            item_tag = ItemTag(id=str(uuid.uuid4()), item_id=item.id, tag_id=tag.id)
            db.add(item_tag)

        db.commit()

        return {"message": "Item created successfully", "item_id": item.id, "flagged_by_ai": is_flagged}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create item: {e}")

@app.get("/items/{item_id}", response_model=ItemDetailResponse)


# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# SQLAlchemy User model
class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    is_admin = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    points_balance = Column(Integer, default=0)

# Missing Database Models
class Category(Base):
    __tablename__ = "categories"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True)
    description = Column(String, nullable=True)

class Item(Base):
    __tablename__ = "items"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    category_id = Column(String, ForeignKey("categories.id"))
    size = Column(String, nullable=True)
    condition = Column(String, nullable=False)  # NEW, LIKE_NEW, GOOD, FAIR, POOR
    item_type = Column(String, nullable=False)  # TOP, BOTTOM, DRESS, SHOES, ACCESSORY
    brand = Column(String, nullable=True)
    color = Column(String, nullable=True)
    material = Column(String, nullable=True)
    points_value = Column(Integer, default=0)
    user_id = Column(String, ForeignKey("users.id"))
    is_available = Column(Boolean, default=True)
    is_approved = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    is_flagged_by_ai = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    category = relationship("Category", backref="items")
    user = relationship("User", backref="items")
    images = relationship("ItemImage", backref="item")
    item_tags = relationship("ItemTag", backref="item")

class ItemImage(Base):
    __tablename__ = "item_images"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    item_id = Column(String, ForeignKey("items.id"))
    image_url = Column(String, nullable=False)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Tag(Base):
    __tablename__ = "tags"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True)

class ItemTag(Base):
    __tablename__ = "item_tags"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    item_id = Column(String, ForeignKey("items.id"))
    tag_id = Column(String, ForeignKey("tags.id"))
    
    # Relationships
    tag = relationship("Tag", backref="item_tags")

class Swap(Base):
    __tablename__ = "swaps"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    initiator_id = Column(String, ForeignKey("users.id"))
    recipient_id = Column(String, ForeignKey("users.id"))
    initiator_item_id = Column(String, ForeignKey("items.id"))
    recipient_item_id = Column(String, ForeignKey("items.id"))
    status = Column(String, default="PENDING")  # PENDING, ACCEPTED, REJECTED, CANCELLED, COMPLETED
    points_exchanged = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    initiator = relationship("User", foreign_keys=[initiator_id], backref="initiated_swaps")
    recipient = relationship("User", foreign_keys=[recipient_id], backref="received_swaps")
    initiator_item = relationship("Item", foreign_keys=[initiator_item_id])
    recipient_item = relationship("Item", foreign_keys=[recipient_item_id])

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    type = Column(String, nullable=False)  # SWAP_REQUEST, SWAP_ACCEPTED, SWAP_REJECTED, etc.
    title = Column(String, nullable=False)
    message = Column(String, nullable=False)
    related_swap_id = Column(String, ForeignKey("swaps.id"), nullable=True)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", backref="notifications")
    related_swap = relationship("Swap", backref="notifications")

class PointTransaction(Base):
    __tablename__ = "point_transactions"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    transaction_type = Column(String, nullable=False)  # EARNED, SPENT, BONUS
    amount = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    related_item_id = Column(String, ForeignKey("items.id"), nullable=True)
    related_swap_id = Column(String, ForeignKey("swaps.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", backref="point_transactions")

class Rating(Base):
    __tablename__ = "ratings"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    rater_id = Column(String, ForeignKey("users.id"))
    rated_user_id = Column(String, ForeignKey("users.id"))
    rating = Column(Integer, nullable=False)  # 1-5 stars
    comment = Column(String, nullable=True)
    swap_id = Column(String, ForeignKey("swaps.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    rater = relationship("User", foreign_keys=[rater_id], backref="ratings_given")
    rated_user = relationship("User", foreign_keys=[rated_user_id], backref="ratings_received")

class ItemViewLog(Base):
    __tablename__ = "item_view_logs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    item_id = Column(String, ForeignKey("items.id"))
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    user_agent = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    item = relationship("Item", backref="view_logs")
    user = relationship("User", backref="view_logs")

class AdminAction(Base):
    __tablename__ = "admin_actions"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    admin_id = Column(String, ForeignKey("users.id"))
    action_type = Column(String, nullable=False)  # APPROVE_ITEM, REJECT_ITEM, BAN_USER, etc.
    target_item_id = Column(String, ForeignKey("items.id"), nullable=True)
    target_user_id = Column(String, ForeignKey("users.id"), nullable=True)
    reason = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    admin = relationship("User", foreign_keys=[admin_id], backref="admin_actions")
    target_item = relationship("Item", foreign_keys=[target_item_id])
    target_user = relationship("User", foreign_keys=[target_user_id])

# Enums for Item conditions and types
class ItemCondition(str, Enum):
    NEW = "NEW"
    LIKE_NEW = "LIKE_NEW"
    GOOD = "GOOD"
    FAIR = "FAIR"
    POOR = "POOR"

class ItemType(str, Enum):
    TOP = "TOP"
    BOTTOM = "BOTTOM"
    DRESS = "DRESS"
    SHOES = "SHOES"
    ACCESSORY = "ACCESSORY"


# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic Schemas
class UserCreate(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str

class UserOut(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
class ItemCreate(BaseModel):
    title: str
    description: Optional[str]
    category_id: str
    size: Optional[str]
    condition: ItemCondition
    item_type: ItemType
    brand: Optional[str]
    color: Optional[str]
    material: Optional[str]
    tags: Optional[List[str]] = []
    points_value: Optional[int] = 0

class ItemDetailResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    size: Optional[str]
    condition: ItemCondition
    item_type: ItemType
    brand: Optional[str]
    color: Optional[str]
    material: Optional[str]
    points_value: int
    is_available: bool
    is_approved: bool
    is_featured: bool
    created_at: datetime
    category: Dict[str, str]
    tags: List[str]
    images: List[str]
    uploader: Dict[str, str]

    class Config:
        from_attributes = True

class PointTransactionResponse(BaseModel):
    id: str
    transaction_type: str
    amount: int
    description: Optional[str]
    related_item_id: Optional[str]
    related_swap_id: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class ItemListResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    category_id: str
    condition: str
    item_type: str
    points_value: int
    is_available: bool
    is_approved: bool
    is_featured: bool
    view_count: int
    primary_image_url: Optional[str]

    class Config:
        from_attributes = True

class SwapRequest(BaseModel):
    initiator_item_id: str
    recipient_item_id: str


class SwapResponse(BaseModel):
    id: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class SwapStatusUpdate(BaseModel):
    status: str  # Allowed values: ACCEPTED, REJECTED, CANCELLED, COMPLETED

class RatingCreate(BaseModel):
    rated_user_id: str
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None
    swap_id: Optional[str] = None

class RatingResponse(BaseModel):
    id: str
    rater_id: str
    rated_user_id: str
    rating: int
    comment: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class PointsHistoryResponse(BaseModel):
    id: str
    transaction_type: str
    amount: int
    description: Optional[str]
    related_item_id: Optional[str]
    related_swap_id: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True








# Utility functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def get_password_hash(password):
    return pwd_context.hash(password)

oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

def get_current_user_optional(token: str = Depends(oauth2_scheme_optional), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: Optional[str] = payload.get("sub")
        if not user_id:
            return None
        return db.query(User).filter(User.id == user_id).first()
    except:
        return None
def create_notification(
    db: Session,
    user_id: str,
    notif_type: str,
    title: str,
    message: str,
    related_swap_id: str,
):
    notif = Notification(
        userId=user_id,
        type=notif_type,
        title=title,
        message=message,
        relatedSwapId=related_swap_id,
        isRead=False,
        createdAt=datetime.utcnow(),
    )
    db.add(notif)
    db.commit()

def create_point_transaction(
    db: Session,
    user_id: str,
    transaction_type: str,
    amount: int,
    description: str,
    related_swap_id: str,
):
    pt = PointTransaction(
        userId=user_id,
        transactionType=transaction_type,
        amount=amount,
        description=description,
        relatedSwapId=related_swap_id,
        createdAt=datetime.utcnow(),
    )
    db.add(pt)
    db.commit()

@app.put("/swaps/{swap_id}/status")
def update_swap_status(
    swap_id: str,
    status_update: SwapStatusUpdate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    allowed_statuses = {"ACCEPTED", "REJECTED", "CANCELLED", "COMPLETED"}
    new_status = status_update.status.upper()

    if new_status not in allowed_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")

    swap = db.query(Swap).filter(Swap.id == swap_id).first()
    if not swap:
        raise HTTPException(status_code=404, detail="Swap not found")

    if current_user.id not in [swap.initiatorId, swap.recipientId]:
        raise HTTPException(status_code=403, detail="Not authorized to update this swap")

    # Fetch items for points & ownership update
    initiator_item = db.query(Item).filter(Item.id == swap.initiatorItemId).first()
    recipient_item = db.query(Item).filter(Item.id == swap.recipientItemId).first()

    if new_status == "ACCEPTED":
        if swap.status != "PENDING":
            raise HTTPException(status_code=400, detail="Swap is not pending")
        if current_user.id != swap.recipientId:
            raise HTTPException(status_code=403, detail="Only recipient can accept")
        swap.status = "ACCEPTED"
        initiator_item.isAvailable = False
        recipient_item.isAvailable = False

        # Notify initiator that recipient accepted swap
        background_tasks.add_task(
            create_notification,
            db=db,
            user_id=swap.initiatorId,
            notif_type="SWAP_ACCEPTED",
            title="Swap Request Accepted",
            message=f"Your swap request {swap.id} has been accepted.",
            related_swap_id=swap.id,
        )

    elif new_status == "REJECTED":
        if swap.status != "PENDING":
            raise HTTPException(status_code=400, detail="Swap is not pending")
        if current_user.id != swap.recipientId:
            raise HTTPException(status_code=403, detail="Only recipient can reject")
        swap.status = "REJECTED"

        # Notify initiator about rejection
        background_tasks.add_task(
            create_notification,
            db=db,
            user_id=swap.initiatorId,
            notif_type="SWAP_REJECTED",
            title="Swap Request Rejected",
            message=f"Your swap request {swap.id} has been rejected.",
            related_swap_id=swap.id,
        )

    elif new_status == "CANCELLED":
        if swap.status in ["COMPLETED", "CANCELLED", "REJECTED"]:
            raise HTTPException(status_code=400, detail="Swap cannot be cancelled")
        swap.status = "CANCELLED"

        # Notify other party
        other_user_id = swap.recipientId if current_user.id == swap.initiatorId else swap.initiatorId
        background_tasks.add_task(
            create_notification,
            db=db,
            user_id=other_user_id,
            notif_type="SWAP_REJECTED",  # Use same type for cancellation notification
            title="Swap Cancelled",
            message=f"Swap {swap.id} has been cancelled by the other party.",
            related_swap_id=swap.id,
        )

    elif new_status == "COMPLETED":
        if swap.status != "ACCEPTED":
            raise HTTPException(status_code=400, detail="Swap not accepted yet")
        if current_user.id != swap.initiatorId:
            raise HTTPException(status_code=403, detail="Only initiator can complete the swap")
        swap.status = "COMPLETED"

        # Transfer ownership
        initiator_item.userId, recipient_item.userId = recipient_item.userId, initiator_item.userId
        initiator_item.isAvailable = True
        recipient_item.isAvailable = True

        # Handle points exchange (example: initiator pays pointsExchanged)
        if swap.pointsExchanged > 0:
            # Deduct points from initiator
            initiator = db.query(User).filter(User.id == swap.initiatorId).first()
            recipient = db.query(User).filter(User.id == swap.recipientId).first()

            initiator.pointsBalance -= swap.pointsExchanged
            recipient.pointsBalance += swap.pointsExchanged

            # Create point transactions
            background_tasks.add_task(
                create_point_transaction,
                db=db,
                user_id=initiator.id,
                transaction_type="SPENT",
                amount=swap.pointsExchanged,
                description=f"Points spent on swap {swap.id}",
                related_swap_id=swap.id,
            )
            background_tasks.add_task(
                create_point_transaction,
                db=db,
                user_id=recipient.id,
                transaction_type="EARNED",
                amount=swap.pointsExchanged,
                description=f"Points earned from swap {swap.id}",
                related_swap_id=swap.id,
            )
        
        # Notify both parties about completion
        for user_id in [swap.initiatorId, swap.recipientId]:
            background_tasks.add_task(
                create_notification,
                db=db,
                user_id=user_id,
                notif_type="SWAP_ACCEPTED",
                title="Swap Completed",
                message=f"Swap {swap.id} has been successfully completed.",
                related_swap_id=swap.id,
            )

    swap.updatedAt = datetime.utcnow()
    db.commit()
    db.refresh(swap)

    return {"message": f"Swap status updated to {swap.status}"}


def require_admin(user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return user
def spam_detection_prompt(title: str, description: str) -> str:
    return f"""
You are an AI moderator for a clothing swapping platform.

Evaluate the following item listing based on its **description and title**.

Flag the item if it:
- Contains vulgar, inappropriate, or offensive language.
- Mentions spammy phrases (e.g. "buy now", "limited offer", "visit xyz site").
- Is irrelevant to clothing or wearable accessories.
- Contains gibberish, repetitive nonsense, or looks auto-generated.
- Appears to be a duplicate of previously submitted items (assume context if needed).
- Promotes ads, services, or anything beyond personal clothing swaps.
- Contains unsafe or illegal content.

Reply only with one word: **FLAG** or **OK**

---
Title: {title}
Description: {description}
"""
def check_if_spam_with_ai(title: str, description: str) -> bool:
    prompt = spam_detection_prompt(title, description)
    model = genai.GenerativeModel("gemini-pro")
    try:
        response = model.generate_content(prompt)
        decision = response.text.strip().upper()
        return decision == "FLAG"
    except Exception as e:
        print(f"Gemini error: {e}")
        return False  # Fail-safe: allow item if AI fails





@app.get("/me", response_model=UserOut)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user


# Auth Routes
@app.post("/signup", response_model=UserOut)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user.email,
        password_hash=get_password_hash(user.password),
        first_name=user.first_name,
        last_name=user.last_name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.passwordHash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
def get_item_detail(
    item_id: str,
    db: Session = Depends(get_db),
    request: Request = None,
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    item = (
        db.query(Item)
        .filter(Item.id == item_id, Item.isApproved == True)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Item not found or not approved")

    # Increment view count
    item.view_count += 1
    db.commit()

    # Optional: Log view
    view_log = ItemViewLog(
        id=str(uuid.uuid4()),
        item_id=item.id,
        user_id=current_user.id if current_user else None,
        user_agent=request.headers.get("user-agent") if request else None,
        ip_address=request.client.host if request else None,
    )
    db.add(view_log)
    db.commit()

    return ItemDetailResponse(
        id=item.id,
        title=item.title,
        description=item.description,
        size=item.size,
        condition=item.condition,
        item_type=item.item_type,
        brand=item.brand,
        color=item.color,
        material=item.material,
        points_value=item.points_value,
        is_available=item.is_available,
        is_approved=item.is_approved,
        is_featured=item.is_featured,
        created_at=item.created_at,
        category={
            "id": item.category.id,
            "name": item.category.name,
        },
        tags=[tag.name for tag in item.item_tags],
        images=[img.image_url for img in item.item_images],
        uploader={
            "id": item.user.id,
            "name": f"{item.user.first_name} {item.user.last_name}",
        }
    )

@app.get("/users/me/points", response_model=List[PointTransactionResponse])
def get_points_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 20,
):
    transactions = (
        db.query(PointTransaction)
        .filter(PointTransaction.user_id == current_user.id)
        .order_by(PointTransaction.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return transactions



@app.get("/items", response_model=List[ItemListResponse])
def browse_items(
    category_id: Optional[str] = None,
    tags: Optional[str] = Query(None, description="Comma separated tag names"),
    condition: Optional[str] = None,
    item_type: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: Optional[str] = "newest",
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    query = db.query(Item).filter(Item.is_available == True, Item.is_approved == True)

    if category_id:
        query = query.filter(Item.category_id == category_id)

    if condition:
        query = query.filter(Item.condition == condition.upper())

    if item_type:
        query = query.filter(Item.item_type == item_type.upper())

    if search:
        search_pattern = f"%{search.lower()}%"
        query = query.filter(
            or_(
                Item.title.ilike(search_pattern),
                Item.description.ilike(search_pattern)
            )
        )
    
    if tags:
        tag_list = [tag.strip().lower() for tag in tags.split(",")]
        query = query.join(ItemTag).join(Tag).filter(Tag.name.in_(tag_list))

    if sort_by == "popular":
        query = query.order_by(Item.view_count.desc())
    else:
        query = query.order_by(Item.created_at.desc())

    items = query.offset(skip).limit(limit).all()

    # For each item, get primary image URL
    result = []
    for item in items:
        primary_img = next((img.image_url for img in item.item_images if img.is_primary), None)
        result.append(
            ItemListResponse(
                id=item.id,
                title=item.title,
                description=item.description,
                category_id=item.category_id,
                condition=item.condition.name,
                item_type=item.item_type.name,
                points_value=item.points_value,
                is_available=item.is_available,
                is_approved=item.is_approved,
                is_featured=item.is_featured,
                view_count=item.view_count,
                primary_image_url=primary_img,
            )
        )
    return result



@app.post("/swaps/request", response_model=SwapResponse)
def request_swap(
    swap_request: SwapRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Fetch initiator's item - must belong to current user
    initiator_item = db.query(Item).filter(
        Item.id == swap_request.initiator_item_id,
        Item.user_id == current_user.id,
        Item.is_available == True,
        Item.is_approved == True
    ).first()

    if not initiator_item:
        raise HTTPException(status_code=400, detail="Initiator item invalid or unavailable")

    # Fetch recipient's item
    recipient_item = db.query(Item).filter(
        Item.id == swap_request.recipient_item_id,
        Item.is_available == True,
        Item.is_approved == True
    ).first()

    if not recipient_item:
        raise HTTPException(status_code=400, detail="Recipient item invalid or unavailable")

    # Cannot swap item with self
    if recipient_item.user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot swap with your own item")

    # Check if there is already a pending swap for these items by the user
    existing_swap = db.query(Swap).filter(
        Swap.initiator_id == current_user.id,
        Swap.initiator_item_id == initiator_item.id,
        Swap.recipient_item_id == recipient_item.id,
        Swap.status == "PENDING"
    ).first()

    if existing_swap:
        raise HTTPException(status_code=400, detail="A pending swap request already exists for these items")

    # Create new swap record
    new_swap = Swap(
        initiator_id=current_user.id,
        recipient_id=recipient_item.user_id,
        initiator_item_id=initiator_item.id,
        recipient_item_id=recipient_item.id,
        status="PENDING",
        points_exchanged=0,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(new_swap)
    db.commit()
    db.refresh(new_swap)

    return new_swap



@app.get("/admin/items/pending")
def get_pending_items(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    items = db.query(Item).filter(Item.is_approved == False).all()
    return items

@app.post("/admin/items/{item_id}/approve")
def approve_item(item_id: str, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item.is_approved = True
    item.is_flagged_by_ai = False  # if it was flagged previously
    db.add(AdminAction(
        admin_id=admin.id,
        action_type="APPROVE_ITEM",
        target_item_id=item.id
    ))
    db.commit()
    return {"message": f"Item {item_id} approved"}


@app.post("/admin/items/{item_id}/reject")
def reject_item(item_id: str, reason: Optional[str] = None, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.add(AdminAction(
        admin_id=admin.id,
        action_type="REJECT_ITEM",
        target_item_id=item.id,
        reason=reason
    ))
    db.delete(item)
    db.commit()
    return {"message": f"Item {item_id} rejected and removed"}

@app.delete("/admin/items/{item_id}/remove")
def remove_item(item_id: str, reason: Optional[str] = None, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.add(AdminAction(
        admin_id=admin.id,
        action_type="REMOVE_ITEM",
        target_item_id=item.id,
        reason=reason
    ))
    db.delete(item)
    db.commit()
    return {"message": f"Item {item_id} removed"}
@app.get("/admin/items/flagged")
def get_flagged_items(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    items = db.query(Item).filter(Item.is_flagged_by_ai == True).all()
    return items

@app.post("/admin/users/{user_id}/ban")
def ban_user(user_id: str, reason: Optional[str] = None, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_verified = False  # or add a separate `isBanned` field if needed
    db.add(AdminAction(
        admin_id=admin.id,
        action_type="BAN_USER",
        target_user_id=user.id,
        reason=reason
    ))
    db.commit()
    return {"message": f"User {user_id} banned"}

@app.post("/admin/users/{user_id}/unban")
def unban_user(user_id: str, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_verified = True
    db.add(AdminAction(
        admin_id=admin.id,
        action_type="UNBAN_USER",
        target_user_id=user.id,
    ))
    db.commit()
    return {"message": f"User {user_id} unbanned"}

@app.post("/items/add")
def add_item(item: ItemCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Call Gemini to auto-flag inappropriate listings
    is_flagged = check_if_spam_with_ai(item.title, item.description or "")

    new_item = Item(
        id=str(uuid.uuid4()),
        user_id=user.id,
        title=item.title,
        description=item.description,
        category_id=item.category_id,
        size=item.size,
        condition=item.condition,
        item_type=item.item_type,
        brand=item.brand,
        color=item.color,
        material=item.material,
        points_value=item.points_value or 0,
        is_flagged_by_ai=is_flagged
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return {"message": "Item added successfully", "flagged_by_ai": is_flagged}



# --- API to create or update rating ---

@app.post("/ratings", response_model=RatingResponse)
def rate_user(rating: RatingCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    existing = db.query(Rating).filter(
        Rating.rater_id == user.id,
        Rating.rated_user_id == rating.rated_user_id
    ).first()

    if existing:
        existing.rating = rating.rating
        existing.comment = rating.comment
        existing.swap_id = rating.swap_id
    else:
        new_rating = Rating(
            id=str(uuid.uuid4()),
            rater_id=user.id,
            rated_user_id=rating.rated_user_id,
            rating=rating.rating,
            comment=rating.comment,
            swap_id=rating.swap_id,
            created_at=datetime.utcnow()
        )
        db.add(new_rating)

    db.commit()
    return existing if existing else new_rating

# --- API to get user ratings with avg and count ---

@app.get("/ratings/user/{user_id}")
def get_user_ratings(user_id: str, db: Session = Depends(get_db)):
    avg_rating = db.query(func.avg(Rating.rating)).filter(Rating.rated_user_id == user_id).scalar()
    total_ratings = db.query(func.count(Rating.id)).filter(Rating.rated_user_id == user_id).scalar()
    recent = db.query(Rating).filter(Rating.rated_user_id == user_id).order_by(Rating.created_at.desc()).limit(10).all()

    return {
        "average_rating": round(avg_rating or 0, 2),
        "total_ratings": total_ratings,
        "recent_feedback": recent
    }


# 1. Get user's point history
# ----------------------------



# ----------------------------------
# 2. Swap & Points Analytics Summary
# ----------------------------------
@app.get("/analytics/swaps")
def get_swap_analytics(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    total_swaps = db.query(Swap).filter(
        (Swap.initiator_id == user.id) | (Swap.recipient_id == user.id)
    ).count()

    completed_swaps = db.query(Swap).filter(
        ((Swap.initiator_id == user.id) | (Swap.recipient_id == user.id)) &
        (Swap.status == "COMPLETED")
    ).count()

    total_points_earned = db.query(func.sum(PointTransaction.amount)).filter(
        PointTransaction.user_id == user.id,
        PointTransaction.transaction_type == "EARNED"
    ).scalar() or 0

    total_points_spent = db.query(func.sum(PointTransaction.amount)).filter(
        PointTransaction.user_id == user.id,
        PointTransaction.transaction_type == "SPENT"
    ).scalar() or 0

    # Optional: Most swapped category
    most_swapped_category = db.query(Category.name, func.count(Item.id)).\
        join(Item, Category.id == Item.category_id).\
        join(Swap, (Swap.initiator_item_id == Item.id) | (Swap.recipient_item_id == Item.id)).\
        filter((Swap.initiator_id == user.id) | (Swap.recipient_id == user.id)).\
        group_by(Category.name).\
        order_by(func.count(Item.id).desc()).first()

    return {
        "total_swaps": total_swaps,
        "completed_swaps": completed_swaps,
        "total_points_earned": total_points_earned,
        "total_points_spent": total_points_spent,
        "most_swapped_category": most_swapped_category[0] if most_swapped_category else None
    }


#Notifications API – Fetch Notifications
class NotificationResponse(BaseModel):
    id: str
    type: str
    title: str
    message: str
    related_swap_id: Optional[str]
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
@app.get("/notifications", response_model=List[NotificationResponse])
def get_my_notifications(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    notifs = (
        db.query(Notification)
        .filter(Notification.user_id == user.id)
        .order_by(Notification.created_at.desc())
        .all()
    )
    return notifs

# Missing API Endpoints

@app.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    """Get all available categories"""
    categories = db.query(Category).all()
    return categories

@app.get("/users/me/items")
def get_my_items(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    status: Optional[str] = None  # "active", "pending", "sold"
):
    """Get current user's uploaded items"""
    query = db.query(Item).filter(Item.user_id == current_user.id)
    
    if status == "active":
        query = query.filter(Item.is_available == True, Item.is_approved == True)
    elif status == "pending":
        query = query.filter(Item.is_approved == False)
    elif status == "sold":
        query = query.filter(Item.is_available == False)
    
    items = query.order_by(Item.created_at.desc()).all()
    return items

@app.get("/users/me/swaps")
def get_my_swaps(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    status: Optional[str] = None  # "pending", "active", "completed", "cancelled"
):
    """Get current user's swap history"""
    query = db.query(Swap).filter(
        (Swap.initiator_id == current_user.id) | (Swap.recipient_id == current_user.id)
    )
    
    if status:
        query = query.filter(Swap.status == status.upper())
    
    swaps = query.order_by(Swap.created_at.desc()).all()
    return swaps

@app.get("/users/me/dashboard")
def get_user_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user dashboard data"""
    # Get user's items count
    total_items = db.query(Item).filter(Item.user_id == current_user.id).count()
    active_items = db.query(Item).filter(
        Item.user_id == current_user.id,
        Item.is_available == True,
        Item.is_approved == True
    ).count()
    pending_items = db.query(Item).filter(
        Item.user_id == current_user.id,
        Item.is_approved == False
    ).count()
    
    # Get swap statistics
    total_swaps = db.query(Swap).filter(
        (Swap.initiator_id == current_user.id) | (Swap.recipient_id == current_user.id)
    ).count()
    
    completed_swaps = db.query(Swap).filter(
        ((Swap.initiator_id == current_user.id) | (Swap.recipient_id == current_user.id)) &
        (Swap.status == "COMPLETED")
    ).count()
    
    # Get recent activity
    recent_items = db.query(Item).filter(Item.user_id == current_user.id).order_by(Item.created_at.desc()).limit(5).all()
    recent_swaps = db.query(Swap).filter(
        (Swap.initiator_id == current_user.id) | (Swap.recipient_id == current_user.id)
    ).order_by(Swap.created_at.desc()).limit(5).all()
    
    return {
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "first_name": current_user.first_name,
            "last_name": current_user.last_name,
            "points_balance": current_user.points_balance,
            "is_admin": current_user.is_admin
        },
        "stats": {
            "total_items": total_items,
            "active_items": active_items,
            "pending_items": pending_items,
            "total_swaps": total_swaps,
            "completed_swaps": completed_swaps
        },
        "recent_items": recent_items,
        "recent_swaps": recent_swaps
    }

@app.get("/items/featured")
def get_featured_items(
    db: Session = Depends(get_db),
    limit: int = 10
):
    """Get featured items for landing page"""
    featured_items = db.query(Item).filter(
        Item.is_featured == True,
        Item.is_approved == True,
        Item.is_available == True
    ).order_by(Item.view_count.desc()).limit(limit).all()
    
    return featured_items

@app.post("/notifications/{notification_id}/read")
def mark_notification_read(
    notification_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark a notification as read"""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.is_read = True
    db.commit()
    return {"message": "Notification marked as read"}

@app.post("/notifications/read-all")
def mark_all_notifications_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark all notifications as read"""
    db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    ).update({"is_read": True})
    db.commit()
    return {"message": "All notifications marked as read"}

@app.get("/admin/dashboard")
def get_admin_dashboard(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Get admin dashboard statistics"""
    total_users = db.query(User).count()
    total_items = db.query(Item).count()
    pending_items = db.query(Item).filter(Item.is_approved == False).count()
    flagged_items = db.query(Item).filter(Item.is_flagged_by_ai == True).count()
    total_swaps = db.query(Swap).count()
    completed_swaps = db.query(Swap).filter(Swap.status == "COMPLETED").count()
    
    # Recent admin actions
    recent_actions = db.query(AdminAction).order_by(AdminAction.created_at.desc()).limit(10).all()
    
    return {
        "stats": {
            "total_users": total_users,
            "total_items": total_items,
            "pending_items": pending_items,
            "flagged_items": flagged_items,
            "total_swaps": total_swaps,
            "completed_swaps": completed_swaps
        },
        "recent_actions": recent_actions
    }

@app.get("/search/recommendations")
def get_item_recommendations(
    user_id: Optional[str] = None,
    category_id: Optional[str] = None,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Get personalized item recommendations"""
    query = db.query(Item).filter(
        Item.is_approved == True,
        Item.is_available == True
    )
    
    if category_id:
        query = query.filter(Item.category_id == category_id)
    
    # If user is logged in, prioritize items from categories they've interacted with
    if current_user:
        # Get user's swap history to find preferred categories
        user_swaps = db.query(Swap).filter(
            (Swap.initiator_id == current_user.id) | (Swap.recipient_id == current_user.id)
        ).all()
        
        # Extract item IDs from swaps
        item_ids = []
        for swap in user_swaps:
            item_ids.extend([swap.initiator_item_id, swap.recipient_item_id])
        
        if item_ids:
            # Get categories from user's swap history
            preferred_categories = db.query(Item.category_id).filter(
                Item.id.in_(item_ids)
            ).distinct().all()
            
            category_ids = [cat[0] for cat in preferred_categories]
            if category_ids:
                # Order by preferred categories first
                query = query.order_by(
                    case(
                        (Item.category_id.in_(category_ids), 0),
                        else_=1
                    ),
                    Item.view_count.desc()
                )
    
    # Fallback to most viewed items
    if not current_user or not user_swaps:
        query = query.order_by(Item.view_count.desc())
    
    recommendations = query.limit(limit).all()
    return recommendations

@app.get("/swaps/me")
def get_user_swaps(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    swaps = db.query(Swap).filter(
        (Swap.initiatorId == current_user.id) | 
        (Swap.recipientId == current_user.id)
    ).order_by(Swap.createdAt.desc()).all()
    return swaps


@app.post("/items/{item_id}/redeem")
def redeem_item_with_points(
    item_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Redeem an item using points"""
    item = db.query(Item).filter(
        Item.id == item_id,
        Item.is_approved == True,
        Item.is_available == True
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if item.user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot redeem your own item")
    
    if current_user.points_balance < item.points_value:
        raise HTTPException(status_code=400, detail="Insufficient points")
    
    # Create point transaction
    point_transaction = PointTransaction(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        transaction_type="SPENT",
        amount=item.points_value,
        description=f"Redeemed item: {item.title}",
        related_item_id=item.id
    )
    
    # Transfer points to item owner
    item_owner = db.query(User).filter(User.id == item.user_id).first()
    item_owner.points_balance += item.points_value
    current_user.points_balance -= item.points_value
    
    # Mark item as unavailable
    item.is_available = False
    
    # Create notification for item owner
    notification = Notification(
        id=str(uuid.uuid4()),
        user_id=item.user_id,
        type="ITEM_REDEEMED",
        title="Item Redeemed",
        message=f"Your item '{item.title}' has been redeemed for {item.points_value} points",
        related_swap_id=None
    )
    
    db.add(point_transaction)
    db.add(notification)
    db.commit()
    
    return {"message": "Item redeemed successfully"}

@app.get("/tags/popular")
def get_popular_tags(
    db: Session = Depends(get_db),
    limit: int = 20
):
    """Get most popular tags"""
    popular_tags = db.query(Tag.name, func.count(ItemTag.id).label('count')).\
        join(ItemTag, Tag.id == ItemTag.tag_id).\
        group_by(Tag.name).\
        order_by(func.count(ItemTag.id).desc()).\
        limit(limit).all()
    
    return [{"name": tag.name, "count": tag.count} for tag in popular_tags]

@app.get("/users/{user_id}/profile")
def get_user_profile(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get public user profile"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get user's items
    user_items = db.query(Item).filter(
        Item.user_id == user_id,
        Item.is_approved == True,
        Item.is_available == True
    ).all()
    
    # Get user's rating
    avg_rating = db.query(func.avg(Rating.rating)).filter(Rating.rated_user_id == user_id).scalar()
    total_ratings = db.query(func.count(Rating.id)).filter(Rating.rated_user_id == user_id).scalar()
    
    return {
        "user": {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "created_at": user.created_at
        },
        "stats": {
            "total_items": len(user_items),
            "average_rating": round(avg_rating or 0, 2),
            "total_ratings": total_ratings
        },
        "items": user_items
    }
    from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
import json
import os

# Load environment variables
load_dotenv()

# Load chatbot model
llm = ChatGroq(
    model="gemma2-9b-it", 
    temperature=0.7,
    api_key=os.getenv("GROQ_API_KEY")
)

# Load knowledge base
with open("rewear_chunks.json", "r") as f:
    rewear_chunks = json.load(f)

knowledge_base = "\n\n".join(
    f"{chunk['title']}\n{chunk['content']}" for chunk in rewear_chunks
)

# Define system prompt
system_prompt = f"""
You are ReWearBot, a helpful assistant for a platform called ReWear.

Instructions:
- You help users understand and use the ReWear platform.
- ReWear is a community-driven platform for swapping unused clothes via direct exchange or a point-based system.
- You should respond clearly, concisely, and with step-by-step guidance when needed.
- Always answer based on the knowledge base provided below.
- If a user asks "How do I start swapping?" or "How do I earn points?", explain the correct process based on the APIs and user flow.
- You should avoid hallucinating any answers outside this knowledge base.
- Keep your tone friendly but professional.
- If asked a question outside the scope of ReWear (e.g., banking, movies), respond: “I specialize in ReWear-related questions. Please ask me something about the platform.”

Knowledge Base:
{knowledge_base}
"""

# Pydantic model for incoming and outgoing messages
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

# Create FastAPI app if not already present
app = FastAPI()

# ReWearBot API Endpoint
@app.post("/chatbot/ask", response_model=ChatResponse)
def ask_rewear_bot(payload: ChatRequest):
    try:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=payload.message)
        ]
        ai_response = llm.invoke(messages)
        return {"response": ai_response.content.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot error: {e}")

