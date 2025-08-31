import streamlit as st
import requests
import json
import os
import sys
import tempfile
from io import BytesIO
from qr import generate_qr_png

# Configure Streamlit page
st.set_page_config(
    page_title="AI FriendZone",
    page_icon="🎙️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #FFD700;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stSelectbox > div > div > select {
        background-color: #2A2A3B;
        color: white;
        border: 2px solid #FFD700;
    }
    .stTextArea > div > div > textarea {
        background-color: #2A2A3B;
        color: white;
        border: 2px solid #FFD700;
        border-radius: 15px;
    }
    .stSlider > div > div > div {
        background-color: #FFD700;
    }
    div[data-testid="stSidebar"] {
        background-color: #1E1E2F;
    }
    .main {
        background-color: #1E1E2F;
    }
</style>
""", unsafe_allow_html=True)

# Backend API configuration
BACKEND_URL = "http://localhost:8000"

# Voice configurations (matching the backend - Hindi voices)
VOICE_MOODS = {
    "Shaan": ['Conversational', 'Promo', 'Calm', 'Sad'],
    "Rahul": ['Conversational'],
    "Shweta": ['Conversational', 'Promo', 'Calm', 'Sad'],
    "Amit": ['Conversational'],
    "Kabir": ['Conversational'],
    "Ayushi": ['Conversational']
}

# Language options for translation
TRANSLATION_LANGUAGES = {
    "Hindi": "hi-IN",
    "English (India)": "en-IN",
    "Spanish": "es-ES",
    "French": "fr-FR",
    "German": "de-DE",
    "Italian": "it-IT",
    "Portuguese": "pt-BR",
    "Chinese": "zh-CN",
    "Japanese": "ja-JP",
    "Korean": "ko-KR",
    "Tamil" : "ta-IN",
    "Bengali" : "bn-IN",
}

def get_voices():
    """Fetch available voices from backend"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/voices")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                return data.get('voices', {})
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to backend: {e}")
    return VOICE_MOODS

def generate_audio(text, voice, mood, pitch, translate=False, target_language=None):
    """Generate audio using the backend API with optional translation"""
    try:
        payload = {
            "text": text,
            "voice": voice,
            "mood": mood,
            "pitch": pitch,
            "translate": translate,
            "target_language": target_language
        }
        
        response = requests.post(
            f"{BACKEND_URL}/api/generate",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to backend: {e}")
        return None

def download_audio(audio_url):
    """Download audio file from URL"""
    try:
        response = requests.get(audio_url, stream=True)
        if response.status_code == 200:
            return response.content
        else:
            st.error("Failed to download audio file")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error downloading audio: {e}")
        return None

def main():
    st.info(f"Streamlit is using Python: {sys.executable}")

    # Sidebar with examples and info
    with st.sidebar:
        st.markdown("## 📚 Examples & Tips")
        
        st.markdown("### 📝 Sample Texts to Try:")
        
        if st.button("💬 English Greeting", use_container_width=True):
            st.session_state.sample_text = "Hello! Welcome to AI FriendZone. How can I help you today?"
        
        if st.button("📈 Business Message", use_container_width=True):
            st.session_state.sample_text = "Good morning! Thank you for joining our meeting. Let's begin with today's agenda."
        
        if st.button("🎆 Celebration", use_container_width=True):
            st.session_state.sample_text = "Congratulations on your achievement! You have done an excellent job."
        
        if st.button("📚 Educational", use_container_width=True):
            st.session_state.sample_text = "Welcome to today's lesson. We will learn about artificial intelligence and its applications."
        
        st.markdown("---")
        st.markdown("### 🌐 Translation Features:")
        st.markdown("""
        - **Auto-Translation**: English text automatically translates to Hindi
        - **Manual Translation**: Choose from 9 languages
        - **No Translation**: Use text as-is
        """)
        
        st.markdown("### 🎤 Available Voices:")
        st.markdown("""
        - **Shaan** (M): 4 moods available
        - **Shweta** (F): 4 moods available  
        - **Rahul** (M): Conversational
        - **Amit** (M): Conversational
        - **Kabir** (M): Conversational
        - **Ayushi** (F): Conversational
        """)
        
        st.markdown("### 🔧 Supported Languages:")
        for lang_name, lang_code in TRANSLATION_LANGUAGES.items():
            st.markdown(f"- **{lang_name}**: `{lang_code}`")
    
    # Title
    st.markdown('<h1 class="main-header">🎙️ AI FriendZone</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #FFD700; font-size: 1.2rem;">Text-to-Speech with Multi-Language Translation</p>', unsafe_allow_html=True)
    
    # Get available voices
    voices = get_voices()
    
    # Create the UI in a container
    with st.container():
        # Text input
        st.markdown("### 📝 Enter Your Text")
        
        # Use sample text if available
        default_text = st.session_state.get('sample_text', '')
        
        text_input = st.text_area(
            "Text to Convert",
            value=default_text,
            height=120,
            placeholder="Type your text here (English recommended for best translation results)...",
            help="Enter text in English for automatic translation to match voice language, or enable manual translation for other languages."
        )
        
        # Clear sample text after it's used
        if 'sample_text' in st.session_state:
            del st.session_state.sample_text
        
        # Voice and mood selection
        st.markdown("### 🎤 Voice Configuration")
        col1, col2 = st.columns(2)
        
        with col1:
            selected_voice = st.selectbox(
                "Choose Voice (All Hindi)",
                options=list(voices.keys()),
                index=0,
                help="All available voices are Hindi speakers"
            )
        
        with col2:
            # Update moods based on selected voice
            available_moods = voices.get(selected_voice, {}).get('moods', ['Conversational'])
            selected_mood = st.selectbox(
                "Choose Mood",
                options=available_moods,
                index=0,
                help="Select the emotional tone for the voice"
            )
        
        # Translation options
        st.markdown("### 🌐 Translation Settings")
        
        # Translation mode selection
        translation_mode = st.radio(
            "Translation Mode",
            ["Auto-Translation (English → Hindi)", "Manual Translation", "No Translation to English (India)"],
            index=0,
            help="Choose how you want to handle text translation"
        )
        
        enable_translation = False
        target_language = None
        
        if translation_mode == "Manual Translation":
            enable_translation = True
            col3, col4 = st.columns(2)
            
            with col3:
                language_name = st.selectbox(
                    "Translate To",
                    options=list(TRANSLATION_LANGUAGES.keys()),
                    index=0,
                    help="Select target language for translation"
                )
                target_language = TRANSLATION_LANGUAGES.get(language_name)
            
            with col4:
                st.markdown("**Selected Language Code:**")
                st.code(target_language if target_language else "None")
        
        elif translation_mode == "Auto-Translation (English → Hindi)":
            st.info(
                "🔄 **Auto-Translation Active**: English text will be automatically translated to Hindi "
                "when using Hindi voices. Perfect for natural Hindi speech generation!"
            )
        
        elif translation_mode == "No Translation to English (India)":
            enable_translation = True
            target_language = "en-IN"
            st.info(
                "🇮🇳 **English (India) Translation**: Text will be translated to English (India) variant. "
                "This is ideal for Indian English accent and expressions."
            )
        
        else:  # No Translation
            st.warning(
                "⚠️ **No Translation**: Text will be used as-is. Make sure your text matches the voice language "
                "(Hindi) for best results."
            )
        
        # Pitch adjustment
        st.markdown("### 🎵 Voice Settings")
        pitch_value = st.slider(
            "Pitch Adjustment (%)",
            min_value=-30,
            max_value=30,
            value=0,
            step=5,
            help="Adjust the pitch of the voice. Negative values = lower pitch, Positive values = higher pitch"
        )
        
        # Generate button
        if st.button("🎵 Generate Voice", type="primary"):
            if not text_input.strip():
                st.error("Please enter some text to convert to speech.")
            else:
                with st.spinner("Generating audio... Please wait."):
                    # Generate audio with optional translation
                    result = generate_audio(
                        text_input, 
                        selected_voice, 
                        selected_mood, 
                        pitch_value,
                        translate=enable_translation,
                        target_language=target_language
                    )
                    
                    if result and result.get('success'):
                        audio_url = result.get('audio_url')
                        
                        if audio_url:
                            st.success("Audio generated successfully!")
                            
                            # Show translation results if available
                            if result.get('translated_text'):
                                st.markdown("### Translation Results")
                                col_orig, col_trans = st.columns(2)
                                
                                with col_orig:
                                    st.markdown("**Original Text:**")
                                    st.write(result.get('original_text', text_input))
                                
                                with col_trans:
                                    st.markdown("**Translated Text:**")
                                    st.write(result.get('translated_text'))
                            
                            # Download and play audio
                            audio_data = download_audio(audio_url)
                            
                            if audio_data:
                                # Display audio player
                                st.audio(audio_data, format="audio/mp3")
                                
                                # Download button
                                st.download_button(
                                    label="📥 Download Audio",
                                    data=audio_data,
                                    file_name="generated_audio.mp3",
                                    mime="audio/mp3"
                                )
                            # Shareable link + QR (show whenever we have an audio_url)
                            st.markdown("### 🔗 Share")
                            
                            col_share1, col_share2 = st.columns([3, 1])
                            with col_share1:
                                st.markdown(f"[Open generated audio link]({audio_url})")
                            with col_share2:
                                st.button("📋 Copy Link", key=f"copy-{audio_url}")
                                st.markdown(
                                f'''
                                <script>
                                function copyToClipboard(text) {{
                                    navigator.clipboard.writeText(text).then(function() {{
                                        // Optional: Show a success message or change button text
                                    }}, function(err) {{
                                        alert('Could not copy text: ', err);
                                    }});
                                }}
                                const button = window.parent.document.querySelector('[data-testid="stButton"] > button:contains("📋 Copy Link")');
                                if (button) {{
                                    button.onclick = function() {{ copyToClipboard('{audio_url}'); }}
                                }}
                                </script>
                                ''',
                                unsafe_allow_html=True
                            )

                            try:
                                # Use scale=4 as requested for a smaller QR code
                                qr_png = generate_qr_png(audio_url, scale=4, border=2)
                                st.image(qr_png, caption="Scan to open audio", use_container_width=False)
                            except Exception as e:
                                st.warning(f"Could not generate QR code: {e}")
                        else:
                            st.error("Failed to get audio URL from the response.")
                    else:
                        error_msg = result.get('error', 'Unknown error occurred') if result else 'Failed to generate audio'
                        st.error(f"Error: {error_msg}")

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>Powered by MurfAI | Built with Streamlit & FastAPI</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
