import threading
import time
from pynput import keyboard

from AIActions import AIActions
from ImageProcessor import ImageProcessor
from AudioRecorder import AudioRecorder
from WebcamCapturer import WebcamCapturer
from AudioPlayer import AudioPlayer

#cd ~/Desktop/Programmering/Python/dumb-self-analyzing-car/conflict/DumbRobot && export OPENAI_API_KEY="sk-svcacct-dO8EKFhbR50o0EwRjz3r80imib9nqTaaeUPcZAr9BwmW08iHhTuQpq9f8xDxGT3BlbkFJ3Ee55z90UJH73WocK3DrPwMCgiIL7hk3l4vWo6wmNTlpYdRL9TLv9Dk8oyxoAA" && source myenv/bin/activate
#sudo python3 Main.py

# Counters
response_count = 0
recording_count = 0
frame_count = 0

# Constants
VOICES = ['alloy',   # 0
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
ASK_FOR_QUESTIONS_TRANSLATIONS = {
    "English": "Hello! Do you have any questions for me?",
    "Swedish": "Hej! Har du några frågor till mig?",
    "German": "Hallo! Hallo! Haben Sie Fragen?"
}

# Primary settings
voice_language = "English" # Supported languages: English, Swedish, German
do_use_car_controller = False
motor_speed = 0.5
servo_angle_normalised = 0.5
voice_volume_db = 0
engine_volume_db = -20
current_voice = VOICES[3]

#Advanced settings
debug_mode = True
do_use_parallel_ai_communication = False

SELECTED_ASK_FOR_QUESTIONS_TRANSLATION = ASK_FOR_QUESTIONS_TRANSLATIONS[voice_language]

# Conditional imports
if do_use_car_controller:
    import CarController
    
# Paths
audio_folder_path = "DumbRobot/Captures/CapturedAudio"
images_folder_path = "DumbRobot/Captures/CapturedImages"
engine_audio_file = "DumbRobot/Data/Audio/EngineC.mp3"

# Other
program_running = True
audio_player = AudioPlayer(voice_volume_db)
engine_audio_player = AudioPlayer(engine_volume_db)
ai = AIActions(voice_language, api_key="sk-svcacct-dO8EKFhbR50o0EwRjz3r80imib9nqTaaeUPcZAr9BwmW08iHhTuQpq9f8xDxGT3BlbkFJ3Ee55z90UJH73WocK3DrPwMCgiIL7hk3l4vWo6wmNTlpYdRL9TLv9Dk8oyxoAA")
current_car_action = 'stationary'

# Initialize the audio recorder and webcam
audio_recorder = AudioRecorder(record_seconds=8, record_cooldown=5, audio_folder_path=audio_folder_path)
webcam = WebcamCapturer(device_index=0, capture_interval=2, images_folder_path=images_folder_path)

def print_debug(text):
    if debug_mode:
        print(text)

def speak(text, voice="onyx"):
    global response_count, audio_folder_path
    response_audio_path = audio_folder_path + "/response_" + str(response_count) + ".mp3"
    response_count += 1
    ai.text_to_audio(text, response_audio_path, voice)
    audio_player.play_audio(file_path=response_audio_path)
    
def ask_for_questions():
    global SELECTED_ASK_FOR_QUESTIONS_TRANSLATION
    speak(SELECTED_ASK_FOR_QUESTIONS_TRANSLATION, current_voice)
    return
    
def record_and_answer():
    global recording_count, audio_recorder
    print("Audio recording started")
    audio_recorder.record_audio(output_prefix="recording", output_suffix=recording_count, on_audio_recorded=on_audio_recorded)
    recording_count += 1
    time.sleep(audio_recorder.record_cooldown)

def on_audio_recorded(audio_path):
    global response_count, current_voice
    
    # 1. Convert audio to text
    user_text = ai.audio_to_text(audio_path)
    print_debug(user_text)

    # 2. Ask the AI with the transcribed text
    response, voice, conversation = ai.ask_with_actions(user_text)
    print_debug(voice)
    print_debug(response)
    
    # 3. Change voice if requested
    if voice in VOICES:
        current_voice = voice

    # 4. Convert AI response text back to audio and play it
    speak(response, current_voice)
    
def on_image_captured(image_path):
    global response_count, current_voice, current_car_action
    
    # 1. Ask the AI for car instructions (using a JSON response format)
    description, action = ai.ask_about_wall_in_image(image_path)
    if description == None or action == None:
        print("WRN: Response invalid: on_image_captured")
        return
    print_debug(description)
    print_debug(action)

    # 2. Update car controller state
    current_car_action = action

    # 3. Convert AI response text back to audio and play it
    if action != 'forward':
        speak(description, current_voice)
        
def on_image_captured_linear(image_path):
    global response_count, current_voice, current_car_action
    
    # 1. Ask the AI for car instructions and detect nearby people (using a JSON response format)
    description, action, hand_is_present = ai.ask_about_wall_and_hand_in_image(image_path)
    if description == None or action == None or hand_is_present == None:
        print("WRN: Response invalid: on_image_captured")
        return
    print_debug(description)
    print_debug(action)
    print_debug(hand_is_present)

    # 2. Update car controller state
    current_car_action = action

    # 3. Convert AI response text back to audio and play it
    if hand_is_present:
        ask_for_questions()
        record_and_answer()
    elif action != 'forward':
        speak(description, current_voice)
    
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

def car_controller_loop():
    while program_running and do_use_car_controller:
        if(current_car_action == 'forward'):
            CarController.drive_car(0, motor_speed)
        elif(current_car_action == 'left'):
            CarController.drive_car(-servo_angle_normalised, 0)
        elif(current_car_action == 'right'):
            CarController.drive_car(servo_angle_normalised, 0)
        else:
            CarController.drive_car(0, 0)

def audio_loop():
    # Clear old audio once at the start
    audio_recorder.clear_old_audio()

    # Continuously capture audio while the program is running
    while program_running:
        record_and_answer()

def image_loop(do_use_parallel_communication):
    global frame_count, webcam
    
    # Clear old images once at the start
    webcam.clear_old_images()

    # Continuously capture frames while the program is running
    while program_running:
        time.sleep(webcam.capture_interval)
        
        print_debug(f"----- Frame {frame_count} -----")
        if do_use_parallel_communication:
            webcam.capture_frame(output_prefix="frame", output_suffix=frame_count, on_image_captured=on_image_captured)
        else:
            webcam.capture_frame(output_prefix="frame", output_suffix=frame_count, on_image_captured=on_image_captured_linear)
        print_debug(f"----- Frame {frame_count} -----")
        
        frame_count += 1

    webcam.release()
    
def engine_audio_loop():
    while program_running:
        engine_audio_player.play_audio(file_path=engine_audio_file)
        time.sleep(0.1)
    
def main_parallel():
    # Create threads for image capture, audio recording, and input listener
    input_thread = threading.Thread(target=check_input)
    audio_thread = threading.Thread(target=audio_loop, args=())
    image_thread = threading.Thread(target=image_loop, args=(True,))
    engine_audio_thread = threading.Thread(target=engine_audio_loop)
    car_controller_thread = threading.Thread(target=car_controller_loop, args=())

    # Start all threads
    input_thread.start()
    audio_thread.start()
    image_thread.start()
    engine_audio_thread.start()
    car_controller_thread.start()

    # Wait for all threads to complete
    input_thread.join()
    audio_thread.join()
    image_thread.join()
    engine_audio_thread.join()
    car_controller_thread.join()

    print("Program exited")
    
def main_linear():
    # Create threads for image- and audio capture, and input listener
    input_thread = threading.Thread(target=check_input)
    image_audio_thread = threading.Thread(target=image_loop, args=(False,))
    engine_audio_thread = threading.Thread(target=engine_audio_loop)
    car_controller_thread = threading.Thread(target=car_controller_loop, args=())

    # Start all threads
    input_thread.start()
    image_audio_thread.start()
    engine_audio_thread.start()
    car_controller_thread.start()

    # Wait for all threads to complete
    input_thread.join()
    image_audio_thread.join()
    engine_audio_thread.join()
    car_controller_thread.join()

    print("Program exited")
    
if __name__ == "__main__":
    if do_use_parallel_ai_communication:
        main_parallel()
    else:
        main_linear()