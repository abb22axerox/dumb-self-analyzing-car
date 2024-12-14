# AI-Driven RC Car




**A smart car that interprets its surroundings:**
This project aims to design and program a remote-controlled car that, using AI technology and various sensors, can interact with its environment. The car can identify objects, take pictures of its surroundings, and describe what it sees through a speaker.

**Team Members:**
William – Responsible for the car's construction and hardware assembly.
Axel – Responsible for Arduino coding and integration of electronic components.
Noah – Responsible for programming AI models for object recognition and software development.

**Features:**
Object Recognition: The camera identifies objects in the car's surroundings using AI and machine learning.
Photography: The car captures images of the environment and stores them for analysis.
Spoken Feedback: The speaker describes what the car sees, for example: "I see a person in front of me."
Sensor Integration: Built-in sensors help the car navigate and detect obstacles.

**Components and Technology:**
Hardware:
Remote-controlled car as the base
Camera for image capturing
Speaker for voice output
Sensors for distance and obstacle detection
Arduino microcontroller
Software:
Python for AI and image recognition
Arduino IDE for microcontroller programming
Machine learning libraries: TensorFlow or OpenCV

**Installation and Execution:**
Requirements
Arduino IDE
Python 3.10+
Libraries: OpenCV, TensorFlow, pyttsx3 (for text-to-speech synthesis)
Steps to Run the Project
Hardware Setup
Mount the sensors, camera, and speaker on the RC car.
Software Setup
Clone the repository:
bash
Copy code
git clone https://github.com/username/ai-rc-car.git
cd ai-rc-car
Install Python dependencies:
bash
Copy code
pip install -r requirements.txt
Upload Arduino Code
Open arduino_code.ino in Arduino IDE and upload it to the microcontroller.
Start the AI System
Run the Python script for object recognition and communication:
bash
Copy code
python ai_car.py

**Usage:**
Start the car using the remote control.
When the car identifies an object in its surroundings:
It takes a photo.
It provides a verbal description of the object through the speaker.
The car navigates autonomously and avoids obstacles using sensors.

**Future Improvements:**
Implement real-time mapping of the environment.
Enhance the car’s speech capabilities with natural language understanding.
Add support for multiple cameras to achieve a 360° field of view.
License
This project is developed for educational purposes and is not licensed for commercial use.

**Contact:**

Noah: noah.marklund@hitachigymnasiet.se
William: william.emilsson@hitachigymansiet.se
Axel: axel.roxenborg@hitachigymnasiet.se

