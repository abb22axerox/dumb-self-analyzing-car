# AI-Driven RC Car

## Overview:
This project aims to design and program a remote-controlled car that, using AI technology and various sensors, can interact with its environment. The car can navigate its environment, take pictures of the surroundings, and describe what it sees through a speaker.

## Team Members:
- **William** – Responsible for the car's construction and hardware assembly.  
- **Axel** – Responsible for Arduino coding and integration of electronics.    
- **Noah** – Responsible for programming AI models for object recognition and user communication


## Features:
- **Object Recognition:** The camera identifies objects in the car's surroundings using AI, and navigates to avoid them.          
- **Photography:** The car captures images of the environment and analyses them.    
- **Spoken Feedback:** The mounted speaker describes what the car sees, for example: "I see a person in front of me." If the car detects a person in it's vicinity, it will try starting a conversation.
- **Artificial Engine Noises:** The car mounted speaker has build in engine sounds to simulate the feeling of a real, combustion car.

## Hardware:
- Self-build car frame
- Webcam for image capturing
- Speaker for voice output
- Sensors for distance and obstacle detection
- Arduino microcontroller
- Software:
- Python for AI and image recognition
- Arduino IDE for microcontroller programming
- Machine learning libraries: TensorFlow or OpenCV

## Installation and Execution:
### Requirements:
- Arduino IDE
- Python 3.10+
- Libraries: OpenCV, TensorFlow, pyttsx3 (for text-to-speech synthesis)

### Steps to Run the Project
1. Hardware setup (rc car with: raspberry pi, motor, servo, webcam, speaker)              
2. Clone this repository (https://github.com/username/ai-rc-car.git)
3. Open in a virtual environment
4. Install python dependencies
5. Navigate to DumbRobot/Main.py
6. Alter hardware & sortware settings to match your preferences
7. Execute Main.py

**Future Improvements:**
- Implement real-time mapping of the environment to improve the car's navigation abilities.
- Enhance the car’s speech capabilities with more user actions, such as adjusting volume settings on demand.
- Add support for multiple cameras to achieve a 360° field of view.

**Contact:**

**Noah:** noah.marklund@hitachigymnasiet.se                                       
**William:** william.emilsson@hitachigymansiet.se                                 
**Axel:** axel.roxenborg@hitachigymnasiet.se                                      