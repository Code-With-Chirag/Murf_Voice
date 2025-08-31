from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import requests
from murf import Murf
import tempfile
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="MurfAI Text-to-Speech API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Murf client
API_KEY = os.getenv('MURF_API_KEY')  # Add your Murf API key to .env file
if not API_KEY:
    raise ValueError("MURF_API_KEY not found in environment variables")

client = Murf(api_key=API_KEY)

# Pydantic models
class TextToSpeechRequest(BaseModel):
    text: str
    voice: Optional[str] = "Shaan"  # Changed from Miles to Shaan (valid Hindi voice)
    mood: Optional[str] = "Conversational"
    pitch: Optional[int] = 0
    translate: Optional[bool] = False
    target_language: Optional[str] = None

class DownloadRequest(BaseModel):
    audio_url: str

# Voice Settings with language mappings
VOICE_MOODS = {
    "Shaan": {
        "voice_id": "hi-IN-shaan",
        "moods": ['Conversational', 'Promo', 'Calm', 'Sad'],
        "language": "hi-IN"
    },
    "Rahul": {
        "voice_id": "hi-IN-rahul",
        "moods": ['Conversational'],
        "language": "hi-IN"
    },
    "Shweta": {
        "voice_id": "hi-IN-shweta",
        "moods": ['Conversational', 'Promo', 'Calm', 'Sad'],
        "language": "hi-IN"
    },
    "Amit": {
        "voice_id": "hi-IN-amit",
        "moods": ['Conversational'],
        "language": "hi-IN"
    },
    "Kabir": {
        "voice_id": "hi-IN-kabir",
        "moods": ['Conversational'],
        "language": "hi-IN"
    },
    "Ayushi": {
        "voice_id": "hi-IN-ayushi",
        "moods": ['Conversational'],
        "language": "hi-IN"
    }
}

@app.get("/")
async def home():
    """Home route"""
    return {
        'message': 'MurfAI Text-to-Speech Backend API',
        'status': 'running'
    }

@app.get("/api/voices")
async def get_voices():
    """Get available voices and their moods"""
    try:
        return {
            'success': True,
            'voices': VOICE_MOODS
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate")
async def generate_audio(request: TextToSpeechRequest):
    """Generate audio from text using Murf AI with optional translation"""
    try:
        # Validate input
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text is required")
        
        # Get voice ID and language
        voice_config = VOICE_MOODS.get(request.voice, {})
        voice_id = voice_config.get('voice_id')
        voice_language = voice_config.get('language')
        
        if not voice_id:
            raise HTTPException(status_code=400, detail=f"Invalid voice: {request.voice}")
        
        # Prepare text for generation
        text_to_generate = request.text
        translated_text = None
        
        # If translation is requested or voice language is different from English
        if request.translate and request.target_language:
            try:
                # Translate the text using Murf's translation API (correct format)
                translation_response = client.text.translate(
                    target_language=request.target_language,
                    texts=[request.text]  # texts parameter expects a list
                )
                
                # Extract translated text from response
                if hasattr(translation_response, 'translations') and translation_response.translations:
                    # translations is a list of Translation objects
                    first_translation = translation_response.translations[0]
                    if hasattr(first_translation, 'translated_text'):
                        translated_text = first_translation.translated_text
                        text_to_generate = translated_text
                    else:
                        translated_text = request.text
                        text_to_generate = request.text
                else:
                    # If translation fails, use original text
                    translated_text = request.text
                    text_to_generate = request.text
                    
            except Exception as e:
                # If translation fails, continue with original text
                print(f"Translation failed: {e}")
                translated_text = request.text
                text_to_generate = request.text
        
        # Auto-translate if voice language is Hindi and text appears to be English
        elif voice_language == "hi-IN" and not any(ord(char) > 127 for char in request.text):
            try:
                # Auto-translate to Hindi (correct format)
                translation_response = client.text.translate(
                    target_language="hi-IN",
                    texts=[request.text]  # texts parameter expects a list
                )
                
                # Extract translated text from response
                if hasattr(translation_response, 'translations') and translation_response.translations:
                    # translations is a list of Translation objects
                    first_translation = translation_response.translations[0]
                    if hasattr(first_translation, 'translated_text'):
                        translated_text = first_translation.translated_text
                        text_to_generate = translated_text
                    else:
                        text_to_generate = request.text
                else:
                    # If translation fails, use original text
                    text_to_generate = request.text
                    
            except Exception as e:
                # If auto-translation fails, use original text
                print(f"Auto-translation failed: {e}")
                text_to_generate = request.text
        
        # Generate audio using Murf
        response = client.text_to_speech.generate(
            format="MP3",
            sample_rate=48000.0,
            channel_type="STEREO",
            text=text_to_generate,
            voice_id=voice_id,
            style=request.mood,
            pitch=request.pitch
        )
        
        audio_url = response.audio_file if hasattr(response, "audio_file") else None
        
        if not audio_url:
            raise HTTPException(status_code=500, detail="Failed to generate audio")
        
        # Debug information
        print(f"DEBUG - Original text: {request.text}")
        print(f"DEBUG - Translated text: {translated_text}")
        print(f"DEBUG - Final text for audio: {text_to_generate}")
        print(f"DEBUG - Translation enabled: {request.translate}")
        print(f"DEBUG - Target language: {request.target_language}")
        print(f"DEBUG - Voice language: {voice_language}")
        
        return {
            'success': True,
            'audio_url': audio_url,
            'original_text': request.text,
            'translated_text': translated_text,
            'final_text': text_to_generate,
            'voice_language': voice_language,
            'translation_enabled': request.translate,
            'target_language': request.target_language,
            'message': 'Audio generated successfully'
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/download")
async def download_audio(request: DownloadRequest):
    """Download and serve audio file"""
    try:
        if not request.audio_url:
            raise HTTPException(status_code=400, detail="Audio URL is required")
        
        # Download the audio file
        response = requests.get(request.audio_url, stream=True)
        
        if response.status_code == 200:
            # Create a temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            
            # Write audio data to temp file
            for chunk in response.iter_content(chunk_size=1024):
                temp_file.write(chunk)
            
            temp_file.close()
            
            # Return the file
            return FileResponse(
                temp_file.name,
                media_type='audio/mpeg',
                filename='generated_audio.mp3'
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to download audio")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    host = os.getenv('HOST', 'localhost')
    port = int(os.getenv('PORT', 8000))
    
    uvicorn.run(app, host=host, port=port)
