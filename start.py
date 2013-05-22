#!/usr/bin/python
# -*- coding: utf-8 -*-

#os.system("padsp julius -quiet -input mic -C ./julius/julian.jconf 2>/dev/null | python eve.py")
    

import os
import wx

		


	

class MyPanel(wx.Panel):
    
    def __init__(self, *args, **kw):
        super(MyPanel, self).__init__(*args, **kw) 

        self.Bind(wx.EVT_BUTTON, self.OnButtonClicked)

    def OnButtonClicked(self, e):
        
        print 'event reached panel class'
        e.Skip()


class startButton(wx.Button):
    
    def __init__(self, *args, **kw):
        super(startButton, self).__init__(*args, **kw) 

        self.Bind(wx.EVT_BUTTON, self.OnButtonClicked)

    def OnButtonClicked(self, e):
        
        print 'event reached button class'
        e.Skip()
        

class Window(wx.Frame):
           
    def __init__(self, *args, **kw):
        super(Window, self).__init__(*args, **kw) 
        
        self.InitUI()
        
        
    def InitUI(self):
    	menubar = wx.MenuBar()
    	fileMenu = wx.Menu()
    	fitem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
    	menubar.Append(fileMenu, '&File')
    	self.SetMenuBar(menubar)

    	self.Bind(wx.EVT_MENU, self.OnQuit, fitem)

    	mpnl = MyPanel(self)

    	startButton(mpnl, label='Start', pos=(15, 15))

    	self.Bind(wx.EVT_BUTTON, self.OnButtonClicked)

    	self.SetTitle('Propagate event')
    	self.Centre()
    	self.Show(True)  

    def OnButtonClicked(self, e):
        
        print 'event reached frame class'
        os.system("padsp julius -quiet -input mic -C ./julius/julian.jconf 2>/dev/null | python eve.py")
        e.Skip()

    def OnQuit(self, e):
		self.Close()


def main():
    print "Loading..."

    app = wx.App()
    Window(None)
    app.MainLoop()    


if __name__ == '__main__':
    main() 