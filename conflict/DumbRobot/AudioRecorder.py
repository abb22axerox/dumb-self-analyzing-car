import glob
import os
import wave
import pyaudio

class AudioRecorder:
    def __init__(self, record_seconds=5, record_cooldown=10, chunk=1024, channels=1, rate=44100, audio_folder="CapturedAudio"):
        """
        output_filename: Name of the output .wav file
        record_seconds: Duration of recording
        record_cooldown: Cooldown between recordings
        chunk: Buffer size
        channels: Number of audio channels
        rate: Sampling rate in Hz
        audio_folder: Path to the folder where captured audio is stored
        """
        self.audio_folder = audio_folder
        os.makedirs(self.audio_folder, exist_ok=True)  # Ensure folder exists
        
        self.record_seconds = record_seconds
        self.record_cooldown = record_cooldown
        self.chunk = chunk
        self.channels = channels
        self.rate = rate

    def clear_old_audio(self):
        # Delete all images in the audio_folder
        for file_path in glob.glob(os.path.join(self.audio_folder, "*")):
            os.remove(file_path)

    def record_audio(self, output_prefix="recording", output_suffix="999", on_audio_recorded=None):
        p = pyaudio.PyAudio()

        # Construct full output path
        filename = f"{output_prefix}_{output_suffix}.wav"
        output_path = os.path.join(self.audio_folder, filename)

        # Open stream
        stream = p.open(format=pyaudio.paInt16,
                         channels=self.channels,
                         rate=self.rate,
                         input=True,
                         frames_per_buffer=self.chunk)

        frames = []

        for _ in range(int(self.rate / self.chunk * self.record_seconds)):
            data = stream.read(self.chunk)
            frames.append(data)

        # Stop recording
        stream.stop_stream()
        stream.close()
        p.terminate()

        # Save the recorded frames to a WAV file
        wf = wave.open(output_path, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        print(f"Audio saved to {output_path}")

        if on_audio_recorded is not None:
            on_audio_recorded(output_path)