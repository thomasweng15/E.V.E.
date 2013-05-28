E.V.E. Brain
------------

This directory contains the files necessary for E.V.E.'s artificial intelligence
capabilities as well as the main python files that control the program.

Artificial Intelligence:
*	standard.brn 				A compiled version of the standard AIML response database.

*	*.ses						Session information to supplement the AI's understanding
								of the current user. Stores information such as name and 
								personality of the current user.


Python Files:
*	command.py 					Contains the CommandAndControl class which loads the 
								brain, processes input from julius to recognize activation commands, and opens listening for voice commands.

* 	listen.py 					Listens for voice input and converts it into text 
								before responding and executing commands.