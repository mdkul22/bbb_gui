import wx
import sys
import random
from datetime import datetime

__author__ = "Mayunk Kulkarni"


class My_App(wx.App):
    """"Additional arg added i.e the sensor_dict which will be pulled regularly"""

    def __init__(self, sensor_dict):
        self.imp_dict = sensor_dict

    def OnInit(self):
        self.frame = MyFrame(None, self.imp_dict)
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

    def return_dict(self):
        return self.imp_dict

    def OnExit(self):
        print('Dying ...')


class MyFrame(wx.Frame):

    """"""

    def __init__(self, sensor_dict, image, parent=None, id=-1,
                 title='Generic Title', pos=wx.DefaultPosition):

        size = (800, 480)
        wx.Frame.__init__(self, parent, id, 'GUI', pos, size)

        self.sizer_h = wx.BoxSizer(wx.HORIZONTAL)

        self.panel0 = MyPanel(self, sensor_dict)
        self.sizer_h.Add(self.panel0, 1, wx.EXPAND)

        self.panel1 = MyPanel1(self, sensor_dict)
        self.sizer_h.Add(self.panel1, 1, wx.EXPAND)

        self.panel2 = MyPanel2(self, sensor_dict)
        self.sizer_h.Add(self.panel2, 1, wx.EXPAND)

        self.panel3 = MyPanel3(self, sensor_dict)
        self.sizer_h.Add(self.panel3, 1, wx.EXPAND)

        self.SetSizer(self.sizer_h)
        self.panel0.Hide()
        self.panel1.Hide()
        self.panel2.Hide()
        self.panel3.ShowYourself()

    def ShutDown(self):
        self.Destroy()

        # Add a panel so it looks correct on all platforms


class MyPanel(wx.Panel):

    """"""
    # --------BATTERY---------------------

    def __init__(self, imp_dict, parent, id=-1):
        """Constructor"""
        wx.Panel.__init__(self, parent, id, size=(800, 480))
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        # timers
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.updateV, self.timer)
        self.timer.Start(1000)

        self.timer1 = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.updateC, self.timer1)
        self.timer1.Start(1000)
        self.imp_dict = imp_dict
        # timers for Warning
        self.timerx = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.BatteryWarn, self.timerx)
        self.timerx.Start(100)

        self.timery = wx.Timer(self)
        self.timery.Start(1000)

        self.timerz = wx.Timer(self)
        self.timerz.Start(1000)

        title = wx.StaticText(self, -1, 'Battery')
        title.SetFont(wx.Font(24, wx.DEFAULT, wx.BOLD, wx.FONTWEIGHT_BOLD))
        title.SetForegroundColour('white')

        self.labelOne = wx.StaticText(
            self, -1, 'Battery (NE) Temperature  :   ' + str(self.btq1))
        self.labelTwo = wx.StaticText(
            self, -1, 'Battery (NW) Temperature  :   ' + str(self.btq2))
        self.labelThree = wx.StaticText(
            self, -1, 'Battery (SE) Temperature  :   ' + str(self.btq3))
        self.labelFour = wx.StaticText(
            self, -1, 'Battery (SW) Temperature  :   ' + str(self.btq4))
        self.labelFive = wx.StaticText(
            self, -1, 'Max. Discharge Current  :   ' + str(self.maxdisc))
        self.labelSix = wx.StaticText(
            self, -1, 'Min. Discharge Current  :   ' + str(self.mindisc))
        self.labelSeven = wx.StaticText(
            self, -1, 'Battery (SW) Temperature  :   ' + str(self.maxc))

        # the label describers
        self.labelOne.SetFont(
            wx.Font(20, wx.FONTFAMILY_DECORATIVE, wx.BOLD, wx.FONTWEIGHT_BOLD))
        self.labelOne.SetForegroundColour('white')
        self.labelTwo.SetFont(
            wx.Font(20, wx.FONTFAMILY_DECORATIVE, wx.BOLD, wx.FONTWEIGHT_BOLD))
        self.labelTwo.SetForegroundColour('white')
        self.labelThree.SetFont(
            wx.Font(20, wx.FONTFAMILY_DECORATIVE, wx.BOLD, wx.FONTWEIGHT_BOLD))
        self.labelThree.SetForegroundColour('white')
        self.labelFour.SetFont(
            wx.Font(20, wx.FONTFAMILY_DECORATIVE, wx.BOLD, wx.FONTWEIGHT_BOLD))
        self.labelFour.SetForegroundColour('white')
        self.labelFive.SetFont(
            wx.Font(20, wx.FONTFAMILY_DECORATIVE, wx.BOLD, wx.FONTWEIGHT_BOLD))
        self.labelFive.SetForegroundColour('white')
        self.labelSix.SetFont(
            wx.Font(20, wx.FONTFAMILY_DECORATIVE, wx.BOLD, wx.FONTWEIGHT_BOLD))
        self.labelSix.SetForegroundColour('white')
        self.labelSeven.SetFont(
            wx.Font(20, wx.FONTFAMILY_DECORATIVE, wx.BOLD, wx.FONTWEIGHT_BOLD))
        self.labelSeven.SetForegroundColour('white')

        # image button creation
        self.wbutton0 = wx.Button(
            self, -1, '-            M P P T               -')
        self.wbutton1 = wx.Button(
            self, -1, '-             B M S                -')
        self.wbutton2 = wx.Button(
            self, -1, '-           M O T O R              -')
        self.wbutton3 = wx.Button(
            self, -1, '-          G E N E R A L           -')

        imageFile = "mppt.png"
        image1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        MPPTBtn = wx.BitmapButton(self, id=-1, bitmap=image1,
                                  pos=(10, 20),
                                  size=(image1.GetWidth()+10,
                                        image1.GetHeight()+10))

        self.Bind(wx.EVT_BUTTON, self.OnMPPT, MPPTBtn)

        imageFile = "battery.png"
        image1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        BatteryBtn = wx.BitmapButton(self, id=-1, bitmap=image1,
                                     pos=(10, 20),
                                     size=(image1.GetWidth()+10,
                                           image1.GetHeight()+10))

        self.Bind(wx.EVT_BUTTON, None, BatteryBtn)

        imageFile = "motor.png"
        image1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        MotorBtn = wx.BitmapButton(self, id=-1, bitmap=image1,
                                   pos=(10, 20),
                                   size=(image1.GetWidth()+10,
                                         image1.GetHeight()+10))

        self.Bind(wx.EVT_BUTTON, self.OnMotor, MotorBtn)

        imageFile = "general.png"
        image1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        GenBtn = wx.BitmapButton(self, id=-1, bitmap=image1,
                                 pos=(10, 20),
                                 size=(image1.GetWidth()+10,
                                       image1.GetHeight()+10))

        self.Bind(wx.EVT_BUTTON, self.OnGeneral, GenBtn)

        # generating sizers
        topSizer = wx.BoxSizer(wx.VERTICAL)
        toolBtn = wx.BoxSizer(wx.HORIZONTAL)
        toolBtn_h = wx.BoxSizer(wx.VERTICAL)
        warnSizer = wx.BoxSizer(wx.HORIZONTAL)
        warnSizer_h = wx.BoxSizer(wx.VERTICAL)
        titleSizer = wx.BoxSizer(wx.HORIZONTAL)
        inputOneSizer = wx.BoxSizer(wx.HORIZONTAL)
        inputTwoSizer = wx.BoxSizer(wx.HORIZONTAL)
        inputThreeSizer = wx.BoxSizer(wx.HORIZONTAL)
        inputFourSizer = wx.BoxSizer(wx.HORIZONTAL)
        inputFiveSizer = wx.BoxSizer(wx.HORIZONTAL)
        inputSixSizer = wx.BoxSizer(wx.HORIZONTAL)
        inputSevenSizer = wx.BoxSizer(wx.HORIZONTAL)

        # adding toolbar
        toolBtn.Add(MPPTBtn, 0, wx.ALL, 5)
        toolBtn.Add(BatteryBtn, 0, wx.ALL, 5)
        toolBtn.Add(MotorBtn, 0, wx.ALL, 5)
        toolBtn.Add(GenBtn, 0, wx.ALL, 5)
        # adding them in a vertical sizer to center them completely
        toolBtn_h.Add(toolBtn, 0, wx.CENTER, 5)
        # same done for warnsizers
        warnSizer.Add(self.wbutton0, 0, wx.ALL, 5)
        warnSizer.Add(wx.StaticLine(self), 0, wx.ALL | wx.EXPAND, 5)
        warnSizer.Add(self.wbutton1, 0, wx.ALL, 5)
        warnSizer.Add(self.wbutton2, 0, wx.ALL, 5)
        warnSizer.Add(self.wbutton3, 0, wx.ALL, 5)

        warnSizer_h.Add(warnSizer, 0, wx.CENTER, 5)

        titleSizer.Add(title, 0, wx.ALL, 5)
        inputOneSizer.Add(self.labelOne, 0, wx.ALL, 5)
        inputTwoSizer.Add(self.labelTwo, 0, wx.ALL, 5)
        inputThreeSizer.Add(self.labelThree, 0, wx.ALL, 5)
        inputFourSizer.Add(self.labelFour, 0, wx.ALL, 5)
        inputFiveSizer.Add(self.labelFive, 0, wx.ALL, 5)
        inputSixSizer.Add(self.labelSix, 0, wx.ALL, 5)

        topSizer.Add(toolBtn_h, 0, wx.ALL | wx.EXPAND | wx.CENTER, 5)
        topSizer.Add(warnSizer_h, 0, wx.ALL | wx.EXPAND | wx.CENTER, 5)
        topSizer.Add(wx.StaticLine(self), 0, wx.ALL | wx.EXPAND, 5)
        topSizer.Add(titleSizer, 0, wx.CENTER)
        topSizer.Add(wx.StaticLine(self), 0, wx.ALL | wx.EXPAND, 5)
        topSizer.Add(inputOneSizer, 0, wx.ALL | wx.EXPAND, 5)
        topSizer.Add(inputTwoSizer, 0, wx.ALL | wx.EXPAND, 5)
        topSizer.Add(inputThreeSizer, 0, wx.ALL | wx.EXPAND, 5)
        topSizer.Add(inputFourSizer, 0, wx.ALL | wx.EXPAND, 5)
        topSizer.Add(inputFiveSizer, 0, wx.ALL | wx.EXPAND, 5)
        topSizer.Add(inputSixSizer, 0, wx.ALL | wx.EXPAND, 5)
        topSizer.Add(inputSevenSizer, 0, wx.ALL | wx.EXPAND, 5)
        topSizer.Add(wx.StaticLine(self), 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(topSizer)
        topSizer.Fit(self)

        self.Raise()
        self.SetPosition((0, 0))
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        # value declarations
        self.btq1 = 0
        self.btq2 = 0
        self.btq3 = 0
        self.btq4 = 0
        self.maxdisc = 0
        self.mindisc = 0
        self.maxc = 0

    def OnEraseBackground(self, evt):
        dc = evt.GetDC()

        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        start_image1 = wx.Image("solarcar.jpg")
        start_image1.Rescale(1310, 800)
        bmp = wx.BitmapFromImage(start_image1)
        dc.DrawBitmap(bmp, 0, 0)

    def closeProgram(self):
        self.Destroy()

    def BatteryWarn(self, event):
        """warner for all seven values"""
        if self.GetParent().panel0.IsShown():
            self.wbutton1.SetBackgroundColour('white')
            if self.btq1 > 65:
                self.labelOne.SetForegroundColour('red')
            else:
                self.labelOne.SetForegroundColour('white')
            if self.btq2 > 65:
                self.labelTwo.SetForegroundColour('red')
            else:
                self.labelTwo.SetForegroundColour('white')
            if self.btq3 > 65:
                self.labelThree.SetForegroundColour('red')
            else:
                self.labelThree.SetForegroundColour('white')
            if self.btq4 > 65:
                self.labelFour.SetForegroundColour('red')
            else:
                self.labelFour.SetForegroundColour('white')
            if self.maxdisc > 600:
                self.labelFive.SetForegroundColour('red')
            else:
                self.labelFive.SetForegroundColour('white')
            if self.mindisc < 500:
                self.labelSix.SetForegroundColour('red')
            else:
                self.labelSix.SetForegroundColour('white')
            if self.maxc > 600:
                self.labelTwo.SetForegroundColour('red')
            else:
                self.labelTwo.SetForegroundColour('white')

        elif (self.btq1, self.btq2, self.btq2, self.btq4) > 65 or (self.maxc, self.maxdisc) > 600 or self.mindisc < 500:
            self.wbutton1.SetBackgroundColour('red')
            self.GetParent().panel1.wbutton1.SetBackgroundColour('red')
            self.GetParent().panel2.wbutton1.SetBackgroundColour('red')
            self.GetParent().panel3.wbutton1.SetBackgroundColour('red')

    def updatetq1(self, event):
        """battery NE quadrant temperature"""
        self.btq1 = self.imp_dict["btq1"][len(self.imp_dict["btq1"])-1]
        t = datetime.datetime.now().strftime("%I:%M:%S%p on %B %d, %Y")
        txt = open('btq1.txt', 'a')
        txt.write(str(self.btq1) + "," + t + "\n")
        self.labelOne.SetLabel('Temperature  : ' + str(self.btq1))
        self.Refresh()

    def updatetq2(self, event):
        """battery NW quadrant temperature"""
        self.btq2 = self.imp_dict["btq2"][len(self.imp_dict["btq2"]) - 1]
        t = datetime.datetime.now().strftime("%I:%M:%S%p on %B %d, %Y")
        txt = open('btq2.txt', 'a')
        txt.write(str(self.btq2) + "," + t + "\n")
        self.labelTwo.SetLabel('Battery Current : ' + str(self.btq2))
        self.Refresh()

    def updatetq3(self, event):
        """battery SE quadrant temperature"""
        self.btq3 = self.imp_dict["btq3"][len(self.imp_dict["btq3"]) - 1]
        t = datetime.datetime.now().strftime("%I:%M:%S%p on %B %d, %Y")
        txt = open('btq3.txt', 'a')
        txt.write(str(self.btq3) + "," + t + "\n")
        self.labelTwo.SetLabel('Battery Current : ' + str(self.btq3))
        self.Refresh()

    def updatetq4(self, event):
        """battery SW quadrant temperature"""
        self.btq4 = self.imp_dict["btq4"][len(self.imp_dict["btq4"]) - 1]
        t = datetime.datetime.now().strftime("%I:%M:%S%p on %B %d, %Y")
        txt = open('btq4.txt', 'a')
        txt.write(str(self.btq4) + "," + t + "\n")
        self.labelTwo.SetLabel('Battery Current : ' + str(self.btq4))
        self.Refresh()

    def updatemaxdc(self, event):
        """max. discharge current"""
        self.maxdisc = self.imp_dict["maxdiscC"][len(self.imp_dict["maxdiscC"]) - 1]
        t = datetime.datetime.now().strftime("%I:%M:%S%p on %B %d, %Y")
        txt = open('maxdiscC.txt', 'a')
        txt.write(str(self.maxdisc) + "," + t + "\n")
        self.labelTwo.SetLabel('Battery Current : ' + str(self.maxdisc))
        self.Refresh()

    def updatemindc(self, event):
        """min. discharge current"""
        self.mindisc = self.imp_dict["mindiscC"][len(self.imp_dict["mindiscC"]) - 1]
        t = datetime.datetime.now().strftime("%I:%M:%S%p on %B %d, %Y")
        txt = open('mindiscC.txt', 'a')
        txt.write(str(self.mindisc) + "," + t + "\n")
        self.labelTwo.SetLabel('Battery Current : ' + str(self.mindisc))
        self.Refresh()

    def updatemaxc(self, event):
        """max current"""
        self.maxc = self.imp_dict["btq3"][len(self.imp_dict["btq3"]) - 1]
        t = datetime.datetime.now().strftime("%I:%M:%S%p on %B %d, %Y")
        txt = open('battery_current.txt', 'a')
        txt.write(str(self.maxc) + "," + t + "\n")
        self.labelTwo.SetLabel('Battery Current : ' + str(self.maxc))
        self.Refresh()

    def ShowYourself(self):
        l = self.GetParent().GetSize()
        self.SetSize(l)
        self.Raise()
        self.SetPosition((0, 0))
        self.Show()

    def OnMPPT(self, event):
        self.Hide()
        self.GetParent().panel1.ShowYourself()

    def OnMotor(self, event):
        self.Hide()
        self.GetParent().panel2.ShowYourself()

    def OnGeneral(self, event):
        self.Hide()
        self.GetParent().panel3.ShowYourself()


class MyPanel1(wx.Panel):

    """"""
    # ---------------MPPT----------------------

    def __init__(self, parent, id=-1):
        """Constructor"""
        wx.Panel.__init__(self, parent, id, size=(800, 480))
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        # timers
        self.timerx = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.MPPTWarn, self.timerx)
        self.timerx.Start(100)

        self.timery = wx.Timer(self)
        self.timery.Start(1000)

        self.timerz = wx.Timer(self)
        self.timerz.Start(1000)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.updatetq1, self.timer)
        self.timer.Start(1000)

        self.timer1 = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.updateC, self.timer1)
        self.timer1.Start(1000)

        # buttons and labels
        title = wx.StaticText(self, -1, 'MPPT')
        title.SetFont(
            wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.BOLD, wx.FONTWEIGHT_BOLD))
        title.SetForegroundColour('white')

        self.labelOne = wx.StaticText(self, -1, 'MPPT current 1')
        self.labelTwo = wx.StaticText(self, -1, 'MPPT current 2')

        self.labelOne.SetFont(
            wx.Font(20, wx.FONTFAMILY_DECORATIVE, wx.BOLD, wx.FONTWEIGHT_BOLD))
        self.labelTwo.SetFont(
            wx.Font(20, wx.FONTFAMILY_DECORATIVE, wx.BOLD, wx.FONTWEIGHT_BOLD))
        self.labelOne.SetForegroundColour('white')
        self.labelTwo.SetForegroundColour('white')

        self.wbutton0 = wx.Button(
            self, -1, '-            M P P T              -')
        self.wbutton1 = wx.Button(
            self, -1, '-             B M S                -')
        self.wbutton2 = wx.Button(
            self, -1, '-           M O T O R              -')
        self.wbutton3 = wx.Button(
            self, -1, '-          G E N E R A L           -')

        imageFile = "battery.png"
        image1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        BatteryBtn = wx.BitmapButton(self, id=-1, bitmap=image1,
                                     pos=(10, 20),
                                     size=(image1.GetWidth()+10,
                                           image1.GetHeight()+10))

        self.Bind(wx.EVT_BUTTON, self.OnBattery, BatteryBtn)

        imageFile = "mppt.png"
        image1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        MPPTBtn = wx.BitmapButton(self, id=-1, bitmap=image1,
                                  pos=(10, 20),
                                  size=(image1.GetWidth()+10,
                                        image1.GetHeight()+10))

        imageFile = "motor.png"
        image1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        MotorBtn = wx.BitmapButton(self, id=-1, bitmap=image1,
                                   pos=(10, 20),
                                   size=(image1.GetWidth()+10,
                                         image1.GetHeight()+10))

        self.Bind(wx.EVT_BUTTON, self.OnMotor, MotorBtn)

        self.Bind(wx.EVT_BUTTON, None, MPPTBtn)

        imageFile = "general.png"
        image1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        GenBtn = wx.BitmapButton(self, id=-1, bitmap=image1,
                                 pos=(10, 20),
                                 size=(image1.GetWidth()+10,
                                       image1.GetHeight()+10))

        self.Bind(wx.EVT_BUTTON, self.OnGeneral, GenBtn)

        topSizer = wx.BoxSizer(wx.VERTICAL)
        toolBtn = wx.BoxSizer(wx.HORIZONTAL)
        toolBtn_h = wx.BoxSizer(wx.VERTICAL)
        warnSizer = wx.BoxSizer(wx.HORIZONTAL)
        warnSizer_h = wx.BoxSizer(wx.VERTICAL)
        titleSizer = wx.BoxSizer(wx.HORIZONTAL)
        inputOneSizer = wx.BoxSizer(wx.HORIZONTAL)
        inputTwoSizer = wx.BoxSizer(wx.HORIZONTAL)

        toolBtn.Add(MPPTBtn, 0, wx.ALL, 5)
        toolBtn.Add(BatteryBtn, 0, wx.ALL, 5)
        toolBtn.Add(MotorBtn, 0, wx.ALL, 5)
        toolBtn.Add(GenBtn, 0, wx.ALL, 5)
        toolBtn_h.Add(toolBtn, 0, wx.CENTER, 5)

        warnSizer.Add(self.wbutton0, 0, wx.ALL, 5)
        warnSizer.Add(self.wbutton1, 0, wx.ALL, 5)
        warnSizer.Add(self.wbutton2, 0, wx.ALL, 5)
        warnSizer.Add(self.wbutton3, 0, wx.ALL, 5)
        warnSizer_h.Add(warnSizer, 0, wx.CENTER, 5)

        titleSizer.Add(title, 0, wx.ALL, 5)
        inputOneSizer.Add(self.labelOne, 0, wx.ALL, 5)
        inputTwoSizer.Add(self.labelTwo, 0, wx.ALL, 5)

        topSizer.Add(toolBtn_h, 0, wx.ALL | wx.EXPAND | wx.CENTER, 5)
        topSizer.Add(warnSizer_h, 0, wx.ALL | wx.EXPAND | wx.CENTER, 5)
        topSizer.Add(wx.StaticLine(self), 0, wx.ALL | wx.EXPAND | wx.CENTER, 5)
        topSizer.Add(titleSizer, 0, wx.CENTER)
        topSizer.Add(wx.StaticLine(self), 0, wx.ALL | wx.EXPAND, 5)
        topSizer.Add(inputOneSizer, 0, wx.ALL | wx.EXPAND, 5)
        topSizer.Add(inputTwoSizer, 0, wx.ALL | wx.EXPAND, 5)
        topSizer.Add(wx.StaticLine(self), 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(topSizer)
        topSizer.Fit(self)

        self.Raise()
        self.SetPosition((0, 0))
        self.Hide()
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

    def OnEraseBackground(self, evt):
        dc = evt.GetDC()

        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        start_image1 = wx.Image("solarcar.jpg")
        start_image1.Rescale(1310, 800)
        bmp = wx.BitmapFromImage(start_image1)
        dc.DrawBitmap(bmp, 0, 0)

    def MPPTWarn(self, event):
        if (self.GetParent().panel1.IsShown()):
            self.wbutton0.SetBackgroundColour('white')
            if i1 > 9.90:
                self.labelOne.SetForegroundColour('red')
            else:
                self.labelOne.SetForegroundColour('white')
            if i2 > 8.90:
                self.labelTwo.SetForegroundColour('red')
            else:
                self.labelTwo.SetForegroundColour('white')
        elif i1 > 9.90 or i2 > 8.90:
            self.wbutton0.SetBackgroundColour('red')
            self.GetParent().panel0.wbutton0.SetBackgroundColour('red')
            self.GetParent().panel2.wbutton0.SetBackgroundColour('red')
            self.GetParent().panel3.wbutton0.SetBackgroundColour('red')

    def onOK(self, event):
        # Do something
        print('onOK handler')

    def onCancel(self, event):
        self.closeProgram()

    def closeProgram(self):
        self.Destroy()

    def updatetq1(self, event):
        """"""
        global i1, t2
        i1 = random.uniform(9, 10)
        txt = open('mppt_current1.txt', 'a')
        txt.write(str(i1) + "," + str(t2) + "\n")
        t2 += 1
        if i1 > 7:
            self.labelOne.SetBackgroundColour('red')
            self.labelOne.SetLabel('Current1 : ' + str(i1))

        else:
            self.labelOne.SetBackgroundColour('white')
            self.labelOne.SetLabel('Current1 : ' + str(i1))

        self.Refresh()

    def updateC(self, event):
        """"""
        global i2, t3
        i2 = random.uniform(8, 9)
        txt = open('mppt_current2.txt', 'a')
        txt.write(str(i2) + "," + str(t3) + "\n")
        t3 += 1
        if i2 > 5.5:
            self.labelTwo.SetBackgroundColour('red')
            self.labelTwo.SetLabel('Current2 : ' + str(i2))

        else:
            self.labelTwo.SetBackgroundColour('white')
            self.labelTwo.SetLabel('Current2 : ' + str(i2))

        self.Refresh()

    def ShowYourself(self):
        l = self.GetParent().GetSize()
        self.SetSize(l)
        self.Raise()
        self.SetPosition((0, 0))
        self.Show()

    def OnMotor(self, event):
        self.Hide()
        self.GetParent().panel2.ShowYourself()

    def OnBattery(self, event):
        self.Hide()
        self.GetParent().panel0.ShowYourself()

    def OnGeneral(self, event):
        self.Hide()
        self.GetParent().panel3.ShowYourself()


class MyPanel2(wx.Panel):

    """"""
    # -------MOTOR CONTROLLER----------------------------

    def __init__(self, parent, id=-1):
        """Constructor"""
        wx.Panel.__init__(self, parent, id, size=(800, 480))
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        # timers
        self.timerx = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.MotorWarn, self.timerx)
        self.timerx.Start(100)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.updatetq1, self.timer)
        self.timer.Start(1000)

        self.timerz = wx.Timer(self)
        self.timerz.Start(1000)

        self.timer1 = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.updateC, self.timer1)
        self.timer1.Start(1000)

        # labels, buttons etc
        title = wx.StaticText(self, -1, 'Motor Controller')
        title.SetFont(
            wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.BOLD, wx.FONTWEIGHT_BOLD))
        title.SetForegroundColour('white')

        self.labelOne = wx.StaticText(self, -1, 'Motor Controller Current: ')
        self.labelTwo = wx.StaticText(self, -1, 'Motor Voltage')

        self.labelOne.SetFont(
            wx.Font(20, wx.FONTFAMILY_DECORATIVE, wx.BOLD, wx.FONTWEIGHT_BOLD))
        self.labelTwo.SetFont(
            wx.Font(20, wx.FONTFAMILY_DECORATIVE, wx.BOLD, wx.FONTWEIGHT_BOLD))
        self.labelOne.SetForegroundColour('white')
        self.labelTwo.SetForegroundColour('white')

        self.wbutton0 = wx.Button(
            self, -1, '-            M P P T               -')
        self.wbutton1 = wx.Button(
            self, -1, '-             B M S                -')
        self.wbutton2 = wx.Button(
            self, -1, '-           M O T O R              -')
        self.wbutton3 = wx.Button(
            self, -1, '-          G E N E R A L           -')

        imageFile = "mppt.png"
        image1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        MPPTBtn = wx.BitmapButton(self, id=-1, bitmap=image1,
                                  pos=(10, 20),
                                  size=(image1.GetWidth()+10,
                                        image1.GetHeight()+10))

        self.Bind(wx.EVT_BUTTON, self.OnMPPT, MPPTBtn)

        imageFile = "battery.png"
        image1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        BatteryBtn = wx.BitmapButton(self, id=-1, bitmap=image1,
                                     pos=(10, 20),
                                     size=(image1.GetWidth()+10,
                                           image1.GetHeight()+10))

        self.Bind(wx.EVT_BUTTON, self.OnBattery, BatteryBtn)

        imageFile = "motor.png"
        image1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        MotorBtn = wx.BitmapButton(self, id=-1, bitmap=image1,
                                   pos=(10, 20),
                                   size=(image1.GetWidth()+10,
                                         image1.GetHeight()+10))

        self.Bind(wx.EVT_BUTTON, None, MotorBtn)

        imageFile = "general.png"
        image1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        GenBtn = wx.BitmapButton(self, id=-1, bitmap=image1,
                                 pos=(10, 20),
                                 size=(image1.GetWidth()+10,
                                       image1.GetHeight()+10))

        self.Bind(wx.EVT_BUTTON, self.OnGeneral, GenBtn)

        topSizer = wx.BoxSizer(wx.VERTICAL)
        toolBtn = wx.BoxSizer(wx.HORIZONTAL)
        toolBtn_h = wx.BoxSizer(wx.VERTICAL)
        warnSizer = wx.BoxSizer(wx.HORIZONTAL)
        warnSizer_h = wx.BoxSizer(wx.VERTICAL)
        titleSizer = wx.BoxSizer(wx.HORIZONTAL)
        inputOneSizer = wx.BoxSizer(wx.HORIZONTAL)
        inputTwoSizer = wx.BoxSizer(wx.HORIZONTAL)

        toolBtn.Add(MPPTBtn, 0, wx.ALL, 5)
        toolBtn.Add(BatteryBtn, 0, wx.ALL, 5)
        toolBtn.Add(MotorBtn, 0, wx.ALL, 5)
        toolBtn.Add(GenBtn, 0, wx.ALL, 5)
        toolBtn_h.Add(toolBtn, 0, wx.CENTER, 5)

        warnSizer.Add(self.wbutton0, 0, wx.ALL, 5)
        warnSizer.Add(wx.StaticLine(self), 0, wx.ALL | wx.EXPAND, 5)
        warnSizer.Add(self.wbutton1, 0, wx.ALL, 5)
        warnSizer.Add(self.wbutton2, 0, wx.ALL, 5)
        warnSizer.Add(self.wbutton3, 0, wx.ALL, 5)
        warnSizer_h.Add(warnSizer, 0, wx.CENTER, 5)

        titleSizer.Add(title, 0, wx.ALL, 5)

        inputOneSizer.Add(self.labelOne, 0, wx.ALL, 5)

        inputTwoSizer.Add(self.labelTwo, 0, wx.ALL, 5)

        topSizer.Add(toolBtn_h, 0, wx.ALL | wx.EXPAND | wx.CENTER, 5)
        topSizer.Add(warnSizer_h, 0, wx.ALL | wx.EXPAND | wx.CENTER, 5)
        topSizer.Add(wx.StaticLine(self), 0, wx.ALL | wx.EXPAND, 5)
        topSizer.Add(titleSizer, 0, wx.CENTER)
        topSizer.Add(wx.StaticLine(self), 0, wx.ALL | wx.EXPAND, 5)
        topSizer.Add(inputOneSizer, 0, wx.ALL | wx.EXPAND, 5)
        topSizer.Add(inputTwoSizer, 0, wx.ALL | wx.EXPAND, 5)
        topSizer.Add(wx.StaticLine(self), 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(topSizer)
        topSizer.Fit(self)

        self.Raise()
        self.SetPosition((0, 0))
        self.Hide()

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

    def OnEraseBackground(self, evt):
        dc = evt.GetDC()

        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        start_image1 = wx.Image("solarcar.jpg")
        start_image1.Rescale(1310, 800)
        bmp = wx.BitmapFromImage(start_image1)
        dc.DrawBitmap(bmp, 0, 0)

    def MotorWarn(self, event):
        if (self.GetParent().panel2.IsShown()):
            self.wbutton2.SetBackgroundColour('white')
            if Mv > 71:
                self.labelOne.SetForegroundColour('red')
            else:
                self.labelOne.SetForegroundColour('white')
            if Im > 200:
                self.labelTwo.SetForegroundColour('red')
            else:
                self.labelTwo.SetForegroundColour('white')
        elif Mv > 71 or Im > 200:
            self.wbutton2.SetBackgroundColour('red')
            self.GetParent().panel0.wbutton2.SetBackgroundColour('red')
            self.GetParent().panel1.wbutton2.SetBackgroundColour('red')
            self.GetParent().panel3.wbutton2.SetBackgroundColour('red')

    def closeProgram(self):
        self.Destroy()

    def updateV(self, event):
        """"""
        global Im, t4
        Im = random.uniform(100, 220)
        txt = open('motor_current.txt', 'a')
        txt.write(str(Im) + "," + str(t4) + "\n")
        t4 += 1
        if Im > 200:
            self.labelOne.SetBackgroundColour('red')
            self.labelOne.SetLabel('Motor Controller Current : ' + str(Im))

        else:
            self.labelOne.SetBackgroundColour('white')
            self.labelOne.SetLabel('Motor Controller Current : ' + str(Im))

        self.Refresh()

    def updateC(self, event):
        """"""
        global Mv, t5
        Mv = random.uniform(65, 72)
        txt = open('motor_voltage.txt', 'a')
        txt.write(str(Mv) + "," + str(t5) + "\n")
        t5 += 1
        if Mv > 69:
            self.labelTwo.SetBackgroundColour('red')
            self.labelTwo.SetLabel('Motor Voltage : ' + str(Mv))

        else:
            self.labelTwo.SetBackgroundColour('white')
            self.labelTwo.SetLabel('Motor Voltage : ' + str(Mv))

        self.Refresh()

    def ShowYourself(self):
        l = self.GetParent().GetSize()
        self.SetSize(l)
        self.Raise()
        self.SetPosition((0, 0))
        self.Show()

    def OnMPPT(self, event):
        self.Hide()
        self.GetParent().panel1.ShowYourself()

    def OnBattery(self, event):
        self.Hide()
        self.GetParent().panel0.ShowYourself()

    def OnGeneral(self, event):
        self.Hide()
        self.GetParent().panel3.ShowYourself()


class MyPanel3(wx.Panel):

    """"""
    # ----------------------------------------------------------------------

    def __init__(self, parent, id=-1):
        """Constructor"""
        wx.Panel.__init__(self, parent, id, size=(800, 480))
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        # timers
        self.timer1 = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.updateS, self.timer1)
        self.timer1.Start(1000)

        self.timery = wx.Timer(self)
        self.timery.Start(1000)

        self.timerz = wx.Timer(self)
        self.timerz.Start(1000)

        self.timer2 = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.updateA, self.timer2)
        self.timer2.Start(1000)

        self.timer3 = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.updateT, self.timer3)
        self.timer3.Start(1000)

        # labels, buttons etc
        title = wx.StaticText(self, -1, 'General')
        title.SetFont(
            wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.BOLD, wx.FONTWEIGHT_BOLD))
        title.SetForegroundColour('white')
        self.labelOne = wx.StaticText(self, -1)
        self.labelOne.SetLabel('Car Speed : ')
        self.labelTwo = wx.StaticText(self, -1)
        self.labelTwo.SetLabel('Acceleration: ')
        self.labelThree = wx.StaticText(self, -1)
        self.labelThree.SetLabel('Ambient Temperature:')

        self.labelOne.SetFont(
            wx.Font(20, wx.FONTFAMILY_DECORATIVE, wx.BOLD, wx.FONTWEIGHT_BOLD))
        self.labelTwo.SetFont(
            wx.Font(20, wx.FONTFAMILY_DECORATIVE, wx.BOLD, wx.FONTWEIGHT_BOLD))
        self.labelThree.SetFont(
            wx.Font(20, wx.FONTFAMILY_DECORATIVE, wx.BOLD, wx.FONTWEIGHT_BOLD))
        self.labelOne.SetForegroundColour('white')
        self.labelTwo.SetForegroundColour('white')
        self.labelThree.SetForegroundColour('white')

        self.wbutton0 = wx.Button(
            self, -1, '-            M P P T               -')
        self.wbutton1 = wx.Button(
            self, -1, '-             B M S                -')
        self.wbutton2 = wx.Button(
            self, -1, '-           M O T O R              -')
        self.wbutton3 = wx.Button(
            self, -1, '-          G E N E R A L           -')

        imageFile = "battery.png"
        image1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        BatteryBtn = wx.BitmapButton(self, id=-1, bitmap=image1,
                                     pos=(10, 20),
                                     size=(image1.GetWidth() + 10,
                                           image1.GetHeight() + 10))

        self.Bind(wx.EVT_BUTTON, self.OnBattery, BatteryBtn)

        imageFile = "mppt.png"
        image1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        MPPTBtn = wx.BitmapButton(self, id=-1, bitmap=image1,
                                  pos=(10, 20),
                                  size=(image1.GetWidth() + 10,
                                        image1.GetHeight() + 10))
        self.Bind(wx.EVT_BUTTON, self.OnMotor, MPPTBtn)

        imageFile = "motor.png"
        image1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        MotorBtn = wx.BitmapButton(self, id=-1, bitmap=image1,
                                   pos=(10, 20),
                                   size=(image1.GetWidth()+10,
                                         image1.GetHeight()+10))

        self.Bind(wx.EVT_BUTTON, self.OnMotor, MotorBtn)

        imageFile = "general.png"
        image1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        GenBtn = wx.BitmapButton(self, id=-1, bitmap=image1,
                                 pos=(10, 20),
                                 size=(image1.GetWidth()+10,
                                       image1.GetHeight()+10))

        self.Bind(wx.EVT_BUTTON, None, GenBtn)

        topSizer = wx.BoxSizer(wx.VERTICAL)
        toolBtn = wx.BoxSizer(wx.HORIZONTAL)
        toolBtn_h = wx.BoxSizer(wx.VERTICAL)
        warnSizer = wx.BoxSizer(wx.HORIZONTAL)
        warnSizer_h = wx.BoxSizer(wx.VERTICAL)
        titleSizer = wx.BoxSizer(wx.HORIZONTAL)
        inputOneSizer = wx.BoxSizer(wx.HORIZONTAL)
        inputTwoSizer = wx.BoxSizer(wx.HORIZONTAL)
        inputThreeSizer = wx.BoxSizer(wx.HORIZONTAL)

        toolBtn.Add(MPPTBtn, 0, wx.ALL, 5)
        toolBtn.Add(BatteryBtn, 0, wx.ALL, 5)
        toolBtn.Add(MotorBtn, 0, wx.ALL, 5)
        toolBtn.Add(GenBtn, 0, wx.ALL, 5)
        toolBtn_h.Add(toolBtn, 0, wx.CENTER, 5)

        warnSizer.Add(self.wbutton0, 0, wx.ALL, 5)
        warnSizer.Add(wx.StaticLine(self), 0, wx.ALL | wx.EXPAND, 5)
        warnSizer.Add(self.wbutton1, 0, wx.ALL, 5)
        warnSizer.Add(self.wbutton2, 0, wx.ALL, 5)
        warnSizer.Add(self.wbutton3, 0, wx.ALL, 5)
        warnSizer_h.Add(warnSizer, 0, wx.CENTER, 5)

        titleSizer.Add(title, 0, wx.ALL, 5)

        inputOneSizer.Add(self.labelOne, 0, wx.ALL, 5)

        inputTwoSizer.Add(self.labelTwo, 0, wx.ALL, 5)

        inputThreeSizer.Add(self.labelThree, 0, wx.ALL, 5)

        topSizer.Add(toolBtn_h, 0, wx.ALL | wx.EXPAND | wx.CENTER, 5)
        topSizer.Add(warnSizer_h, 0, wx.ALL | wx.EXPAND | wx.CENTER, 5)
        topSizer.Add(wx.StaticLine(self), 0, wx.ALL | wx.EXPAND, 5)
        topSizer.Add(titleSizer, 0, wx.CENTER)
        topSizer.Add(wx.StaticLine(self), 0, wx.ALL | wx.EXPAND, 5)
        topSizer.Add(inputOneSizer, 0, wx.ALL | wx.EXPAND, 5)
        topSizer.Add(inputTwoSizer, 0, wx.ALL | wx.EXPAND, 5)
        topSizer.Add(inputThreeSizer, 0, wx.ALL | wx.EXPAND, 5)
        topSizer.Add(wx.StaticLine(self), 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(topSizer)
        topSizer.Fit(self)

        self.Raise()
        self.SetPosition((0, 0))
        self.Hide()

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

    def OnEraseBackground(self, evt):
        dc = evt.GetDC()

        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        start_image1 = wx.Image("solarcar.jpg")
        start_image1.Rescale(1310, 800)
        bmp = wx.BitmapFromImage(start_image1)
        dc.DrawBitmap(bmp, 0, 0)

    def updateS(self, event):
        v = 0
        self.labelOne.SetLabel('Car Speed : ' + str(v))

    def updateA(self, event):
        a = 0
        self.labelTwo.SetLabel('Acceleration : ' + str(a))

    def updateT(self, event):
        t = random.uniform(28, 30)
        self.labelThree.SetLabel('Ambient Temperature : ' + str(t))

    def closeProgram(self):
        self.Destroy()

    def ShowYourself(self):
        l = self.GetParent().GetSize()
        self.SetSize(l)
        self.Raise()
        self.SetPosition((0, 0))
        self.Show()

    def OnMotor(self, event):
        self.Hide()
        self.GetParent().panel2.ShowYourself()

    def OnMPPT(self, event):
        self.Hide()
        self.GetParent().panel1.ShowYourself()

    def OnBattery(self, event):
        self.Hide()
        self.GetParent().panel0.ShowYourself()


def main(val):
    app = My_App(redirect=False, sensor_dict=val)
    app.MainLoop()

if __name__ == '__main__':
    main()
