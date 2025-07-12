from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import json

load_dotenv()

llm = ChatGroq(model="gemma2-9b-it", temperature=0.7, api_key=os.getenv("GROQ_API_KEY"))

with open("rewear_chunks.json", "r") as f:
    rewear_chunks = json.load(f)

knowledge_base = "\n\n".join(f"{chunk['title']}\n{chunk['content']}" for chunk in rewear_chunks)

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

# Initialize chat history
chat_history = [
    SystemMessage(content=system_prompt)
]

user_query = str(input("You: "))
chat_history.append(HumanMessage(content=user_query))

ai_response = llm.invoke(chat_history)
chat_history.append(ai_response) 

print(f"AI: {ai_response.content}")
