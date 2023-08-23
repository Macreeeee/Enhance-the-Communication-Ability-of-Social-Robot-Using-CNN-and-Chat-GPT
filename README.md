# Enhance the Communication Ability of Social Robot Using CNN and Chat-GPT
MSc project. A application for Nao robot with face varification, face expression recognition, AI-driven conversation and motion functions.

This application integrates ChatGPT into Nao robot to endowing it with flexible response.

Third-party APIs:
Deepface, FER for face expression recognition
VOSK for speech to text
ChatGPT for AI-driven content generation

To run this application, you need to have two versions of Python: Python 2.7 and Python 3.7. They should be able to run with "python27 program.py" and "python program.py" respectively. If this envolve error when running, please change the python exe folder name according to above, or change the code calling python in this applicaiton.

To install requirements:
python27 -m pip install -r requirements_py27.txt
python -m pip install -r requirements_py37.txt

To start the application, you can use python3.7 to run the 'call_main.py' file, or directly use python2.7 to run the 'main.py' file in the python27 folder.

Once the GUI is started, please enter the socket port for this application (usually 5000), Nao's ip address and port (by press the chect button of Nao once), and your ChatGPT API key(applied in Openai website https://platform.openai.com/account/api-keys). Tick the Nao avaliable checkbox and press the initial building. Once the program says initialization done, you can press the start conmmunication button.
![alt text](https://github.com/Macreeeee/cognitive_robot_with_machine_learning/tree/main/src/recordings/pictures/gui_sample.jpg)
You can press the clear recording button whenever you find the recording window crowded.

Once the stop button is pressed, the conversation will end until Nao finish speaking its response.

Note: If you want to run the application without Nao, the function is within testing and may encounter errors.
