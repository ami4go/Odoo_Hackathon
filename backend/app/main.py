from fastapi import FastAPI, HTTPException, Depends, Form, File, UploadFile, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.orm import declarative_base, Session
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Optional, List, Dict
import uuid
import os
from app.database import engine, SessionLocal
from sqlalchemy import or_, and_
from fastapi import Query
from fastapi import status
from fastapi import BackgroundTasks
import google.generativeai as genai
from dotenv import load_dotenv
import os
from sqlalchemy import func  # For average rating
from pydantic import Field
from enum import Enum

# Define enums
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
    OUTERWEAR = "OUTERWEAR"
    SHOES = "SHOES"
    ACCESSORIES = "ACCESSORIES"

class TransactionType(str, Enum):
    EARNED = "EARNED"
    SPENT = "SPENT"
    REFUNDED = "REFUNDED"
    BONUS = "BONUS"

class SwapStatus(str, Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class NotificationType(str, Enum):
    SWAP_REQUEST = "SWAP_REQUEST"
    SWAP_ACCEPTED = "SWAP_ACCEPTED"
    SWAP_REJECTED = "SWAP_REJECTED"
    POINTS_EARNED = "POINTS_EARNED"
    ITEM_APPROVED = "ITEM_APPROVED"
    ITEM_REJECTED = "ITEM_REJECTED"

# Load env vars manually (or use dotenv if needed)
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

Base = declarative_base()
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

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Optional OAuth2 for endpoints that don't require authentication
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)

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

# SQLAlchemy Item model
class Item(Base):
    __tablename__ = "items"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String)
    category_id = Column(String)
    title = Column(String)
    description = Column(String, nullable=True)
    size = Column(String, nullable=True)
    condition = Column(String)
    item_type = Column(String)
    brand = Column(String, nullable=True)
    color = Column(String, nullable=True)
    material = Column(String, nullable=True)
    points_value = Column(Integer, default=0)
    is_available = Column(Boolean, default=True)
    is_approved = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    is_flagged_by_ai = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

# SQLAlchemy Swap model
class Swap(Base):
    __tablename__ = "swaps"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    initiator_id = Column(String)
    recipient_id = Column(String)
    initiator_item_id = Column(String)
    recipient_item_id = Column(String)
    status = Column(String, default="PENDING")
    points_exchanged = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

# SQLAlchemy PointTransaction model
class PointTransaction(Base):
    __tablename__ = "point_transactions"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String)
    transaction_type = Column(String)
    amount = Column(Integer)
    description = Column(String, nullable=True)
    related_item_id = Column(String, nullable=True)
    related_swap_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# SQLAlchemy Notification model
class Notification(Base):
    __tablename__ = "notifications"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String)
    type = Column(String)
    title = Column(String)
    message = Column(String)
    is_read = Column(Boolean, default=False)
    related_item_id = Column(String, nullable=True)
    related_swap_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# SQLAlchemy Rating model
class Rating(Base):
    __tablename__ = "ratings"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    rater_id = Column(String)
    rated_user_id = Column(String)
    swap_id = Column(String, nullable=True)
    rating = Column(Integer)
    comment = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# SQLAlchemy Category model
class Category(Base):
    __tablename__ = "categories"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True)
    description = Column(String, nullable=True)
    icon = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# SQLAlchemy ItemImage model
class ItemImage(Base):
    __tablename__ = "item_images"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    item_id = Column(String)
    image_url = Column(String)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# SQLAlchemy Tag model
class Tag(Base):
    __tablename__ = "tags"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# SQLAlchemy ItemTag model
class ItemTag(Base):
    __tablename__ = "item_tags"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    item_id = Column(String)
    tag_id = Column(String)

# SQLAlchemy ItemViewLog model
class ItemViewLog(Base):
    __tablename__ = "item_view_logs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=True)
    item_id = Column(String)
    viewed_at = Column(DateTime, default=datetime.utcnow)
    user_agent = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)

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

def get_current_user_optional(token: str = Depends(oauth2_scheme_optional), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if not user_id:
            return None
        return db.query(User).filter(User.id == user_id).first()
    except:
        return None

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

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
    if not user.isAdmin:
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
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

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
        # Create Item
        item = Item(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            category_id=category_id,
            size=size,
            condition=condition,
            item_type=item_type,
            brand=brand,
            color=color,
            material=material,
            points_value=points_value,
            user_id=current_user.id,
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
                imageUrl=f"/static/uploads/{filename}",
                isPrimary=(idx == 0)
            )
            db.add(image)

        # Tags
        tag_list = [t.strip() for t in tags.split(",") if t.strip()]
        for tag_name in tag_list:
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(id=str(uuid.uuid4()), name=tag_name)
                db.add(tag)
                db.flush()
            item_tag = ItemTag(id=str(uuid.uuid4()), item_id=item.id, tag_id=tag.id)
            db.add(item_tag)

        db.commit()

        return {"message": "Item created successfully", "item_id": item.id}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create item: {e}")

@app.get("/items/{item_id}", response_model=ItemDetailResponse)
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
    item.viewCount += 1
    db.commit()

    # Optional: Log view
    view_log = ItemViewLog(
        id=str(uuid.uuid4()),
        itemId=item.id,
        userId=current_user.id if current_user else None,
        userAgent=request.headers.get("user-agent") if request else None,
        ipAddress=request.client.host if request else None,
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
        points_value=item.pointsValue,
        is_available=item.isAvailable,
        is_approved=item.isApproved,
        is_featured=item.isFeatured,
        created_at=item.createdAt,
        category={
            "id": item.category.id,
            "name": item.category.name,
        },
        tags=[tag.tag.name for tag in item.itemTags],
        images=[img.imageUrl for img in item.images],
        uploader={
            "id": item.user.id,
            "name": f"{item.user.firstName} {item.user.lastName}",
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
        .filter(PointTransaction.userId == current_user.id)
        .order_by(PointTransaction.createdAt.desc())
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
    query = db.query(Item).filter(Item.isAvailable == True, Item.isApproved == True)

    if category_id:
        query = query.filter(Item.categoryId == category_id)

    if condition:
        query = query.filter(Item.condition == condition.upper())

    if item_type:
        query = query.filter(Item.itemType == item_type.upper())

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
        query = query.order_by(Item.viewCount.desc())
    else:
        query = query.order_by(Item.createdAt.desc())

    items = query.offset(skip).limit(limit).all()

    # For each item, get primary image URL
    result = []
    for item in items:
        primary_img = next((img.imageUrl for img in item.images if img.isPrimary), None)
        result.append(
            ItemListResponse(
                id=item.id,
                title=item.title,
                description=item.description,
                category_id=item.categoryId,
                condition=item.condition.name,
                item_type=item.itemType.name,
                points_value=item.pointsValue,
                is_available=item.isAvailable,
                is_approved=item.isApproved,
                is_featured=item.isFeatured,
                view_count=item.viewCount,
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
        Item.userId == current_user.id,
        Item.isAvailable == True,
        Item.isApproved == True
    ).first()

    if not initiator_item:
        raise HTTPException(status_code=400, detail="Initiator item invalid or unavailable")

    # Fetch recipient's item
    recipient_item = db.query(Item).filter(
        Item.id == swap_request.recipient_item_id,
        Item.isAvailable == True,
        Item.isApproved == True
    ).first()

    if not recipient_item:
        raise HTTPException(status_code=400, detail="Recipient item invalid or unavailable")

    # Cannot swap item with self
    if recipient_item.userId == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot swap with your own item")

    # Check if there is already a pending swap for these items by the user
    existing_swap = db.query(Swap).filter(
        Swap.initiatorId == current_user.id,
        Swap.initiatorItemId == initiator_item.id,
        Swap.recipientItemId == recipient_item.id,
        Swap.status == "PENDING"
    ).first()

    if existing_swap:
        raise HTTPException(status_code=400, detail="A pending swap request already exists for these items")

    # Create new swap record
    new_swap = Swap(
        initiatorId=current_user.id,
        recipientId=recipient_item.userId,
        initiatorItemId=initiator_item.id,
        recipientItemId=recipient_item.id,
        status="PENDING",
        pointsExchanged=0,
        createdAt=datetime.utcnow(),
        updatedAt=datetime.utcnow()
    )

    db.add(new_swap)
    db.commit()
    db.refresh(new_swap)

    return new_swap

@app.put("/swaps/{swap_id}/status")
def update_swap_status(
    swap_id: str,
    status_update: SwapStatusUpdate,
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

    # Only recipient or initiator can update status
    if current_user.id not in [swap.initiatorId, swap.recipientId]:
        raise HTTPException(status_code=403, detail="Not authorized to update this swap")

    # Business logic for status updates:

    # Recipient can ACCEPT or REJECT a PENDING swap
    if new_status == "ACCEPTED":
        if swap.status != "PENDING":
            raise HTTPException(status_code=400, detail="Swap is not pending")
        if current_user.id != swap.recipientId:
            raise HTTPException(status_code=403, detail="Only recipient can accept")
        swap.status = "ACCEPTED"
        # Mark both items unavailable
        initiator_item = db.query(Item).filter(Item.id == swap.initiatorItemId).first()
        recipient_item = db.query(Item).filter(Item.id == swap.recipientItemId).first()
        initiator_item.isAvailable = False
        recipient_item.isAvailable = False

    elif new_status == "REJECTED":
        if swap.status != "PENDING":
            raise HTTPException(status_code=400, detail="Swap is not pending")
        if current_user.id != swap.recipientId:
            raise HTTPException(status_code=403, detail="Only recipient can reject")
        swap.status = "REJECTED"

    elif new_status == "CANCELLED":
        # Either party can cancel if swap not completed
        if swap.status in ["COMPLETED", "CANCELLED", "REJECTED"]:
            raise HTTPException(status_code=400, detail="Swap cannot be cancelled")
        if current_user.id not in [swap.initiatorId, swap.recipientId]:
            raise HTTPException(status_code=403, detail="Not authorized to cancel")
        swap.status = "CANCELLED"

    elif new_status == "COMPLETED":
        # Only initiator can mark swap completed after acceptance
        if swap.status != "ACCEPTED":
            raise HTTPException(status_code=400, detail="Swap not accepted yet")
        if current_user.id != swap.initiatorId:
            raise HTTPException(status_code=403, detail="Only initiator can complete the swap")
        swap.status = "COMPLETED"
        # Transfer item ownership
        initiator_item = db.query(Item).filter(Item.id == swap.initiatorItemId).first()
        recipient_item = db.query(Item).filter(Item.id == swap.recipientItemId).first()
        initiator_item.userId, recipient_item.userId = recipient_item.userId, initiator_item.userId
        # Mark items available after swap completed (optional based on your logic)
        initiator_item.isAvailable = True
        recipient_item.isAvailable = True

    swap.updatedAt = datetime.utcnow()
    db.commit()
    db.refresh(swap)

    return {"message": f"Swap status updated to {swap.status}"}

@app.get("/admin/items/pending")
def get_pending_items(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    items = db.query(Item).filter(Item.isApproved == False).all()
    return items

@app.post("/admin/items/{item_id}/approve")
def approve_item(item_id: str, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item.isApproved = True
    item.isFlaggedByAI = False  # if it was flagged previously
    db.add(AdminAction(
        adminId=admin.id,
        actionType="APPROVE_ITEM",
        targetItemId=item.id
    ))
    db.commit()
    return {"message": f"Item {item_id} approved"}


@app.post("/admin/items/{item_id}/reject")
def reject_item(item_id: str, reason: Optional[str] = None, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.add(AdminAction(
        adminId=admin.id,
        actionType="REJECT_ITEM",
        targetItemId=item.id,
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
        adminId=admin.id,
        actionType="REMOVE_ITEM",
        targetItemId=item.id,
        reason=reason
    ))
    db.delete(item)
    db.commit()
    return {"message": f"Item {item_id} removed"}
@app.get("/admin/items/flagged")
def get_flagged_items(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    items = db.query(Item).filter(Item.isFlaggedByAI == True).all()
    return items

@app.post("/admin/users/{user_id}/ban")
def ban_user(user_id: str, reason: Optional[str] = None, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.isVerified = False  # or add a separate `isBanned` field if needed
    db.add(AdminAction(
        adminId=admin.id,
        actionType="BAN_USER",
        targetUserId=user.id,
        reason=reason
    ))
    db.commit()
    return {"message": f"User {user_id} banned"}

@app.post("/admin/users/{user_id}/unban")
def unban_user(user_id: str, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.isVerified = True
    db.add(AdminAction(
        adminId=admin.id,
        actionType="UNBAN_USER",
        targetUserId=user.id,
    ))
    db.commit()
    return {"message": f"User {user_id} unbanned"}

@app.post("/items/add")
def add_item(item: ItemCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Call Gemini to auto-flag inappropriate listings
    is_flagged = check_if_spam_with_ai(item.title, item.description or "")

    new_item = Item(
        id=str(uuid.uuid4()),
        userId=user.id,
        title=item.title,
        description=item.description,
        categoryId=item.categoryId,
        size=item.size,
        condition=item.condition,
        itemType=item.itemType,
        brand=item.brand,
        color=item.color,
        material=item.material,
        pointsValue=item.pointsValue or 0,
        isFlaggedByAI=is_flagged
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return {"message": "Item added successfully", "flagged_by_ai": is_flagged}
@app.get("/admin/items/flagged")
def get_flagged_items(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if not user.isAdmin:
        raise HTTPException(status_code=403, detail="Not authorized")

    flagged_items = db.query(Item).filter(Item.isFlaggedByAI == True).all()
    return flagged_items


# --- API to create or update rating ---

@app.post("/ratings", response_model=RatingResponse)
def rate_user(rating: RatingCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    existing = db.query(Rating).filter(
        Rating.raterId == user.id,
        Rating.ratedUserId == rating.rated_user_id
    ).first()

    if existing:
        existing.rating = rating.rating
        existing.comment = rating.comment
        existing.swapId = rating.swap_id
    else:
        new_rating = Rating(
            id=str(uuid.uuid4()),
            raterId=user.id,
            ratedUserId=rating.rated_user_id,
            rating=rating.rating,
            comment=rating.comment,
            swapId=rating.swap_id,
            createdAt=datetime.utcnow()
        )
        db.add(new_rating)

    db.commit()
    return existing if existing else new_rating

# --- API to get user ratings with avg and count ---

@app.get("/ratings/user/{user_id}")
def get_user_ratings(user_id: str, db: Session = Depends(get_db)):
    avg_rating = db.query(func.avg(Rating.rating)).filter(Rating.ratedUserId == user_id).scalar()
    total_ratings = db.query(func.count(Rating.id)).filter(Rating.ratedUserId == user_id).scalar()
    recent = db.query(Rating).filter(Rating.ratedUserId == user_id).order_by(Rating.createdAt.desc()).limit(10).all()

    return {
        "average_rating": round(avg_rating or 0, 2),
        "total_ratings": total_ratings,
        "recent_feedback": recent
    }


# 1. Get user's point history
# ----------------------------
@app.get("/points/history", response_model=List[PointsHistoryResponse])
def get_points_history(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    transaction_type: Optional[str] = None
):
    query = db.query(PointTransaction).filter(PointTransaction.userId == user.id)
    if transaction_type:
        query = query.filter(PointTransaction.transactionType == transaction_type.upper())
    return query.order_by(PointTransaction.createdAt.desc()).all()


# ----------------------------------
# 2. Swap & Points Analytics Summary
# ----------------------------------
@app.get("/analytics/swaps")
def get_swap_analytics(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    total_swaps = db.query(Swap).filter(
        (Swap.initiatorId == user.id) | (Swap.recipientId == user.id)
    ).count()

    completed_swaps = db.query(Swap).filter(
        ((Swap.initiatorId == user.id) | (Swap.recipientId == user.id)) &
        (Swap.status == "COMPLETED")
    ).count()

    total_points_earned = db.query(func.sum(PointTransaction.amount)).filter(
        PointTransaction.userId == user.id,
        PointTransaction.transactionType == "EARNED"
    ).scalar() or 0

    total_points_spent = db.query(func.sum(PointTransaction.amount)).filter(
        PointTransaction.userId == user.id,
        PointTransaction.transactionType == "SPENT"
    ).scalar() or 0

    # Optional: Most swapped category
    most_swapped_category = db.query(Category.name, func.count(Item.id)).\
        join(Item, Category.id == Item.categoryId).\
        join(Swap, (Swap.initiatorItemId == Item.id) | (Swap.recipientItemId == Item.id)).\
        filter((Swap.initiatorId == user.id) | (Swap.recipientId == user.id)).\
        group_by(Category.name).\
        order_by(func.count(Item.id).desc()).first()

    return {
        "total_swaps": total_swaps,
        "completed_swaps": completed_swaps,
        "total_points_earned": total_points_earned,
        "total_points_spent": total_points_spent,
        "most_swapped_category": most_swapped_category[0] if most_swapped_category else None
    }







