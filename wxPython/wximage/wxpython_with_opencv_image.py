import wx
import cv2
import numpy as np

# http://www.cs.cmu.edu/~chuck/lennapg/
filename = "test.jpg"


def cv2_image_to_wx_image(cv2_image):
    # type: (np.ndarray) -> wx.Image

    height, width = cv2_image.shape[:2]
    wx_image = wx.EmptyImage(width, height)  # type: wx.Image
    wx_image.SetData(cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB))
    return wx_image


def create_wx_bitmap_from_cv2_image(cv2_image):
    # type: (np.ndarray) -> wx.Bitmap

    height, width = cv2_image.shape[:2]
    cv2_image_rgb = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)

    return wx.BitmapFromBuffer(width, height, cv2_image_rgb)


class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)

        cv2_image = cv2.imread(filename)  # type: np.ndarray

        bitmap = create_wx_bitmap_from_cv2_image(cv2_image)  # type: wx.Bitmap

        wx.StaticBitmap(self, -1, bitmap, (0, 0), self.GetClientSize())
        self.SetSize(bitmap.GetSize())


if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame(None, "wxPython with OpenCV")
    frame.Show()
    app.MainLoop()