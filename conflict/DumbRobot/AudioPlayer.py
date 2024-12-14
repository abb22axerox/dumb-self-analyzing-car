from pydub import AudioSegment
from pydub.playback import play
import threading

class AudioPlayer:
    def __init__(self):
        self.is_playing = False  # Tracks if audio is currently playing

    def play_audio(self, file_path):
        """
        Play an audio file asynchronously.
        """
        def _play():
            if self.is_playing:
                print("Audio file is already being played. Cannot play multiple audio files at once")
                return
            self.is_playing = True
            try:
                # Load and play the audio file
                audio = AudioSegment.from_file(file_path)
                play(audio)
            except Exception as e:
                print(f"Error playing audio: {e}")
            finally:
                self.is_playing = False

        # Start playback in a separate thread
        threading.Thread(target=_play, daemon=True).start()