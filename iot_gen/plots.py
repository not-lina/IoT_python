import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
import wx

class FPlotA(wx.Frame):
    def __init__(self, df):
        wx.Frame.__init__(self, None, -1, 'plot a')
        self.panel = wx.Panel(self)
        self.fig = Figure()
        self.canvas = FigCanvas(self.panel, -1, self.fig)

        self.axes = self.fig.add_subplot(111)

        self.axes.hist(df['outside_temp'])
        self.canvas.draw()
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.panel.SetSizer(self.vbox)
        self.vbox.Fit(self)


class FPlotB(wx.Frame):
    def __init__(self, df):
        wx.Frame.__init__(self, None, -1, 'plot b')
        self.panel = wx.Panel(self)
        self.fig = Figure()
        self.canvas = FigCanvas(self.panel, -1, self.fig)

        self.axes = self.fig.add_subplot(111)
        self.axes.plot(df['outside_temp'], df['inside_temp'])
        self.canvas.draw()
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.panel.SetSizer(self.vbox)
        self.vbox.Fit(self)

class FPlotC(wx.Frame):
    def __init__(self, df):
        wx.Frame.__init__(self, None, -1, 'plot c')
        self.panel = wx.Panel(self)
        self.fig = Figure()
        self.canvas = FigCanvas(self.panel, -1, self.fig)

        bins = 15
        ax1 = self.fig.add_subplot(1, 1, 1)
        ax2 = self.fig.add_subplot(1, 2, 1)

        ax1.hist(df['outside_temp'], bins, alpha=0.5, label='outside_temp')
        ax1.hist(df['inside_temp'], bins, alpha=0.5, label='inside_temp')
        ax1.legend(loc='upper right')
        ax2.hist(df['outside_humidity'], bins, alpha=0.5, label='outside_humidity')
        ax2.hist(df['inside_humidity'], bins, alpha=0.5, label='inside_humidity')
        ax2.legend(loc='upper right')

        self.canvas.draw()
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.panel.SetSizer(self.vbox)
        self.vbox.Fit(self)
