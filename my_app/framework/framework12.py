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

        # Panel
        self.panel_txt = wx.Panel(self, -1, pos=(350, 350), size=(400, 260))
        self.panel_frame = wx.Panel(self, -1, pos=(350, 50), size=(400, 350))
        self.panel_dummy = wx.Panel(self, -1, pos=(350, 50), size=(400, 450))
        self.panel_button = wx.Panel(self, -1, pos=(20, 50), size=(300, 500))
        self.panel_music = wx.Panel(self, -1, pos=(0, 0), size=(10, 10))
       
        # Button
        self.button1 = wx.Button(self.panel_button, wx.ID_ANY, 'Loading', size=(100, 50))
        self.button1.Bind(wx.EVT_BUTTON, self.button_onLoadFile, self.button1)
        self.button2 = wx.Button(self.panel_button, wx.ID_ANY, 'Music', size=(100, 50))
        self.button2.Bind(wx.EVT_BUTTON, self.button_Music, self.button2)
        self.button3 = wx.Button(self.panel_button, wx.ID_ANY, 'Radio', size=(100, 50))
        self.button3.Bind(wx.EVT_BUTTON, self.button_Music, self.button3)
        self.button4 = wx.Button(self.panel_button, wx.ID_ANY, 'LipNet', size=(100, 50))
        self.button4.Bind(wx.EVT_BUTTON, self.button_lipnet, self.button4)
        self.button5 = wx.Button(self.panel_button, wx.ID_ANY, 'Lipreading', size=(100, 50))
        self.button5.Bind(wx.EVT_BUTTON, self.button_lipreading, self.button5)

        self.button6 = wx.Button(self.panel_button, wx.ID_ANY, 'Play', size=(100, 50))
        self.button6.Bind(wx.EVT_BUTTON, self.button_start, self.button6)
        self.button7 = wx.Button(self.panel_button, wx.ID_ANY, 'Pose', size=(100, 50))
        self.button7.Bind(wx.EVT_BUTTON, self.button_pose, self.button7)
        self.button8 = wx.Button(self.panel_button, wx.ID_ANY, 'Stop', size=(100, 50))
        self.button8.Bind(wx.EVT_BUTTON, self.button_stop, self.button8)

        self.button9 = wx.Button(self.panel_button, wx.ID_ANY, '1', size=(100, 50))
        self.button9.Bind(wx.EVT_BUTTON, self.button_sound_effect_1, self.button9)
        self.button10 = wx.Button(self.panel_button, wx.ID_ANY, '2', size=(100, 50))
        self.button10.Bind(wx.EVT_BUTTON, self.button_sound_effect_2, self.button10)
        self.button11 = wx.Button(self.panel_button, wx.ID_ANY, '3', size=(100, 50))
        self.button11.Bind(wx.EVT_BUTTON, self.button_sound_effect_3, self.button11)
        self.ef_1 = 0
        self.ef_2 = 0
        self.ef_3 = 0

        # Font
        font_button = wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.button1.SetFont(font_button)
        self.button2.SetFont(font_button)
        self.button3.SetFont(font_button)
        self.button4.SetFont(font_button)
        self.button5.SetFont(font_button)
        self.button6.SetFont(font_button)
        self.button7.SetFont(font_button)
        self.button8.SetFont(font_button)
        self.button9.SetFont(font_button)
        self.button10.SetFont(font_button)
        self.button11.SetFont(font_button)
        
        # File
        self.k = 0
        self.filename = '1'

        # Layout
        self.layout = wx.BoxSizer(wx.HORIZONTAL)

        # Layout Button
        self.layout_button = wx.BoxSizer(wx.VERTICAL)
        
        # Layout Button1
        self.layout_button1 = wx.BoxSizer(wx.VERTICAL)
        self.layout_button1.Add(self.button1, proportion=1,flag=wx.EXPAND)
        
        self.layout_button_music = wx.BoxSizer(wx.HORIZONTAL)
        self.layout_button_music.Add(self.button2, proportion=1,flag=wx.EXPAND)
        self.layout_button_music.Add(self.button3, proportion=1,flag=wx.EXPAND)
        self.layout_button1.Add(self.layout_button_music, proportion=1,flag=wx.EXPAND)

        self.layout_button1.Add(self.button4, proportion=1,flag=wx.EXPAND)
        self.layout_button1.Add(self.button5, proportion=1,flag=wx.EXPAND)
        self.layout_button.Add(self.layout_button1,flag=wx.EXPAND)
        
        # Layout Button2
        self.layout_button2 = wx.BoxSizer(wx.HORIZONTAL)
        self.layout_button2.Add(self.button6, proportion=1,flag=wx.EXPAND)
        self.layout_button2.Add(self.button7, proportion=1,flag=wx.EXPAND)
        self.layout_button2.Add(self.button8, proportion=1,flag=wx.EXPAND)
        self.layout_button.Add(wx.Size(0, 30))
        self.layout_button.Add(self.layout_button2,flag=wx.EXPAND)

        # Layout Sound effect
        self.layout_effect = wx.BoxSizer(wx.HORIZONTAL)
        self.layout_effect.Add(self.button9, proportion=1,flag=wx.EXPAND)
        self.layout_effect.Add(self.button10, proportion=1,flag=wx.EXPAND)
        self.layout_effect.Add(self.button11, proportion=1,flag=wx.EXPAND)
        self.layout_button.Add(wx.Size(0, 30))
        self.layout_button.Add(self.layout_effect,flag=wx.EXPAND)

        self.layout.Add(self.layout_button,flag=wx.EXPAND)
        self.SetSizer(self.layout)


    def button_onLoadFile(self, evt):
        if self.k == 0 or self.k == 2:
            self.panel_dummy.Destroy()
        
        self.panel_dummy = wx.Panel(self, -1, pos=(350, 50), size=(400, 450))
        self.panel_video = wx.Panel(self, -1, pos=(350, 50), size=(400, 350))
        self.k = 2

        cu_path = os.getcwd() 
        os.chdir('./video')

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
        os.chdir(cu_path)   
        
    def doLoadFile(self, path):
        if not self.mc.Load(path):
            wx.MessageBox("Unable to load %s: Unsupported format?" % path, "ERROR", wx.ICON_ERROR | wx.OK)
        else:
            folder, self.filename = os.path.split(path)
            #print(self.filename[0])
            self.mc.SetBestFittingSize()
            self.GetSizer().Layout()
            self.mc.Play()

    def button_Music(self, evt):      
        cu_path = os.getcwd() 
        os.chdir('./music')
        try:
            self.mc_music = wx.media.MediaCtrl(self.panel_music, style=wx.SIMPLE_BORDER)
        except NotImplementedError:
            self.panel_music.Destroy()
            raise
        dlg = wx.FileDialog(self, message="Choose a media file",
                            defaultDir=os.getcwd(), defaultFile="",
                            style=wx.OPEN | wx.CHANGE_DIR )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.doLoadFile_Music(path)
        dlg.Destroy()
        os.chdir(cu_path)   
        
    def doLoadFile_Music(self, path):
        if not self.mc_music.Load(path):
            wx.MessageBox("Unable to load %s: Unsupported format?" % path, "ERROR", wx.ICON_ERROR | wx.OK)
        else:
            folder, self.filename = os.path.split(path)
            #print(self.filename[0])
            self.mc_music.SetBestFittingSize()
            self.GetSizer().Layout()
            self.mc_music.Play()
   
    def button_lipnet(self, e):     
        file_shell = self.filename[0]
        #os.system('~/try/honnda/framework/script/' + file_shell + '.sh')
        c_path = os.getcwd() 
        os.chdir('/home/takashi/try/lipnet/LipNet')
        os.system('./my_predict2.sh evaluation/models/overlapped-weights368.h5 /home/takashi/try/honnda/framework/video/'+ file_shell + '.mp4')
        os.chdir(c_path)    

    def button_lipreading(self, e):
        if self.k == 0 or self.k == 2:
            self.panel_dummy.Destroy()
        if self.k == 2:
            self.panel_video.Destroy()
        self.k = 1        
        video = np.load('/home/takashi/try/honnda/framework/npy/'+ self.filename[0] +  '/video_face.npy')
        self.frame = video
        self.bmp = create_wx_bitmap_from_cv2_image(self.frame[0])
        self.bmp = scale_bitmap(self.bmp, 400, 350)
        text = np.load('/home/takashi/try/honnda/framework/npy/'+ self.filename[0] +  '/result_split.npy')
        self.subtitle = text
        self.inc = max(len(self.frame)/(len(self.subtitle)+1), 0.01)
        
        self.timer = wx.Timer(self)
        self.timer.Start(1000./self.fps)        
        self.i = 0
        self.Bind(wx.EVT_TIMER, self.NextFrame)

    def click_button_stop(self, e):      
        self.timer.Stop()

    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self.panel_frame)
        dc.DrawBitmap(self.bmp, 0, 0)
        
        self.layout_frame = wx.BoxSizer(wx.VERTICAL)

        sub = " ".join(self.subtitle[:int(0/self.inc)])
        self.txt = wx.StaticText(self.panel_txt, -1, sub,(0,70))
        self.font = wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.txt.SetFont(self.font)

    def NextFrame(self, event):
        if self.i < 75:
            self.bmp = create_wx_bitmap_from_cv2_image(self.frame[self.i-1])
            self.bmp = scale_bitmap(self.bmp, 400, 350)
            sub = " ".join(self.subtitle[:int(self.i/self.inc)])
            print(self.subtitle[:int(self.i/self.inc)])
            self.txt = wx.StaticText(self.panel_txt, -1, sub,(0,70))
            self.txt.SetFont(self.font)
            self.layout_frame.Add(self.txt)
            self.layout.Add(self.layout_frame)
            self.Refresh()
            print(self.i)
            self.i = self.i + 1
        else:
            self.i = 0
            self.layout.Layout()
     
    def button_start(self, e):
        if self.k == 1:
            self.timer = wx.Timer(self)
            self.timer.Start(1000./self.fps)        
            self.i = 0
            self.Bind(wx.EVT_TIMER, self.NextFrame)
        elif self.k == 2:
            self.mc.Play()

    def button_pose(self, e):
        if self.k == 1:
            self.timer.Stop()
            self.i = 0
            self.layout.Layout()
        elif self.k == 2:
            self.mc.Pause()

    def button_stop(self, e):
        if self.k == 1:
            self.timer.Stop()
            self.i = 0
            self.layout.Layout()
        elif self.k == 2:
            self.mc.Stop()

    def button_sound_effect_1(self, e):
        if self.ef_1 == 0:
            self.mc_ef_1 = wx.media.MediaCtrl(self.panel_music, style=wx.SIMPLE_BORDER)
            self.ef_1 = 1
        if self.ef_1 == 1:
            effect_path = '~/try/honnda/framework/sound_effect/car-blinker1.mp3'
            self.mc_ef_1.Load(effect_path)
            self.mc_ef_1.Play()
            self.ef_1 = 2
        elif self.ef_1 == 2:
            self.mc_ef_1.Stop()
            self.ef_1 = 1

    def button_sound_effect_2(self, e):
        if self.ef_2 == 0:
            self.mc_ef_2 = wx.media.MediaCtrl(self.panel_music, style=wx.SIMPLE_BORDER)
            self.ef_2 = 2
        if self.ef_2 == 1:
            effect_path = '~/try/honnda/framework/sound_effect/car-pass1.mp3'
            self.mc_ef_2.Load(effect_path)
            self.mc_ef_2.Play()
            self.ef_2 = 2
        elif self.ef_2 == 2:
            self.mc_ef_2.Stop()
            self.ef_2 = 1

    def button_sound_effect_3(self, e):
        if self.ef_3 == 0:
            self.mc_ef_3 = wx.media.MediaCtrl(self.panel_music, style=wx.SIMPLE_BORDER)
            self.ef_3 = 2
        if self.ef_3 == 1:
            effect_path = '~/try/honnda/framework/sound_effect/crossroad.mp3'
            self.mc_ef_3.Load(effect_path)
            self.mc_ef_3.Play()
            self.ef_3 = 2
        elif self.ef_3 == 2:
            self.mc_ef_3.Stop()
            self.ef_3 = 1


if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame(None, "LipNet")
    frame.Show()
    app.MainLoop()       
        