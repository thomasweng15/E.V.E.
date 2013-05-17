#!/bin/bash
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "++++++++++++++++++++  Welcome to HAL-E  ++++++++++++++++++++"
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "+                                                          +"
echo "+                Say 'Okay HAL-E' to start!                +"
echo "+                                                          +"
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
padsp julius -quiet -input mic -C ./julius/julian.jconf 2>/dev/null | python command.py
