import wx
import cv2
import numpy as np
from time import sleep


def cv2_image_to_wx_image(cv2_image):
    # type: (np.ndarray) -> wx.Image

    height, width = cv2_image.shape[:2]
    wx_image = wx.EmptyImage(width, height)  # type: wx.Image
    wx_image.SetData(cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB))
    return wx_image


def create_wx_bitmap_from_cv2_image(cv2_image):
    # type: (np.ndarray) -> wx.Bitmap

    height, width = cv2_image.shape[:2]
    #cv2_image_rgb = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)

    #return wx.BitmapFromBuffer(width, height, cv2_image_rgb)
    return wx.BitmapFromBuffer(width, height, cv2_image)


class MyFrame(wx.Frame):
    def __init__(self, parent, title, fps=15):
        wx.Frame.__init__(self, parent, title=title)
        
        video = np.load('video_face.npy')
        #cv2_image = cv2.imread(filename)  # type: np.ndarray
        bitmap = create_wx_bitmap_from_cv2_image(video[0])  # type: wx.Bitmap
        wx.StaticBitmap(self, -1, bitmap, (0, 0), self.GetClientSize())
        self.SetSize(bitmap.GetSize())

        #panel = wx.Panel(wx.Frame, wx.ID_ANY)
        self.button = wx.Button(self, wx.ID_ANY, 'Button')
        self.button.Bind(wx.EVT_BUTTON, self.click_button, self.button)

    def click_button(self, e):
        video = np.load('video_face.npy')
        #cv2_image = cv2.imread(filename)  # type: np.ndarray
        bitmap = create_wx_bitmap_from_cv2_image(video[20]) # type: wx.Bitmap
        wx.StaticBitmap(self, -1, bitmap, (0, 0), self.GetClientSize())
        self.SetSize(bitmap.GetSize())


if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame(None, "wxPython with OpenCV")
    frame.Show()
    app.MainLoop()