import wx
from DataLoader import DataLoader
import json
import csv
from plots import FPlotC, FPlotB, FPlotA

NUM_USERS = 10
NUM_READINGS = 10

class VisualizeData():
    def __init__(self, parent):
        self.parent = parent

    def PlotA(self, event):
        f2 = FPlotA(self.parent.data.toDf())
        f2.Show()
    def PlotB(self, event):
        f3 = FPlotB(self.parent.data.toDf())
        f3.Show()
    def PlotC(self, event):
        f4 = FPlotC(self.parent.data.toDf())
        f4.Show()

class GenerateData(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.status = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        sizer.Add(self.status, 1, wx.ALL|wx.EXPAND)
        self.SetSizer(sizer)
        self.parent = parent
        self.status.WriteText(f'welcome\n')

    def IotGenerator(self, event):
        self.status.WriteText(f'generating iot data\n')
        data = DataLoader(NUM_USERS, NUM_READINGS)

        self.parent.progress = wx.ProgressDialog(
            "generating users data ...",
            "",
            NUM_USERS*NUM_READINGS,
            self,
            wx.PD_AUTO_HIDE|wx.PD_APP_MODAL|wx.PD_SMOOTH
        )

        for (nu, nd) in data.genUsers():
            t = nu*NUM_READINGS + nd
            self.parent.progress.Update(t,f"generating user: {nu} iot data: {nd}")
            wx.Yield()

        self.parent.progress.Destroy()
        self.parent.data = data
        self.status.WriteText(f'\n {len(data.users)} users \n {len(data.data[0])} samples each \n')


    def writeCsv(self, pathname):
        headers = self.parent.data.headers()
        with open(pathname, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            for data in self.parent.data.toCsv():
                writer.writerow(data)
            self.status.WriteText('save complete')

    def writeJson(self, pathname):
        with open(pathname, 'w') as file:
            json.dump(self.parent.data.toJson(), file)
            self.status.WriteText('save complete')

    def SaveJson(self, event):
        filetype = 'json'
        self.OnSaveAs(event, filetype, self.writeJson)

    def SaveCsv(self,event):
        filetype = 'csv'
        self.OnSaveAs(event, filetype, self.writeCsv)

    def LoadCsv(self, event):
        data = DataLoader(NUM_USERS, NUM_READINGS)
        wildcard = "CSV files (*.csv)|*.csv"
        dialog = wx.FileDialog(self, "Open csv File", wildcard=wildcard,
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if dialog.ShowModal() == wx.ID_CANCEL:
            return

        filename = dialog.GetPath()
        data.fromCsv(filename)
        self.status.WriteText(f'loaded from{filename}\n')
        self.parent.data = data

    def OnSaveAs(self, event, filetype, handler):
        with wx.FileDialog(self, f"Save {filetype} file", wildcard=f"{filetype} files (*.{filetype})|*.{filetype}",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL: return

            pathname = fileDialog.GetPath()
            try:
                handler(pathname)

                self.status.WriteText(f'writing to {pathname}\n')
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % pathname)

class FrameContainer(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='Data Generator')
        self.fileMenuExitItem = None
        self.SetupMenus()
        self.Show(True)

    def SetupMenus(self):
        menuBar = wx.MenuBar()
        self.SetupFileMenu(menuBar)
        self.SetupStatsMenu(menuBar)
        self.SetMenuBar(menuBar)

    def AddItemToMenu(self, menu, name, descr, cb):
        item = menu.Append(
            wx.NewId(),
            name,
            descr
        )
        self.Bind(wx.EVT_MENU, cb, item)

    def SetupFileMenu(self, menuBar):
        fileMenu = wx.Menu()
        dGen = GenerateData(self)
        fileItems = [
            ("Generate IoT", "Generate sample IoT data", dGen.IotGenerator),
            ("Save JSON"   , "Save data to json file"  , dGen.SaveJson),
            ("Save CSV"    , "Save data to csv file"   , dGen.SaveCsv),
            ("Load CSV", "Load data from csv file"     , dGen.LoadCsv)
        ]

        for (a, b, c) in fileItems:
            self.AddItemToMenu(fileMenu, a, b, c)

        self.BindExit(fileMenu)
        menuBar.Append(fileMenu, "&File")

    def BindExit(self, menu):
        exitMenuItem = menu.Append(
            wx.NewId(),
            "Exit",
            "Exit the application"
        )
        self.Bind(wx.EVT_MENU, self.OnCloseFrame, exitMenuItem)
        self.Bind(wx.EVT_CLOSE, self.OnCloseFrame)

    def SetupStatsMenu(self, menuBar):
        statsMenu = wx.Menu()
        viz = VisualizeData(self)
        statsItems = [
            ("Plot A", "Outside temperature"        , viz.PlotA),
            ("Plot B", "Outside vs Room Temperature", viz.PlotB),
            ("Plot C", "Show All Measurements"      , viz.PlotC)
        ]

        for (a, b, c) in statsItems:
            self.AddItemToMenu(statsMenu, a, b, c)

        menuBar.Append(statsMenu, "&Statistics")

    # Destroys the main frame which quits the wxPython application
    def OnExitApp(self, event):
        self.Destroy()


    # Makes sure the user was intending to quit the application
    def OnCloseFrame(self, event):
        dialog = wx.MessageDialog(
            self,
            message = "Are you sure you want to quit?",
            caption = "Caption",
            style = wx.YES_NO,
            pos = wx.DefaultPosition
        )

        response = dialog.ShowModal()

        if (response == wx.ID_YES):
            self.OnExitApp(event)
        else:
            event.StopPropagation()

def main():
    app = wx.App(False)
    frame = FrameContainer()
    app.MainLoop()

if __name__ == '__main__':
    main()
