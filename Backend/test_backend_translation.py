import requests
import json

# Test the backend translation functionality
BACKEND_URL = "http://localhost:8000"

def test_manual_translation():
    """Test manual translation to Spanish"""
    print("Testing Manual Translation (English -> Spanish)...")
    
    payload = {
        "text": "Hello, how are you today?",
        "voice": "Shaan",
        "mood": "Conversational",
        "pitch": 0,
        "translate": True,
        "target_language": "es-ES"
    }
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/generate",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Manual Translation Success!")
            print(f"Original: {result.get('original_text')}")
            print(f"Translated: {result.get('translated_text')}")
            print(f"Final: {result.get('final_text')}")
            print(f"Audio URL: {result.get('audio_url')[:50]}..." if result.get('audio_url') else "No audio URL")
        else:
            print(f"❌ Manual Translation Failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_auto_translation():
    """Test auto-translation to Hindi"""
    print("\nTesting Auto-Translation (English -> Hindi)...")
    
    payload = {
        "text": "Good morning! How can I help you?",
        "voice": "Shweta",
        "mood": "Conversational", 
        "pitch": 0,
        "translate": False,  # Auto-translation should trigger
        "target_language": None
    }
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/generate",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Auto-Translation Success!")
            print(f"Original: {result.get('original_text')}")
            print(f"Translated: {result.get('translated_text')}")
            print(f"Final: {result.get('final_text')}")
            print(f"Audio URL: {result.get('audio_url')[:50]}..." if result.get('audio_url') else "No audio URL")
        else:
            print(f"❌ Auto-Translation Failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_no_translation():
    """Test without any translation"""
    print("\nTesting No Translation...")
    
    payload = {
        "text": "This is a test message",
        "voice": "Shaan",
        "mood": "Conversational",
        "pitch": 0,
        "translate": False,
        "target_language": None
    }
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/generate",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ No Translation Success!")
            print(f"Original: {result.get('original_text')}")
            print(f"Translated: {result.get('translated_text')}")
            print(f"Final: {result.get('final_text')}")
        else:
            print(f"❌ No Translation Failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("Testing Backend Translation Functionality")
    print("=" * 50)
    
    test_manual_translation()
    test_auto_translation()
    test_no_translation()
    
    print("\n" + "=" * 50)
    print("Testing Complete!")
