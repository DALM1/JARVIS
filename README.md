Hand Gesture Recognition for JARVIS Automation

This project is a hand gesture recognition system that uses MediaPipe and OpenCV to automate tasks on macOS based on hand gestures. The system recognizes several gestures, each mapped to specific commands, such as launching applications, closing windows, putting the computer to sleep, and shutting down the gesture recognition program.

Features

1. Open VS Code with a Specific Project

	•	Gesture: One closed fist (right hand)
	•	Action: Opens VS Code with the project located at /Users/dalm1/Desktop/Reroll/Progra/JARVIS.

2. Close All Open VS Code Windows

	•	Gesture: Both hands in a closed fist
	•	Action: Closes all currently open VS Code windows.

3. Shut Down the Gesture Recognition Program

	•	Gesture: Horizontal scissors gesture (index and middle finger extended, other fingers folded)
	•	Action: Exits and shuts down the hand gesture recognition program.

4. Put the Computer to Sleep

	•	Gesture: Open hand gesture (like the “paper” sign in rock-paper-scissors)
	•	Action: Puts the computer into sleep mode.


5.  Customization

	•	The script currently uses hardcoded paths and commands for macOS. You can customize paths (e.g., for the VS Code project) and gestures according to your needs.
	•	The thresholds for gesture recognition can be adjusted by modifying the tolerances in the is_fist, is_scissors, and is_paper functions.

  License

  This project is open-source and available under the MIT License.

  You can add more sections as needed, like troubleshooting or known issues, depending on your project development.
