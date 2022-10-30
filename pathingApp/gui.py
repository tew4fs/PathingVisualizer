import tkinter as tk
import math
import time
from algorthims.astar import AStar


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.GRID_WIDTH = 25
        self.GRID_HEIGHT = 25
        self.BLOCK_COLOR = "#878E88"
        self.GRID_COLOR_ONE = "#77B6EA"
        self.GRID_COLOR_TWO = "#C7D3DD"
        self.START_COLOR = "#59C3C3"
        self.FINISH_COLOR = "#F45B69"
        self.BACKGROUND_COLOR = "#767676"
        self.ALGORITHM_COLOR = "#DDD19D"
        self.PATH_COLOR = "#B9DE9E"

        self.geometry("1150x950")
        self.title("Pathing Algorithms")
        self.resizable(0, 0)
        self.configure(bg=self.BACKGROUND_COLOR)

        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=1)

        self.grid = tk.Frame(self, borderwidth=1, relief="solid")
        self.grid.grid(column=0, row=1, padx=10, pady=35)

        self.previewWindow = tk.Frame(self, bg=self.BACKGROUND_COLOR)
        self.previewGrid = tk.Frame(self.previewWindow, borderwidth=1, relief="solid")
        self.previewWindow.columnconfigure(0, weight=3)
        self.previewWindow.columnconfigure(1, weight=1)
        self.previewGrid.grid(column=0, row=1, padx=75, pady=70)
        self.previewControlPanel = tk.Frame(self.previewWindow, bg=self.BACKGROUND_COLOR)
        self.previewControlPanel.grid(column=1, row=1, padx=10)

        self.controlPanel = tk.Frame(self, bg=self.BACKGROUND_COLOR)
        self.controlPanel.grid(column=1, row=1)

        self.previewPoints = []
        self.points = []
        self.blocks = []
        self.previewBlocks = []
        self.currentPath = []
        self.observedPoints = []

        self.startColumn = 0
        self.startRow = 0
        self.finishColumn = 1
        self.finishRow = 0

        self.previewStartColumn = 0
        self.previewStartRow = 0
        self.previewFinishColumn = 1
        self.previewFinishRow = 0

        self.clear = tk.Button(
            self.controlPanel,
            text="Clear",
            command=self.clearGrid,
            width=10,
            pady=10,
            bg=self.GRID_COLOR_TWO,
        )
        self.clear.grid(column=0, pady=10)

        self.run = tk.Button(
            self.controlPanel,
            text="Run",
            command=self.runAlgorithm,
            width=10,
            pady=10,
            bg=self.GRID_COLOR_TWO,
        )
        self.run.grid(column=0, pady=10)

        self.save = tk.Button(
            self.controlPanel,
            text="Save",
            command=self.saveGrid,
            width=10,
            pady=10,
            bg=self.GRID_COLOR_TWO,
        )
        self.save.grid(column=0, pady=10)

        self.preview = tk.Button(
            self.controlPanel,
            text="Load",
            command=self.showPreview,
            width=10,
            pady=10,
            bg=self.GRID_COLOR_TWO,
        )
        self.preview.grid(column=0, pady=10)

        self.load = tk.Button(
            self.previewControlPanel,
            text="Load",
            command=self.loadGrid,
            width=5,
            pady=5,
            bg=self.GRID_COLOR_TWO,
        )
        self.load.grid(column=0, pady=10)

        self.cancel = tk.Button(
            self.previewControlPanel,
            text="Cancel",
            command=self.previewCancel,
            width=5,
            pady=5,
            bg=self.GRID_COLOR_TWO,
        )
        self.cancel.grid(column=0, pady=10)

        for r in range(self.GRID_HEIGHT):
            for c in range(self.GRID_WIDTH):
                box = tk.Label(
                    self.grid,
                    width=4,
                    height=2,
                    borderwidth=1,
                    relief="solid",
                    bg=self.getBackgroundColor(c, r),
                    name="c" + str(c) + "r" + str(r),
                )
                self.points.append(box)
                box.grid(column=c, row=r)
                box.bind("<B1-Motion>", self.mouse1Motion)
                box.bind("<B3-Motion>", self.mouse3Motion)
                box.bind("<ButtonRelease-1>", self.mouse1Up)
                box.bind("<ButtonRelease-3>", self.mouse3Up)

        self.start = tk.Label(
            self.grid,
            width=4,
            height=2,
            text="S",
            name="start",
            padx=0,
            pady=0,
            borderwidth=1,
            bg=self.START_COLOR,
        )
        self.start.grid(column=0, row=0)
        self.finish = tk.Label(
            self.grid,
            width=4,
            height=2,
            text="F",
            name="finish",
            padx=0,
            pady=0,
            borderwidth=1,
            bg=self.FINISH_COLOR,
        )
        self.finish.grid(column=1, row=0)

        for r in range(self.GRID_HEIGHT):
            for c in range(self.GRID_WIDTH):
                box = tk.Label(
                    self.previewGrid,
                    borderwidth=1,
                    width=2,
                    relief="solid",
                    bg=self.getBackgroundColor(c, r),
                    name="c" + str(c) + "r" + str(r),
                )
                self.previewPoints.append(box)
                box.grid(column=c, row=r)
        self.previewStart = tk.Label(
            self.previewGrid,
            width=2,
            text="S",
            name="start",
            padx=0,
            pady=0,
            borderwidth=1,
            bg=self.START_COLOR,
        )
        self.previewStart.grid(column=0, row=0)
        self.previewFinish = tk.Label(
            self.previewGrid,
            width=2,
            text="F",
            name="finish",
            padx=0,
            pady=0,
            borderwidth=1,
            bg=self.FINISH_COLOR,
        )
        self.previewFinish.grid(column=1, row=0)

        self.start.bind("<B1-Motion>", self.moveStart)
        self.finish.bind("<B1-Motion>", self.moveFinish)

    def clearGrid(self):
        self.blocks.clear()
        for r in range(self.GRID_HEIGHT):
            for c in range(self.GRID_WIDTH):
                index = r * self.GRID_WIDTH + c
                self.points[index].configure(bg=self.getBackgroundColor(c, r))

    def runAlgorithm(self):
        aStar = AStar()
        self.clearPath()
        self.currentPath, self.observedPoints = aStar.A_Star(
            (self.startColumn, self.startRow),
            (self.finishColumn, self.finishRow),
            self.blocks,
            self.GRID_HEIGHT,
            self.GRID_WIDTH,
        )
        self.showPath()

    def saveGrid(self):
        file = open("grids/grids.txt", "w")
        lines = [
            str(self.startColumn) + " " + str(self.startRow) + "\n",
            str(self.finishColumn) + " " + str(self.finishRow) + "\n",
            str(self.blocks) + "\n",
        ]
        file.writelines(lines)
        file.close()

    def previewCancel(self):
        for block in self.previewBlocks:
            index = block[1] * self.GRID_WIDTH + block[0]
            self.previewPoints[index].configure(bg=self.getBackgroundColor(block[0], block[1]))
        self.previewWindow.grid_forget()

    def showPreview(self):
        self.previewWindow.grid(column=0, row=1, padx=10, pady=35)
        self.loadPreviewGrid("G1")
        self.previewStart.grid(column=self.previewStartColumn, row=self.previewStartRow)
        self.previewFinish.grid(column=self.previewFinishColumn, row=self.previewFinishRow)
        for block in self.previewBlocks:
            index = block[1] * self.GRID_WIDTH + block[0]
            self.previewPoints[index].configure(bg=self.BLOCK_COLOR)

    def loadPreviewGrid(self, id):
        file = open("grids/grids.txt", "r")
        start = file.readline().split()
        finish = file.readline().split()
        blocks = file.readline().split("), (")

        self.previewStartColumn = int(start[0])
        self.previewStartRow = int(start[1])
        self.previewFinishColumn = int(finish[0])
        self.previewFinishRow = int(finish[1])
        blocks[0] = blocks[0][2:]
        blocks[len(blocks) - 1] = blocks[len(blocks) - 1][: len(blocks[len(blocks) - 1]) - 3]
        blockList = []
        for block in blocks:
            point = block.split(",")
            blockList.append((int(point[0]), int(point[1])))
        self.previewBlocks = blockList
        file.close()

    def loadGrid(self):
        for block in self.previewBlocks:
            index = block[1] * self.GRID_WIDTH + block[0]
            self.previewPoints[index].configure(bg=self.getBackgroundColor(block[0], block[1]))
        self.previewWindow.grid_forget()
        self.clearGrid()
        self.startColumn = self.previewStartColumn
        self.startRow = self.previewStartRow
        self.finishColumn = self.previewFinishColumn
        self.finishRow = self.previewFinishRow
        self.blocks = self.previewBlocks
        self.refreshGrid()

    def showPath(self):
        for point in self.observedPoints:
            c = point[0]
            r = point[1]
            self.points[c + r * self.GRID_WIDTH].configure(bg=self.ALGORITHM_COLOR)
            self.update()
            time.sleep(0.025)
        for point in self.currentPath:
            c = point[0]
            r = point[1]
            self.points[c + r * self.GRID_WIDTH].configure(bg=self.PATH_COLOR)

    def clearPath(self):
        for point in self.currentPath:
            c = point[0]
            r = point[1]
            self.points[c + r * self.GRID_WIDTH].configure(bg=self.getBackgroundColor(c, r))
        for point in self.observedPoints:
            c = point[0]
            r = point[1]
            self.points[c + r * self.GRID_WIDTH].configure(bg=self.getBackgroundColor(c, r))
        self.currentPath = []
        self.observedPoints = []

    def parseName(self, name):
        indexOfR = name.find("r")
        c = int(name[1:indexOfR])
        r = int(name[indexOfR+1:])
        return c, r

    def inMotionEvent(self, event, startColumn, startRow):
        widgetHeight = event.widget.winfo_height()
        widgetWidth = event.widget.winfo_width()
        x = event.x
        y = event.y
        deltaC = (x) / widgetWidth
        deltaR = (y) / widgetHeight
        c = math.floor(startColumn + deltaC)
        r = math.floor(startRow + deltaR)
        return c, r

    def getColAndRowInMotion(self, event):
        startC, startR = self.parseName(str(event.widget).split(".")[-1])
        return self.inMotionEvent(event, startC, startR)

    def getFlagsColAndRowInMotion(self, event, isStart):
        if isStart:
            return self.inMotionEvent(event, self.startColumn, self.startRow)
        else:
            return self.inMotionEvent(event, self.finishColumn, self.finishRow)

    def refreshGrid(self):
        self.start.grid(column=self.startColumn, row=self.startRow)
        self.finish.grid(column=self.finishColumn, row=self.finishRow)
        for block in self.blocks:
            self.addBlock(block[0], block[1])

    def addBlock(self, c, r):
        if self.blocks.count((c, r)) == 0:
            self.blocks.append((c, r))
        if c >= 0 and c < self.GRID_WIDTH and r >= 0 and r < self.GRID_HEIGHT:
            index = r * self.GRID_WIDTH + c
            self.points[index].configure(bg=self.BLOCK_COLOR)

    def removeBlock(self, c, r):
        if self.blocks.count((c, r)) > 0:
            self.blocks.remove((c, r))
        if c >= 0 and c < self.GRID_WIDTH and r >= 0 and r < self.GRID_HEIGHT:
            index = r * self.GRID_WIDTH + c
            self.points[index].configure(bg=self.getBackgroundColor(c, r))

    def mouse1Motion(self, event):
        self.clearPath()
        c, r = self.getColAndRowInMotion(event)
        self.addBlock(c, r)

    def mouse3Motion(self, event):
        self.clearPath()
        c, r = self.getColAndRowInMotion(event)
        self.removeBlock(c, r)

    def mouse1Up(self, event):
        self.clearPath()
        c, r = self.getColAndRowInMotion(event)
        self.addBlock(c, r)

    def mouse3Up(self, event):
        self.clearPath()
        c, r = self.getColAndRowInMotion(event)
        self.removeBlock(c, r)

    def getBackgroundColor(self, c, r):
        if r % 2 == 0:
            if c % 2 == 0:
                return self.GRID_COLOR_TWO
        elif c % 2 == 1:
            return self.GRID_COLOR_TWO
        return self.GRID_COLOR_ONE

    def moveStart(self, event):
        self.clearPath()
        c, r = self.getFlagsColAndRowInMotion(event, True)
        if c >= 0 and c < self.GRID_WIDTH and r >= 0 and r < self.GRID_HEIGHT:
            self.startColumn = c
            self.startRow = r
            event.widget.grid(column=c, row=r)

    def moveFinish(self, event):
        self.clearPath()
        c, r = self.getFlagsColAndRowInMotion(event, False)
        if c >= 0 and c < self.GRID_WIDTH and r >= 0 and r < self.GRID_HEIGHT:
            self.finishColumn = c
            self.finishRow = r
            event.widget.grid(column=c, row=r)


if __name__ == "__main__":
    gui = GUI()
    gui.mainloop()
