from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Optional
import os
import asyncio
import uuid
from datetime import datetime, timezone
from emergentintegrations.llm.chat import LlmChat, UserMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="SmartSpark API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.environ.get("DB_NAME", "smartspark")
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

# API key
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Models
class ChatMessage(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str

class ConversationHistory(BaseModel):
    conversation_id: str
    messages: List[dict]
    created_at: str
    updated_at: str

@app.get("/")
async def root():
    return {"message": "SmartSpark API is running!"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(chat_request: ChatMessage):
    try:
        # Generate conversation ID if not provided
        conversation_id = chat_request.conversation_id or str(uuid.uuid4())
        
        # Get or create conversation history
        conversation = await db.conversations.find_one({"conversation_id": conversation_id})
        if not conversation:
            conversation = {
                "conversation_id": conversation_id,
                "messages": [],
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
            await db.conversations.insert_one(conversation)
        
        # Add user message to history
        user_message = {
            "role": "user",
            "content": chat_request.message,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await db.conversations.update_one(
            {"conversation_id": conversation_id},
            {"$push": {"messages": user_message}, "$set": {"updated_at": datetime.now(timezone.utc).isoformat()}}
        )
        
        # Create LLM chat instance
        chat_instance = LlmChat(
            api_key=OPENAI_API_KEY,
            session_id=conversation_id,
            system_message="You are SmartSpark, a helpful and intelligent AI assistant. You are creative, knowledgeable, and always ready to help users with their questions and tasks."
        ).with_model("openai", "gpt-4o-mini")
        
        # Send message to OpenAI
        user_msg = UserMessage(text=chat_request.message)
        ai_response = await chat_instance.send_message(user_msg)
        
        # Add AI response to history
        ai_message = {
            "role": "assistant",
            "content": ai_response,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await db.conversations.update_one(
            {"conversation_id": conversation_id},
            {"$push": {"messages": ai_message}, "$set": {"updated_at": datetime.now(timezone.utc).isoformat()}}
        )
        
        return ChatResponse(response=ai_response, conversation_id=conversation_id)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@app.get("/api/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    try:
        conversation = await db.conversations.find_one({"conversation_id": conversation_id})
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Convert MongoDB ObjectId to string for JSON serialization
        conversation["_id"] = str(conversation["_id"])
        return conversation
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving conversation: {str(e)}")

@app.get("/api/conversations")
async def get_conversations():
    try:
        conversations = []
        async for conversation in db.conversations.find().sort("updated_at", -1):
            conversation["_id"] = str(conversation["_id"])
            conversations.append(conversation)
        return conversations
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving conversations: {str(e)}")

@app.delete("/api/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    try:
        result = await db.conversations.delete_one({"conversation_id": conversation_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return {"message": "Conversation deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting conversation: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)