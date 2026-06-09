import logging
import os
from google.cloud import speech_v1
import io

logger = logging.getLogger(__name__)

# Language codes for supported languages
LANGUAGE_CODES = {
    "en": "en-US",
    "hi": "hi-IN",
    "ta": "ta-IN",
    "te": "te-IN",
    "kn": "kn-IN",
    "mr": "mr-IN",
    "bn": "bn-IN"
}

class VoiceProcessor:
    """
    Process voice input and convert to text
    """
    
    def __init__(self):
        """Initialize Google Cloud Speech client"""
        try:
            if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
                self.client = speech_v1.SpeechClient()
                self.google_enabled = True
            else:
                logger.warning("Google Cloud Speech not configured")
                self.google_enabled = False
        except Exception as e:
            logger.error(f"Failed to initialize Google Cloud Speech: {str(e)}")
            self.google_enabled = False
    
    async def transcribe_voice(
        self,
        audio_bytes: bytes,
        language: str = "en"
    ) -> dict:
        """
        Transcribe voice to text
        
        Args:
            audio_bytes: Audio file bytes
            language: Language code (en, hi, ta, te, kn, mr, bn)
        
        Returns:
            {
                "transcript": str,
                "language": str,
                "confidence": float,
                "error": str (if any)
            }
        """
        try:
            if not self.google_enabled:
                return {
                    "transcript": "",
                    "language": language,
                    "confidence": 0.0,
                    "error": "Google Cloud Speech not configured"
                }
            
            language_code = LANGUAGE_CODES.get(language, "en-US")
            
            # Prepare audio content
            audio = speech_v1.RecognitionAudio(content=audio_bytes)
            config = speech_v1.RecognitionConfig(
                encoding=speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code=language_code,
            )
            
            # Perform recognition
            response = self.client.recognize(config=config, audio=audio)
            
            # Extract transcript
            transcript = ""
            confidence = 0.0
            
            if response.results:
                result = response.results[0]
                if result.alternatives:
                    alternative = result.alternatives[0]
                    transcript = alternative.transcript
                    confidence = alternative.confidence
            
            logger.info(f"Transcribed voice in {language_code}")
            
            return {
                "transcript": transcript,
                "language": language,
                "confidence": float(confidence),
                "duration": len(audio_bytes) / 16000  # Approximate duration in seconds
            }
            
        except Exception as e:
            logger.error(f"Error transcribing voice: {str(e)}")
            return {
                "transcript": "",
                "language": language,
                "confidence": 0.0,
                "error": str(e)
            }
    
    @staticmethod
    def get_supported_languages() -> dict:
        """
        Get list of supported languages for voice input
        """
        return {
            "en": "English",
            "hi": "हिंदी (Hindi)",
            "ta": "தமிழ் (Tamil)",
            "te": "తెలుగు (Telugu)",
            "kn": "ಕನ್ನಡ (Kannada)",
            "mr": "मराठी (Marathi)",
            "bn": "বাংলা (Bengali)"
        }
    
    @staticmethod
    def save_audio(audio_bytes: bytes, filename: str) -> str:
        """
        Save uploaded audio file
        """
        try:
            os.makedirs("uploads/audio", exist_ok=True)
            filepath = os.path.join("uploads/audio", filename)
            
            with open(filepath, "wb") as f:
                f.write(audio_bytes)
            
            logger.info(f"Audio saved: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error saving audio: {str(e)}")
            return None
