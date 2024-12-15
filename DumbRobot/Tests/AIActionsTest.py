import base64
from openai import OpenAI

class AIActions:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def audio_to_text(self, audio_path):
        # Transcribe audio using Whisper model
        with open(audio_path, "rb") as audio_file:
            transcription = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcription.text

    def image_to_text(self, image_path):
        # Encode image in base64
        base64_image = self._encode_image(image_path)

        # Get description from GPT model
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "What is in this image?",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
        )
        return response.choices[0].message.content

    def text_to_audio(self, text, output_path):
        # Generate audio from text using a special model (as per the provided code)
        completion = self.client.chat.completions.create(
            model="gpt-4o-audio-preview",
            modalities=["text", "audio"],
            audio={"voice": "onyx", "format": "mp3"},
            messages=[
                {
                    "role": "user",
                    "content": text
                }
            ]
        )
        # Save the audio
        wav_bytes = base64.b64decode(completion.choices[0].message.audio.data)
        with open(output_path, "wb") as f:
            f.write(wav_bytes)

    @staticmethod
    def _encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')



# AI actions
ai = AIActions(api_key="sk-svcacct-dO8EKFhbR50o0EwRjz3r80imib9nqTaaeUPcZAr9BwmW08iHhTuQpq9f8xDxGT3BlbkFJ3Ee55z90UJH73WocK3DrPwMCgiIL7hk3l4vWo6wmNTlpYdRL9TLv9Dk8oyxoAA")

# Transcribe audio
transcription_text = ai.audio_to_text("dog.wav")
print(transcription_text)

# Describe image
description = ai.image_to_text("Desert.jpeg")
print(description)

# Generate audio from text
ai.text_to_audio("Thank you for the opportunity to be here.", "response.wav")