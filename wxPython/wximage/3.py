from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import wx
import numpy as np
import cv2
import sys

uni3 = cv2.imread('test.jpg')


class ImagePanel(wx.Panel):

    def __init__(self, parent, size, ID = wx.ID_ANY):

        wx.Panel.__init__(self, parent, ID, size = size)
        self.size = size
        bmp = wx.EmptyBitmap(self.size[0], self.size[1])
        self.stbmp = wx.StaticBitmap(self, bitmap = bmp)
        

    def redraw(self, img):

        assert(img.ndim == 3)
        assert(img.dtype == np.uint8)
        assert(img.shape[0] == self.size[1] and img.shape[1] == self.size[0])

        buf = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        bmp = wx.BitmapFromBuffer(img.shape[1], img.shape[0], buf)
        self.stbmp.SetBitmap(bmp)


class MyFrame(wx.Frame):

    def __init__(self, parent, ID, title):

        wx.Frame.__init__(self, parent, ID, title)

        self.ip = ImagePanel(self, size = (uni3.shape[1], uni3.shape[0]))

        self.button = wx.Button(self, wx.ID_ANY, 'Press Me')
        self.button.Bind(wx.EVT_BUTTON, self.buttonPressed)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.ip, border = 10, flag = wx.ALIGN_CENTER | wx.ALL)
        sizer.Add(self.button, border = 10, flag = wx.ALIGN_CENTER | wx.ALL)
        self.SetSizerAndFit(sizer)

        self.black = True
        

    def buttonPressed(self, event = None):

        img = uni3
        if not self.black:
            img = 255 - img
        self.ip.redraw(img)
        self.black = not self.black
        

if __name__ == '__main__':

    app = wx.App(False)
    frame = MyFrame(None, wx.ID_ANY, sys.argv[0])
    frame.Show()
    app.MainLoop()