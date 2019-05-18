import wx
import cv2
import numpy as np
from time import sleep
import wx.media
import os

def create_wx_bitmap_from_cv2_image(cv2_image):
    height, width = cv2_image.shape[:2]
    return wx.BitmapFromBuffer(width, height, cv2_image)

def scale_bitmap(bitmap, width, height):
    image = wx.ImageFromBitmap(bitmap)
    image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    result = wx.BitmapFromImage(image)
    return result

class MyFrame(wx.Frame):
    def __init__(self, parent, title, fps=25):
        wx.Frame.__init__(self, parent, title=title, size=(800, 500))
        self.fps = fps
        
        video = np.load('video_face.npy')
        self.frame = video
        self.bmp = create_wx_bitmap_from_cv2_image(self.frame[0])
        self.bmp = scale_bitmap(self.bmp, 400, 350)
        text = np.load('result_split.npy')
        self.subtitle = text
        self.inc = max(len(self.frame)/(len(self.subtitle)+1), 0.01)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.panel_txt = wx.Panel(self, -1, pos=(350, 350), size=(400, 170))
        self.panel_frame = wx.Panel(self, -1, pos=(350, 50), size=(400, 350))

        self.panel_button = wx.Panel(self, -1, pos=(20, 50), size=(300, 500))
        self.button1 = wx.Button(self.panel_button, wx.ID_ANY, 'Load', size=(100, 50))
        self.button1.Bind(wx.EVT_BUTTON, self.onLoadFile, self.button1)
        self.button2 = wx.Button(self.panel_button, wx.ID_ANY, 'Musuic', size=(100, 50))
        self.button2.Bind(wx.EVT_BUTTON, self.onLoadFile, self.button2)
        self.button3 = wx.Button(self.panel_button, wx.ID_ANY, 'Radio', size=(100, 50))
        self.button3.Bind(wx.EVT_BUTTON, self.onLoadFile, self.button3)

        self.button4 = wx.Button(self.panel_button, wx.ID_ANY, 'Play', size=(100, 50))
        self.button4.Bind(wx.EVT_BUTTON, self.onLoadFile, self.button4)
        self.button5 = wx.Button(self.panel_button, wx.ID_ANY, 'Pose', size=(100, 50))
        self.button5.Bind(wx.EVT_BUTTON, self.click_button_stop, self.button5)
        self.button6 = wx.Button(self.panel_button, wx.ID_ANY, 'Stop', size=(100, 50))
        self.button6.Bind(wx.EVT_BUTTON, self.click_button_start, self.button6)

        self.button7 = wx.Button(self.panel_button, wx.ID_ANY, 'Lipreading', size=(100, 50))
        self.button7.Bind(wx.EVT_BUTTON, self.onLoadFile, self.button7)
        self.button8 = wx.Button(self.panel_button, wx.ID_ANY, 'Lipreading', size=(100, 50))
        self.button8.Bind(wx.EVT_BUTTON, self.click_button_stop, self.button8)
        self.button9 = wx.Button(self.panel_button, wx.ID_ANY, 'Lipreading', size=(100, 50))
        self.button9.Bind(wx.EVT_BUTTON, self.click_button_start, self.button9)

        self.layout = wx.BoxSizer(wx.HORIZONTAL)

        self.layout_button = wx.BoxSizer(wx.VERTICAL)
        
        self.layout_button1 = wx.BoxSizer(wx.HORIZONTAL)
        #self.layout_button = wx.GridSizer(3, 1, 50, 10)
        self.layout_button1.Add(self.button1, proportion=1)
        self.layout_button1.Add(self.button2, proportion=1)
        self.layout_button1.Add(self.button3, proportion=1)
        self.layout_button.Add(self.layout_button1,flag=wx.EXPAND)
        
        self.layout_button2 = wx.BoxSizer(wx.HORIZONTAL)
        #self.layout_button = wx.GridSizer(3, 1, 50, 10)
        self.layout_button2.Add(self.button4, proportion=1)
        self.layout_button2.Add(self.button5, proportion=1)
        self.layout_button2.Add(self.button6, proportion=1)
        self.layout_button.Add(self.layout_button2,flag=wx.EXPAND)

        self.layout_button3 = wx.BoxSizer(wx.HORIZONTAL)
        #self.layout_button = wx.GridSizer(3, 1, 50, 10)
        self.layout_button3.Add(self.button7, proportion=1)
        self.layout_button3.Add(self.button8, proportion=1)
        self.layout_button3.Add(self.button9, proportion=1)
        self.layout_button.Add(self.layout_button3,flag=wx.EXPAND)

        self.layout.Add(self.layout_button,flag=wx.EXPAND)
        self.SetSizer(self.layout)

    
    def click_button_start(self, e):
        #self.panel_video.Destroy()
        try:
            self.panel_video.Destroy()
        except AttributeError:
            self.timer = wx.Timer(self)
            self.timer.Start(1000./self.fps)        
            self.i = 0
            self.Bind(wx.EVT_TIMER, self.NextFrame)
            raise       
        

    def click_button_stop(self, e):      
        self.timer.Stop()

    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self.panel_frame)
        dc.DrawBitmap(self.bmp, 0, 0)
        #self.main_frame = wx.StaticBitmap(self, wx.ID_ANY, self.bmp)

        self.layout_frame = wx.BoxSizer(wx.VERTICAL)
        #self.layout_frame.Add(self.main_frame)

        sub = " ".join(self.subtitle[:int(0/self.inc)])
        self.txt = wx.StaticText(self.panel_txt, -1, sub,(0,70))
        #self.txt.SetBackgroundColour('#000000')
        self.font = wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.txt.SetFont(self.font)

    def NextFrame(self, event):
        if self.i < 75:
            self.bmp = create_wx_bitmap_from_cv2_image(self.frame[self.i-1])
            self.bmp = scale_bitmap(self.bmp, 400, 350)
            #self.bmp.CopyFromBuffer(self.frame[self.i-1])
            sub = " ".join(self.subtitle[:int(self.i/self.inc)])
            print(self.subtitle[:int(self.i/self.inc)])
            self.txt = wx.StaticText(self.panel_txt, -1, sub,(0,70))
            self.txt.SetFont(self.font)
            self.layout_frame.Add(self.txt)
            self.layout.Add(self.layout_frame)
            #print(sub)
            self.Refresh()
            print(self.i)
            self.i = self.i + 1
        else:
            self.i = 0
            #self.layout.Remove(self.layout_frame)
            #self.txt.Destroy()
            self.layout.Layout()
            #self.Refresh()
            #self.layout_frame.Layout()

    def onLoadFile(self, evt):
        self.panel_video = wx.Panel(self, -1, pos=(350, 50), size=(400, 350))

        try:
            self.mc = wx.media.MediaCtrl(self.panel_video, style=wx.SIMPLE_BORDER)
        except NotImplementedError:
            self.panel_video.Destroy()
            raise

        dlg = wx.FileDialog(self, message="Choose a media file",
                            defaultDir=os.getcwd(), defaultFile="",
                            style=wx.OPEN | wx.CHANGE_DIR )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.doLoadFile(path)
        dlg.Destroy()
        
    def doLoadFile(self, path):
        if not self.mc.Load(path):
            wx.MessageBox("Unable to load %s: Unsupported format?" % path, "ERROR", wx.ICON_ERROR | wx.OK)
        else:
            folder, filename = os.path.split(path)
            #self.st_file.SetLabel('%s' % filename)
            self.mc.SetBestFittingSize()
            self.GetSizer().Layout()
            #self.slider.SetRange(0, self.mc.Length())
            self.mc.Play()
        
    def onPlay(self, evt):
        self.mc.Play()
    
    def onPause(self, evt):
        self.mc.Pause()
    
    def onStop(self, evt):
        self.mc.Stop()



if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame(None, "LipNet")
    frame.Show()
    app.MainLoop()       
        