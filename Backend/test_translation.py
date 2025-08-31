import os
from dotenv import load_dotenv
from murf import Murf

# Load environment variables
load_dotenv()

# Initialize Murf client
client = Murf(api_key=os.getenv('MURF_API_KEY'))

try:
    print("Testing Murf Translation API...")
    print("-" * 40)
    
    # Test translation according to documentation
    response = client.text.translate(
        target_language="es-ES",
        texts=["Hello, world!", "How are you?"],
    )
    
    print("Translation Response:")
    print(f"Type: {type(response)}")
    print(f"Response: {response}")
    
    # Check available attributes
    print("\nAvailable attributes:")
    for attr in dir(response):
        if not attr.startswith('_'):
            print(f"  {attr}: {getattr(response, attr, 'N/A')}")
    
    # Test single text translation
    print("\n" + "="*50)
    print("Testing single text translation:")
    
    single_response = client.text.translate(
        target_language="hi-IN",
        texts=["Hello, how are you today?"],
    )
    
    print(f"Single Translation Response: {single_response}")
    
    # Check attributes for single response
    print("\nSingle response attributes:")
    for attr in dir(single_response):
        if not attr.startswith('_'):
            value = getattr(single_response, attr, 'N/A')
            if callable(value):
                continue
            print(f"  {attr}: {value}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
