#!/usr/bin/python
# -*- coding: utf-8 -*-

from brain.command import CommandAndControl

import subprocess
import sys
import wx
import time
import threading

ID_MENU_QUIT = wx.NewId()
ID_MENU_HELP = wx.NewId()
ID_MENU_ABOUT = wx.NewId()

def main(inputMode):
	print "Loading..."

	cmd = CommandAndControl()

	# TODO catch padsp error instead of using padsp by default
	proc = subprocess.Popen(['padsp', 'julius', '-quiet', 
			'-input', 'mic', 
			'-C', './julius/julian.jconf'], 
			stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

	if inputMode == "voice":
		while 1: 
			juliusInp = proc.stdout.readline()
			cmd.get_input(juliusInp)
			sys.stdout.flush()
	else:
		while 1: 
			inp = "sentence1: <s> " + raw_input("> ") + " </s>"
			cmd.get_input(inp)

def print_help():
	print "Usage: python eve.py [options]"
	print "Options:"
	print "  -x				  Open E.V.E. in terminal; no GUI."
	print "  -s               Read from stdin instead of using julius."
	print "  -help            Print this message and exit."
	print
	print "Please report bugs to thomasweng15 on github.com"

class Thread(threading.Thread):
    def run (self):
        print "Loading..."

        self.exit = False
        self.is_listening = True

        # this next line with textctrl is causing a segfault
        cmd = CommandAndControl()

        while self.is_listening:
            proc = subprocess.Popen(['padsp', 'julius', '-quiet', 
                '-input', 'mic', 
                '-C', './julius/julian.jconf'], 
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            while True:
                if self.exit:
                    break
                juliusInp = proc.stdout.readline()
                cmd.get_input(juliusInp)
                sys.stdout.flush()

class Window(wx.Frame):
    def __init__(self, *args, **kw):
        super(Window, self).__init__(*args, **kw) 
        self.panel = wx.Panel(self)

        # create menu bar
        self.create_menu()

        # create sizers
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        control_sizer = self.build_controls()
        output_sizer = self.build_output()

        main_sizer.Add(control_sizer, 0, wx.TOP|wx.LEFT, 5)
        main_sizer.Add(output_sizer, 0, wx.TOP, 5)
        self.panel.SetSizerAndFit(main_sizer)

        # initialize threading?
        self.is_listening = False
        self.exit = False
        
        self.thread = Thread()
        
        self.SetSize((805, 500))
        self.Centre()
        self.Show()

    def on_btn1(self, e):
        if self.is_listening is False:
            self.is_listening = True
            self.thread.start() # TODO might need to pass listening flag and stuff

    def build_output(self):
        output_sizer = wx.BoxSizer(wx.HORIZONTAL)

        text_ctrl = wx.TextCtrl(self.panel, 
            size = (800, 300), # TODO make this variable
            style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)

        #sys.stdout = text_ctrl # ERROR causing the segfault

        output_sizer.Add(text_ctrl, 0, wx.LEFT, 3)

        return output_sizer

    def build_controls(self):
        control_sizer = wx.BoxSizer(wx.HORIZONTAL)

        btn1 = wx.Button(self.panel, label='Start!', size=(70, 30))
        control_sizer.Add(btn1, 0, wx.LEFT, 3)

        btn1.Bind(wx.EVT_BUTTON, self.on_btn1)

        return control_sizer

    def create_menu(self):
        menubar = wx.MenuBar()

        file_menu = wx.Menu()
        file_menu.Append(ID_MENU_QUIT, 'Quit')        

        help_menu = wx.Menu()
        help_menu.Append(ID_MENU_HELP, 'Help')
        help_menu.Append(ID_MENU_ABOUT, 'About')

        menubar.Append(file_menu, '&File')
        menubar.Append(help_menu, '&Help')

        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.on_quit, id=ID_MENU_QUIT)
        self.Bind(wx.EVT_MENU, self.on_help, id=ID_MENU_HELP)
        self.Bind(wx.EVT_MENU, self.on_about, id=ID_MENU_ABOUT)

    def on_quit(self, e):
        self.Close()

    def on_help(self, e):
        helpBox = wx.MessageDialog(None, 'Help Info', 'Help', 
            wx.OK | wx.ICON_INFORMATION)
        helpBox.ShowModal()

    def on_about(self, e):
        abtBox = wx.MessageDialog(None, 'About Infor', 'About', 
            wx.OK | wx.ICON_INFORMATION)
        abtBox.ShowModal()

if __name__ == '__main__':
	if len(sys.argv) == 1:
		app = wx.App()
		Window(None, title='E.V.E.')
		app.MainLoop()

	elif len(sys.argv) == 2 and sys.argv[1] == "-x":
		main("voice")
		
	elif len(sys.argv) == 2 and sys.argv[1] == "-s":
		print "Standard input mode."
		main("cmdline")

	elif len(sys.argv) == 2 and sys.argv[1] == "-help":
		print_help()
		sys.exit(1)

	else:
		sys.exit('Error: Invalid arguments. Use the \'-help\' option to learn more.')
	
