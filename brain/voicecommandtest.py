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
[PREP] = about, for, regarding, of, from, in

through

Syntax to support:
(1)… A_VERB I_KEY …
(2)… A_VERB T_KEY PREP (QUERY)
(3)… A_VERB (QUERY) PREP T_KEY …
(4)… T_KEY (QUERY)
(5)... I_KEY …

corner cases: 
get a list of youtube videos of [query] -- this is a different command, this is search
	not covered in scope currently
“google search [query]” or “youtube search [query]” would include “search” in the query
this is not a natural way of saying the command, and is out of scope.
“open google and find [query]” would go straight to i_key under this algorithm
to solve this, we shouldn’t break out of loop, we should check type to the end and have a hierarchy like before.

Steps:
Iterate through line once to determine command type and syntax structure
Iterate through line again and extract query given type and syntax.

a_verb 			t_key 		i_key
(1)	(2) (3)		(4)			(5)

0verriding command chain: T_KEY >  I_KEY > “”
'''

def main():
	# Initialize array of transitive keys
	t_key = ['google', 'youtube', 'computer']

	while 1:
		line = raw_input("input line: ")
		words = line.split()

		for word in words:
			if word in t_key:
				print "COMMAND: " + word
				query_list = words[words.index(word) + 1:]
				query = ' '.join(query_list)
				print "QUERY: " + query


if __name__ == "__main__":
	main()