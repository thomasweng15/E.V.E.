HAL-E Julius Activation
------------------------

This directory contains the files necessary for HAL-E to listen for activation commands, e.g. "HAL-E Listen." HAL-E uses Julius Speech Recognition software in order to always listen for the activation command. 

Julius relies relies on a .voca, .grammar, and .jconf file to build a recognition model. 
*	hal-e.voca stores the vocabulary of the model by category (denoted by the % signs) with phoneme spelling of each word.
*	hal-e.grammar stores the syntax of the model, with each line defining a different syntactical structure.
*	hulian.jconf stores configuration information for runnning Julius.

Running 'mkdfa hal-e' in the terminal in this directory creates the remaining files and builds the recognition model. After running mkdfa, the command:

	julius -quiet -input mic -C ./julius/julian.jconf 2>/dev/null

can then be executed to test the recognition model (e.g., to test whether 'OKAY HAL-E' is correctly recognized or not).

--Thomas Weng (5/16/2013)