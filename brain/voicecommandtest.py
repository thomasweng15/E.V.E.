#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Goals:
classify voice command type (which T_KEY or I_KEY)
classify syntax structure
extract query

Terms: 
T_KEY = transitive key
I_KEY = intransitive key
A_VERB = action verb

[T_KEY] = google, youtube, computer
[I_KEY] = news, screenshot

[A_VERB] = get, take, find, pull (up), bring (up), do
[PREP] = about, for, regarding, of, from, in, through, on

Syntax to support:
(1)… A_VERB I_KEY …
(2)… A_VERB T_KEY PREP (QUERY)
	ex:
	do a google search for macklemore
	get me a youtube video of cats
(3)… A_VERB (QUERY) PREP T_KEY …
	ex:
	find macklemore on google
	get cats from youtube
(4)… T_KEY (QUERY)
(5)... I_KEY …

corner cases: 
get a list of youtube videos of [query] -- this is a different command, this is search
	not covered in scope currently
“google search [query]” or “youtube search [query]” would include “search” in the query
this is not a natural way of saying the command, and is out of scope.
“open google and find [query]” would go straight to i_key under this algorithm
to solve this, we shouldn’t break out of loop, we should check type to the end and have a hierarchy like before.

"find me a video on youtube of cats"
	this fails

Steps:
Iterate through line once to determine command type and syntax structure
Iterate through line again and extract query given type and syntax.

a_verb 			t_key 		i_key
(1)	(2) (3)		(4)			(5)

0verriding command chain: T_KEY >  I_KEY > “”
'''

def main():
	t_keys = ['google', 'youtube', 'computer']
	action_verbs = ['get', 'find', 'do']
	prepositions = ['of', 'from', 'through', 'in', 'on']

	command_type = ""

	while 1:
		line = raw_input("input line: ")
		words = line.split()

		has_action_verb = False

		for word in words:
			if word in action_verbs:
				has_action_verb = True

			if word in t_keys:
				command_type = word
				print "COMMAND: " + word

				if has_action_verb:
					# if previous word is in prepositions, syntax 3
					if words[words.index(word) - 1] in prepositions:
						syntax = 3
					else:
						syntax = 2
				else:
					syntax = 4

				print "SYNTAX INDEX: " + str(syntax) 	

			# TODO add i_keys

			# TODO extract query

#def get_query():
	#query_list = words[words.index(word) + 1:]
	#query = ' '.join(query_list)
	#print "QUERY: " + query


if __name__ == "__main__":
	main()