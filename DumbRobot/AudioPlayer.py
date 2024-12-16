from pydub import AudioSegment
from pydub.playback import play
import threading

class AudioPlayer:
    def __init__(self, volume_db):
        self.is_playing = False  # Tracks if audio is currently playing
        self.volume_db = volume_db

    def play_audio(self, file_path):
        """
        Play an audio file asynchronously.
        """
        def _play():
            if self.is_playing:
                return
            self.is_playing = True
            try:
                # Load and play the audio file
                audio = AudioSegment.from_file(file_path)
                audio = audio + self.volume_db
                play(audio)
            except Exception as e:
                print(f"Error playing audio: {e}")
            finally:
                self.is_playing = False

        # Start playback in a separate thread
        threading.Thread(target=_play, daemon=True).start()