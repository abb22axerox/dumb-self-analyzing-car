import threading
import time
from pynput import keyboard

from AIActions import AIActions
from ImageProcessor import ImageProcessor
from AudioRecorder import AudioRecorder
from WebcamCapturer import WebcamCapturer
from AudioPlayer import AudioPlayer

program_running = True
audio_player = AudioPlayer()
ai = AIActions(api_key="sk-svcacct-dO8EKFhbR50o0EwRjz3r80imib9nqTaaeUPcZAr9BwmW08iHhTuQpq9f8xDxGT3BlbkFJ3Ee55z90UJH73WocK3DrPwMCgiIL7hk3l4vWo6wmNTlpYdRL9TLv9Dk8oyxoAA")

response_count = 1
frame_count = 1

voices = ['alloy',   # 0
          'echo',    # 1
          'fable',   # 2
          'onyx',    # 3
          'nova',    # 4
          'shimmer', # 5
          'coral',   # 6
          'verse',   # 7
          'ballad',  # 8
          'ash',     # 9
          'sage'     # 10
          ]
current_voice = voices[3]

def speak(text, voice="onyx"):
    global response_count
    response_audio_path = "DumbRobot/Captures/CapturedAudio/response_" + str(response_count) + ".mp3"
    response_count += 1
    ai.text_to_audio(text, response_audio_path, voice)
    audio_player.play_audio(file_path=response_audio_path)

def on_image_captured(image_path):
    global response_count
    global current_voice
    
    # 1. Ask the AI for car instructions (json format)
    description, action = ai.ask_about_wall_in_image(image_path)
    if description == None or action == None:
        print("WRN: Response invalid: on_image_captured")
        return
    print(description)
    print(action)

    # # 2. Convert AI response text back to audio and play it
    # if action != 'forward':
    #     speak(description, current_voice)

def on_audio_recorded(audio_path):
    global response_count
    global current_voice
    
    # 1. Convert audio to text
    user_text = ai.audio_to_text(audio_path)
    print(user_text)

    # 2. Ask the AI with the transcribed text
    response, voice, conversation = ai.ask_with_actions(user_text)
    print(voice)
    print(response)
    
    # 3. Change voice is requested
    if voice in voices:
        current_voice = voice

    # 3. Convert AI response text back to audio and play it
    speak(response, current_voice)
    
def check_input():
    global program_running

    def on_press(key):
        global program_running
        try:
            # Check if the program exit key is pressed
            if key.char == 'p':
                program_running = False
                print("Stopping program...")
                return False  # Stop the listener
        except AttributeError:
            pass

    # Start listening to keyboard events
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def image_loop(webcam):
    global frame_count
    
    # Clear old images once at the start
    webcam.clear_old_images()

    # Continuously capture frames while the program is running
    while program_running:
        time.sleep(webcam.capture_interval)
        
        print(f"----- Frame {frame_count} -----")
        webcam.capture_frame(output_prefix="frame", output_suffix=frame_count, on_image_captured=on_image_captured)
        print(f"----- Frame {frame_count} -----")
        
        frame_count += 1

    webcam.release()

def check_audio(audio_recorder):
    # Clear old audio once at the start
    audio_recorder.clear_old_audio()

    # Continuously capture audio while the program is running
    recording_index = 1
    while program_running:
        print("Audio recording started")
        audio_recorder.record_audio(output_prefix="recording", output_suffix=recording_index, on_audio_recorded=on_audio_recorded)
        recording_index += 1
        time.sleep(audio_recorder.record_cooldown)
    
if __name__ == "__main__":
    # Initialize the recorder and capturer
    audio_recorder = AudioRecorder(record_seconds=8, record_cooldown=5, audio_folder="DumbRobot/Captures/CapturedAudio")
    webcam = WebcamCapturer(device_index=0, capture_interval=2, images_folder="DumbRobot/Captures/CapturedImages")

    # Create threads for image capture, audio recording, and input checking
    input_thread = threading.Thread(target=check_input)
    audio_thread = threading.Thread(target=check_audio, args=(audio_recorder,))
    image_thread = threading.Thread(target=image_loop, args=(webcam,))

    # Start all threads
    input_thread.start()
    audio_thread.start()
    image_thread.start()

    # Wait for all threads to complete
    input_thread.join()
    audio_thread.join()
    image_thread.join()

    print("Program exited")