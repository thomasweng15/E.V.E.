#!/bin/bash
padsp julius -quiet -input mic -C ./julius/julian.jconf 2>/dev/null | python command.py
