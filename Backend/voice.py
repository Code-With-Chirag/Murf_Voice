import os 
from dotenv import load_dotenv
from murf import Murf 

# Load environment variables
load_dotenv()
client = Murf(api_key=os.getenv('MURF_API_KEY'))

# Get all available voices
voices = client.text_to_speech.get_voices()

# Filter only Hindi voices
hindi_voices = [voice for voice in voices if 'hi-IN' in voice.voice_id]

# Display Hindi voice information only
print("\n=== AVAILABLE HINDI VOICES ===")
print(f"Found {len(hindi_voices)} Hindi voices:\n")

for voice in hindi_voices:
    print(f"Voice: {voice.display_name}")
    print(f"ID: {voice.voice_id}")
    print(f"Available Moods: {', '.join(voice.available_styles)}")
    print("-" * 50)
