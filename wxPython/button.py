import wx
app = wx.App(False)
frame = wx.Frame(None, -1, 'Hello,World!' ,size=(300,100))

wx.Button(frame, wx.ID_OPEN, pos=(10,10) ,label="open")
wx.Button(frame, wx.ID_CLOSE, pos=(10,40))
wx.Button(frame, wx.ID_NEW, pos=(100,10))
wx.Button(frame, wx.ID_SAVE, pos=(100,40))
wx.Button(frame, wx.ID_HELP, pos=(200,40))

frame.Show()
app.MainLoop()