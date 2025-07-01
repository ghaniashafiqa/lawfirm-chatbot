from app.services.llm import OpenAIClient
from app.config import Config
import os
from dotenv import load_dotenv

def test_openai_connection():
    """Test script to verify OpenAI API connection"""
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment variables")
        return False
    
    print(f"🔑 Testing OpenAI API with key: {api_key[:10]}...")
    
    try:
        client = OpenAIClient(api_key)
        
        test_prompt = """Based on the following context, answer the question:

Context: SAP Law Firm provides comprehensive legal services including corporate law, litigation, and legal consultation.

Question: What services does SAP Law Firm provide?"""
        
        response = client.generate(test_prompt)
        print("✅ OpenAI API connection successful!")
        print(f"📝 Test response: {response}")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI API connection failed: {e}")
        return False

if __name__ == "__main__":
    test_openai_connection()