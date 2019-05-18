#!/usr/bin/env python
#coding:utf-8
 
import wx
 
class MyWindow(wx.Frame):
    def __init__(self, parent=None, id=-1, title=None):
        wx.Frame.__init__(self, parent, id, title)
        self.panel = wx.Panel(self, size=(300, 200))
        self.panel.SetBackgroundColour('WHITE')
        font = wx.Font(60, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.stext = wx.StaticText(self.panel)
        self.stext.SetFont(font)
        self.stext.SetWindowStyle(wx.BORDER_SIMPLE)
        self.stext.CenterOnParent()
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.Fit()
        self.counter = 20
        self.timer.Start(500)
 
    def OnTimer(self, event):
        self.stext.SetLabel("%02d" % self.counter)
        self.stext.CenterOnParent()
        if self.counter == 0:
            self.timer.Stop()
        else:
            self.counter -= 1
 
if __name__ == '__main__':
    app = wx.PySimpleApp()
    w = MyWindow(title='wx-timer')
    w.Center()
    w.Show()
    app.MainLoop()