import base64
from openai import OpenAI
import os

# Initialize OpenAI client
client = OpenAI()

# Make the API call
completion = client.chat.completions.create(
    model="gpt-4o-audio-preview",
    modalities=["text", "audio"],
    audio={"voice": "onyx", "format": "mp3"},
    messages=[
        {
            "role": "user",
            "content": "Tell me what you think about Noah"
        }
    ]
)

# Print the completion response
print(completion.choices[0])

# Decode the audio data and save it as a .wav file
wav_bytes = base64.b64decode(completion.choices[0].message.audio.data)

# Set the path where you want to save the audio file
output_path = "/home/uaxel/Desktop/Programmering/Python/dumb-self-analyzing-car/testing/4o-direct-audio/dog.wav"

# Ensure the directory exists before saving the file
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Write the decoded audio to the specified path
with open(output_path, "wb") as f:
    f.write(wav_bytes)

print(f"Audio file saved at: {output_path}")
