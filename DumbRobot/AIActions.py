import base64
import json
from openai import OpenAI

VOICES = ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer', 
          'coral', 'verse', 'ballad', 'ash', 'sage']
          
class AIActions:
    def __init__(self, language, api_key):
        self.language = language
        self.client = OpenAI(api_key=api_key)

    def audio_to_text(self, audio_path):
        # Transcribe audio using Whisper model
        with open(audio_path, "rb") as audio_file:
            transcription = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcription.text

    def image_to_text(self, image_path, prompt="What is in this image?"):
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
                            "text": prompt,
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
            
    def ask_about_wall_in_image(self, image_path):
        # Encode image in base64
        base64_image = self._encode_image(image_path)

        # Updated prompt asking about walls and directions, and requesting a JSON response.
        prompt = [
            {
                "type": "text",
                "text": (
                    "Look at the image provided and respond in the following JSON format:\n"
                    "{\n"
                    "  \"description\": \"A detailed description of what is in the image, focusing heavily on one small detail. For your response, use the following language: + " + self.language + "\",\n"
                    "  \"action\": \"left\"/\"right\"/\"forward\"\n"
                    "}\n\n"
                    "The camera is mounted on a small car, so consider the perspective as being low to the ground.\n"
                    "If there is a wall or obstacle directly ahead, choose either \"left\" or \"right\" to avoid steering the car into a corner.\n"
                    "Keep in mind, the camera from which this picture is taken is placed on top of a small car, so only move to the side if any obstacle is VERY close to the camera.\n"
                    "If there is no immediate wall or obstacle blocking forward movement, choose \"forward\".\n"
                    "Write the description in " + self.language + " ONLY. The action should still be written in english.\n"
                    "Now, analyze the image carefully and produce ONLY the JSON object as described."
                )
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                },
            },
        ]

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        )
        response_text = response.choices[0].message.content.strip()

        # Find the indices of the actual JSON object
        start = response_text.find('{')
        end = response_text.rfind('}')

        if start != -1 and end != -1:
            json_content = response_text[start:end+1].strip()
            try:
                result = json.loads(json_content)
                description = result.get("description", "")
                action = result.get("action", "")
                return description, action
            except json.JSONDecodeError:
                print("The AI did not return valid JSON.")
                return None, None
        else:
            print("Could not find a JSON object in the response.")
            return None, None
        
    def ask_about_wall_and_hand_in_image(self, image_path):
        # Encode image in base64
        base64_image = self._encode_image(image_path)

        # Updated prompt asking about walls, directions, and hand presence, requesting a JSON response
        prompt = [
            {
                "type": "text",
                "text": (
                    "Look at the image provided and respond in the following JSON format:\n"
                    "{\n"
                    "  \"description\": \"A detailed description of what is in the image, focusing heavily on one small detail. For your response, use the following language: + " + self.language + "\",\n"
                    "  \"action\": \"left\"/\"right\"/\"forward\",\n"
                    "  \"hand_is_present\": true/false\n"
                    "}\n\n"
                    "The camera is mounted on a small car, so consider the perspective as being low to the ground.\n"
                    "If there is a wall or obstacle directly ahead, choose either \"left\" or \"right\" to avoid steering the car into a corner.\n"
                    "If there is no immediate wall or obstacle blocking forward movement, choose \"forward\".\n"
                    "Additionally, analyze whether a human hand is visible in the image. If it is, set \"hand_is_present\" to true; otherwise, set it to false.\n"
                    "Write the description in " + self.language + " ONLY. The action and hand presence should still be written in English.\n"
                    "Now, analyze the image carefully and produce ONLY the JSON object as described."
                )
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                },
            },
        ]

        # Send the prompt to the AI model
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        )
        response_text = response.choices[0].message.content.strip()

        # Find the indices of the actual JSON object
        start = response_text.find('{')
        end = response_text.rfind('}')

        if start != -1 and end != -1:
            json_content = response_text[start:end + 1].strip()
            try:
                result = json.loads(json_content)
                description = result.get("description", "")
                action = result.get("action", "")
                hand_is_present = result.get("hand_is_present", False)
                return description, action, hand_is_present
            except json.JSONDecodeError:
                print("The AI did not return valid JSON.")
                return None, None, None
        else:
            print("Could not find a JSON object in the response.")
            return None, None, None
    
    def ask(self, text):
        # A generic method to send text queries to the AI
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": text
                }
            ],
        )
        return response.choices[0].message.content.strip()
    
    def ask_with_actions(self, text, conversation=None):
        """
        Ask a question and maintain the conversation context.
        
        :param text: The user's query.
        :param conversation: A list of message dictionaries representing the conversation context.
        :return: A tuple containing the response message, the voice, and the updated conversation.
        """
        
        # Initialize the conversation if it's the first call
        if conversation is None:
            conversation = [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant that answers user queries with a short answer, and can optionally change its voice "
                        "If any specific name is mentioned, look up as much information as possible online, preferably from the MrKoll website, and respond using as detailed of a description of the person as possible. An incredible amount of detail."
                        "If the name Judith is mentioned, then the full name is Judith Maj Linn Beck Johansson"
                        "If the name Jeton is mentioned, then the full name is Jeton Mustini. In this case don't look up information, just tell some joke about him and Kalle Kula"
                        "If the name Lars is mentioned, then the full name is Lars Fryxell"
                        "If the name Joakim is mentioned, then the full name is Joakim Flink"
                        "If the name Sofie is mentioned, then the full name is Sofie Ahlberg"
                        "for Text-to-Speech purposes. The user may request a specific voice from the following list: "
                        f"{', '.join(VOICES)}."
                        "ANSWER ONLY USING JSON FORMAT. THERE SHOULD BE A 'response', AS WELL AS A 'voice' IF REQUESTED BY THE USER. OTHERWISE, DONT INCLUDE THE 'voice' IN THE JSON!"
                        "For your 'response', use the following language: + " + self.language
                    )
                }
            ]

        # Add the user's input to the conversation
        conversation.append({
            "role": "user",
            "content": text
        })

        # Limit the conversation length to avoid overload
        max_context_length = 10  # Adjust as needed
        if len(conversation) > max_context_length:
            conversation = conversation[-max_context_length:]

        # Send the prompt to the AI with the conversation context
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation
        )

        # Extract the AI's response
        response_text = response.choices[0].message.content.strip()

        # Clean the response by removing Markdown code fences if present
        if response_text.startswith("```") and response_text.endswith("```"):
            response_text = '\n'.join(response_text.split('\n')[1:-1])

        # Parse the JSON response
        try:
            result = json.loads(response_text)
            response_message = result.get("response", "")
            voice = result.get("voice", None)
            if not voice == None:
                if not voice in response_message.lower():
                    voice = None
        except json.JSONDecodeError:
            print("The AI did not return valid JSON. Returning raw response.")
            response_message = response_text
            voice = None

        # Add the AI's response to the conversation
        conversation.append({
            "role": "assistant",
            "content": response_message
        })

        return response_message, voice, conversation

    def text_to_audio(self, text, output_path, voice="onyx"):
        # Generate audio from text using a special model (as per the provided code)
        completion = self.client.chat.completions.create(
            model="gpt-4o-audio-preview",
            modalities=["text", "audio"],
            audio={"voice": voice, "format": "mp3"},
            messages=[
                {
                    "role": "user",
                    "content": "REPEAT THE FOLLOWING TEXT. DON'T CHANGE A SINGLE FUDGING WORD!!!!!!!: " + text
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