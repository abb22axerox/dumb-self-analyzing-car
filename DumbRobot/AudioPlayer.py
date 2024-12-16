from pydub import AudioSegment
from pydub.playback import play
import threading

class AudioPlayer:
    def __init__(self, volume_db):
        self.is_playing = False  # Tracks if audio is currently playing
        self.volume_db = volume_db
        self._playback_thread = None

    def play_audio(self, file_path, blocking=True):
        """
        Play an audio file. If `blocking` is True, wait until playback is finished.
        """
        def _play():
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

        if blocking:
            # Synchronous playback: execute _play in the current thread
            _play()
        else:
            # Asynchronous playback: start _play in a separate thread
            self._playback_thread = threading.Thread(target=_play, daemon=True)
            self._playback_thread.start()

    def wait_until_finished(self):
        """
        Wait until audio playback is finished (useful for synchronous control).
        """
        if self._playback_thread:
            self._playback_thread.join()
