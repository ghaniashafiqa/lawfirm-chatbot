import requests
import json

class OpenAIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.endpoint = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def generate(self, prompt: str, max_tokens=1000, temperature=0.7):
        payload = {
            "model": "gpt-4o-mini",  # Using GPT-4o-mini
            "messages": [
                {
                    "role": "system", 
                    "content": "You are a helpful legal assistant for SAP Law Firm. Answer questions based on the provided context accurately and professionally. If the context doesn't contain enough information to fully answer the question, clearly state what information is missing and provide what you can based on the available context."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": False
        }
        
        try:
            response = requests.post(self.endpoint, 
                                   json=payload, 
                                   headers=self.headers, 
                                   timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        
        except requests.exceptions.RequestException as e:
            print(f"Error calling OpenAI API: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_details = e.response.json()
                    print(f"API Error Details: {error_details}")
                except:
                    print(f"Response status: {e.response.status_code}")
            return "I apologize, but I'm currently unable to process your request. Please try again later."
        except KeyError as e:
            print(f"Unexpected response format: {e}")
            return "I encountered an error processing your request. Please try again."