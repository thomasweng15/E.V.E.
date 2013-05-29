#!/usr/bin/python
# -*- coding: utf-8 -*-

from brain.command import CommandAndControl

import subprocess
import sys
import wx

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


class Window(wx.Frame):
    def __init__(self, *args, **kw):
        super(Window, self).__init__(*args, **kw) 
       
        self.InitUI()
        
    def InitUI(self):
    	self.CreateMenuBar()

    	self.SetMinSize((100, 100)) #TODO update this

    	panel = wx.Panel(self)

    	vbox = wx.BoxSizer(wx.VERTICAL)

    	hbox1 = wx.BoxSizer(wx.HORIZONTAL)
    	btn1 = wx.Button(panel, label='Start!', size=(70, 30))

    	hbox1.Add(btn1, flag=wx.EXPAND | wx.TOP | wx.LEFT, border=10)
    	# TODO add more buttons such as Mute or Preferences
    	vbox.Add(hbox1, flag=wx.EXPAND, border=10)

    	vbox.Add((-1, 10))

    	ln1 = wx.StaticLine(self, pos=(0, 50), size=(300,1))

    	panel.SetSizerAndFit(vbox)

    	self.SetSize((300,300))
    	self.Centre()
    	self.Show(True)  

    def CreateMenuBar(self):
    	mb = wx.MenuBar()

    	fMenu = wx.Menu()
    	fMenu.Append(ID_MENU_QUIT, 'Quit')
    	
    	hMenu = wx.Menu()
    	hMenu.Append(ID_MENU_HELP, 'Help')
    	hMenu.Append(ID_MENU_ABOUT, 'About')


    	mb.Append(fMenu, '&File')
    	mb.Append(hMenu, '&Help')
    	self.SetMenuBar(mb)

    	self.Bind(wx.EVT_MENU, self.OnQuit, id=ID_MENU_QUIT)
        self.Bind(wx.EVT_MENU, self.OnHelp, id=ID_MENU_HELP)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=ID_MENU_ABOUT) 

    def OnQuit(self, e):
    	self.Close()

    def OnHelp(self, e):
    	helpBox = wx.MessageDialog(None, 'Help Info', 'Help', 
    		wx.OK | wx.ICON_INFORMATION)
    	helpBox.ShowModal()

    def OnAbout(self, e):
    	aboutBox = wx.MessageDialog(None, 'Help Info', 'Help', 
    		wx.OK | wx.ICON_INFORMATION)
    	aboutBox.ShowModal()


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
	
