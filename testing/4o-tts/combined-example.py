from openai import OpenAI
from pathlib import Path
 
client = OpenAI()
 
class Chat:
    def __init__(self, initial_prompt):
        self.messages = [{"role": "system", "content": initial_prompt}]
    def add_user_message(self, content):
        self.messages.append({"role": "user", "content": content})
    def add_assistant_message(self, content):
        self.messages.append({"role": "assistant", "content": content})
    def get_response(self, model="gpt-4o-mini"):
        completion = client.chat.completions.create(
            model=model,
            messages=self.messages
        )
        assistant_reply = completion.choices[0].message.content
        self.add_assistant_message(assistant_reply)
        return assistant_reply
 
def startup_chat(initial_prompt, initial_user_message):
    chat = Chat(initial_prompt)
    chat.add_user_message(initial_user_message)
    response = chat.get_response()
    return chat, response
 
def new_message(chat, content):
    chat.add_user_message(content)
    response = chat.get_response()
    return response
 
def generate_speech(text, filename="speech.mp3"):
    # Define the file path
    speech_file_path = Path(__file__).parent / filename
 
    # Generate the audio
    response = client.audio.speech.create(
        model="tts-1",
        voice="onyx",
        input=text.upper()
    )
 
    # Save to file
    response.stream_to_file(speech_file_path)
    print(f"Audio file saved at {speech_file_path}")
 
# Example usage:
 
# Starting a new chat session
initial_prompt = "You are an idiot car that can talk, really dumb."
initial_user_message = (
    "You just rammed into a wall, use swearwords and describe how you feel while screaming in three sentences. "
    "Use loads of exclamation marks. Use extremely simple language, almost like you are not a native speaker."
)
chat1, initial_response1 = startup_chat(initial_prompt, initial_user_message)
print("Assistant:", initial_response1)
 
# Continue the conversation
user_message1 = "What will you do next?"
response1 = new_message(chat1, user_message1)
print("Assistant:", response1)
 
# Generate speech from the assistant's reply
generate_speech(response1, filename="assistant_reply.mp3")
 
# Starting another chat session
chat2, initial_response2 = startup_chat("You are a wise old owl.", "Share some wisdom.")
print("Assistant:", initial_response2)
 
# Continue the conversation
user_message2 = "Tell me more."
response2 = new_message(chat2, user_message2)
print("Assistant:", response2)