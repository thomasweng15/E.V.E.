#!/bin/bash
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "+++++++++++++++++++++++++  Welcome to HAL-E  +++++++++++++++++++++++++"
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "+                                                                    +"
echo "+                    Say 'HAL-E Listen' to start!                    +"
echo "+                                                                    +"
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
padsp julius -quiet -input mic -C ./julius/julian.jconf 2>/dev/null | python ./hal-e/hal-e.py
