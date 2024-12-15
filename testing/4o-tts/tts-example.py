from pathlib import Path
from openai import OpenAI
client = OpenAI()

speech_file_path = Path(__file__).parent / "speech.mp3"
response = client.audio.speech.create(
  model="tts-1",
  voice="onyx",
  input="Whoa, that was NOT part of the plan! What the heck?! I'm a car, not a wall-crashing machine! Fudge sticks, that hurt! I could use a mechanic, like, yesterday!"
)

response.stream_to_file(speech_file_path)