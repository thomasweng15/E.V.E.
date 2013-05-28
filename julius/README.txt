E.V.E. Julius Activation
------------------------

This directory contains the files necessary for E.V.E. to listen for activation commands
(e.g. "okay computer"). E.V.E. uses Julius Speech Recognition software to be always listening for activation commands. 

Julius relies on a .voca, .grammar, and .jconf file to build a recognition model:

*	eve.voca 				stores the vocabulary of the model by category 
							(denoted by the % signs) with phoneme spelling of each word.

*	eve.grammar 			stores the grammar of the model, with each line defining 
							a different grammatical structure.

*	julian.jconf 			stores configuration information for runnning Julius.


Running 'mkdfa eve' in the terminal in this directory builds the recognition model, 
creating all remaining unmentioned files. After running mkdfa, the command:

	julius -quiet -input mic -C ./julius/julian.jconf

can then be executed to test the recognition model (e.g., to test whether 'okay computer' is correctly recognized or not).

Julius help reference: http://www.voxforge.org/home/dev/acousticmodels/linux/create/htkjulius/tutorial/data-prep/step-1

--Thomas Weng