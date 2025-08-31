import os
from dotenv import load_dotenv
from murf import Murf

# Load environment variables
load_dotenv()

# Initialize Murf client
client = Murf(api_key=os.getenv('MURF_API_KEY'))

def test_manual_translation():
    """Test manual translation exactly like backend does"""
    print("=" * 60)
    print("TESTING MANUAL TRANSLATION")
    print("=" * 60)
    
    # Simulate request
    request_text = "Hello, how are you today?"
    translate = True
    target_language = "es-ES"
    
    print(f"Original text: {request_text}")
    print(f"Translate enabled: {translate}")
    print(f"Target language: {target_language}")
    
    text_to_generate = request_text
    translated_text = None
    
    if translate and target_language:
        try:
            print("\n🔄 Calling Murf translation API...")
            
            # Translate the text using Murf's translation API (correct format)
            translation_response = client.text.translate(
                target_language=target_language,
                texts=[request_text]  # texts parameter expects a list
            )
            
            print(f"Translation response type: {type(translation_response)}")
            print(f"Translation response: {translation_response}")
            
            # Extract translated text from response
            if hasattr(translation_response, 'translations') and translation_response.translations:
                print(f"Found translations: {len(translation_response.translations)}")
                
                # translations is a list of Translation objects
                first_translation = translation_response.translations[0]
                print(f"First translation object: {first_translation}")
                print(f"First translation type: {type(first_translation)}")
                
                if hasattr(first_translation, 'translated_text'):
                    translated_text = first_translation.translated_text
                    text_to_generate = translated_text
                    print(f"✅ Successfully extracted translated text: {translated_text}")
                else:
                    print("❌ No 'translated_text' attribute found")
                    translated_text = request_text
                    text_to_generate = request_text
            else:
                print("❌ No 'translations' attribute found or empty")
                translated_text = request_text
                text_to_generate = request_text
                
        except Exception as e:
            print(f"❌ Translation failed with error: {e}")
            import traceback
            traceback.print_exc()
            translated_text = request_text
            text_to_generate = request_text
    
    print(f"\nFINAL RESULTS:")
    print(f"Original text: {request_text}")
    print(f"Translated text: {translated_text}")
    print(f"Text for audio generation: {text_to_generate}")
    
def test_auto_translation():
    """Test auto translation to Hindi"""
    print("\n" + "=" * 60)
    print("TESTING AUTO TRANSLATION (English → Hindi)")
    print("=" * 60)
    
    # Simulate request
    request_text = "Good morning! How can I help you?"
    voice_language = "hi-IN"
    
    print(f"Original text: {request_text}")
    print(f"Voice language: {voice_language}")
    
    # Check if text appears to be English (simple check)
    is_english = not any(ord(char) > 127 for char in request_text)
    print(f"Text appears to be English: {is_english}")
    
    text_to_generate = request_text
    translated_text = None
    
    # Auto-translate if voice language is Hindi and text appears to be English
    if voice_language == "hi-IN" and is_english:
        try:
            print("\n🔄 Auto-translating to Hindi...")
            
            # Auto-translate to Hindi (correct format)
            translation_response = client.text.translate(
                target_language="hi-IN",
                texts=[request_text]  # texts parameter expects a list
            )
            
            print(f"Translation response: {translation_response}")
            
            # Extract translated text from response
            if hasattr(translation_response, 'translations') and translation_response.translations:
                # translations is a list of Translation objects
                first_translation = translation_response.translations[0]
                if hasattr(first_translation, 'translated_text'):
                    translated_text = first_translation.translated_text
                    text_to_generate = translated_text
                    print(f"✅ Auto-translation successful: {translated_text}")
                else:
                    print("❌ No 'translated_text' attribute found")
                    text_to_generate = request_text
            else:
                print("❌ No translations found")
                text_to_generate = request_text
                
        except Exception as e:
            print(f"❌ Auto-translation failed: {e}")
            import traceback
            traceback.print_exc()
            text_to_generate = request_text
    
    print(f"\nFINAL RESULTS:")
    print(f"Original text: {request_text}")
    print(f"Translated text: {translated_text}")
    print(f"Text for audio generation: {text_to_generate}")

if __name__ == "__main__":
    test_manual_translation()
    test_auto_translation()
