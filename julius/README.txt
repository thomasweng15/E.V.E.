EVE Julius Activation
----------------------

This directory contains the files necessary for EVE to listen for activation commands, e.g. "okay computer." EVE uses Julius Speech Recognition software in order to always listen for the activation command. 

Julius relies relies on a .voca, .grammar, and .jconf file to build a recognition model. 
*	eve.voca stores the vocabulary of the model by category (denoted by the % signs) with phoneme spelling of each word.
*	eve.grammar stores the syntax of the model, with each line defining a different syntactical structure.
*	julian.jconf stores configuration information for runnning Julius.

Running 'mkdfa eve' in the terminal in this directory creates the remaining files and builds the recognition model. After running mkdfa, the command:

	julius -quiet -input mic -C ./julius/julian.jconf 2>/dev/null

can then be executed to test the recognition model (e.g., to test whether 'okay computer' is correctly recognized or not).

Julius help reference: http://www.voxforge.org/home/dev/acousticmodels/linux/create/htkjulius/tutorial/data-prep/step-1

--Thomas Weng (5/16/2013)