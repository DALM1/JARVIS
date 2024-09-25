JARVIS Automation: Hand Gesture and Voice-Controlled Automation System

This project implements a hand gesture recognition system powered by MediaPipe and OpenCV for automating tasks on macOS. It recognizes specific hand gestures and voice commands to control applications like VS Code, ChatGPT, and system actions such as sleep mode or shutting down the recognition program. This project also integrates OpenAI’s GPT for intelligent conversation and task execution.

Features

1. Open VS Code with a Specific Project

	•	Gesture: One closed fist (right hand).
	•	Action: Opens VS Code with the project located at /Users/dalm1/Desktop/Reroll/Progra/JARVIS.

2. Close All Open VS Code Windows

	•	Gesture: Both hands in a closed fist.
	•	Action: Closes all currently open VS Code windows.

3. Put the Computer to Sleep

	•	Gesture: Open hand gesture (like the “paper” sign in rock-paper-scissors, excluding thumb).
	•	Action: Puts the computer into sleep mode.

4. Open ChatGPT Application via Voice Command

	•	Voice Command: Say “GPT ouverture”.
	•	Action: Opens the ChatGPT application on macOS.

5. Shut Down the Gesture Recognition Program

	•	Option 1: Gesture:
	•	Gesture: Horizontal scissors gesture (index and middle fingers extended, other fingers folded) or gun gesture (thumb and index extended).
	•	Action: Exits and shuts down the hand gesture recognition program.
	•	Option 2: Voice Command:
	•	Command: Say “Jarvis fermeture”.
	•	Action: Exits and shuts down the hand gesture recognition program.

6. Voice Interaction with GPT

	•	Gesture: Open hand gesture (like the “paper” sign in rock-paper-scissors, excluding thumb).
	•	Action: Initiates a conversation with GPT. The program listens to the user’s input and provides a response using OpenAI’s GPT model.

Voice Commands Overview

	•	“GPT ouverture”: Opens the ChatGPT application on macOS.
	•	“Jarvis fermeture”: Closes the gesture recognition program.
	•	Any question to GPT: Interacts with GPT to get answers on various topics.

Requirements

	•	Python: Ensure Python 3.8 or later is installed.
	•	OpenCV: For real-time video capturing and processing.
	•	MediaPipe: For hand gesture detection.
	•	OpenAI API: For interacting with GPT. Make sure you have your API key set in the environment variables.


  License

  This project is open-source and available under the MIT License.

  You can add more sections as needed, like troubleshooting or known issues, depending on your project development.
