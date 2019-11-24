from pipes import SOURCE
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.config import Config
import random
import sys


class mishbezet(ButtonBehavior, Image):
    def __init__(self, line, colom, num=0, **kwargs):
        # num = -1  is a bomb in the cell , if not the number in the cell is the number of the bombs around the cell.
        ButtonBehavior.__init__(self, **kwargs)
        Image.__init__(self, **kwargs)
        self.flagged = False
        self.line = line
        self.hidden = True
        self.col = colom
        self.num = num
        self.source = "dolphin.png"


# random.randint(1,101)


class Board(GridLayout):
    def __init__(self, numLines=10, **kwargs):
        # constructor of the board
        GridLayout.__init__(self, **kwargs)
        self.cols = numLines  # number of colomn in the gridLayout
        self.myBoard = list()  # all the cells in the board
        self.countBomb = 0
        self.bombAmount = Label(text=str(self.countBomb), font_size='20sp')
        self.firstMove = True
        self.finished = False
        self.createSquares()

    def createSquares(self):
        for i in range(self.cols):
            for j in range(self.cols):
                ta = mishbezet(i, j)
                ta.bind(on_press=self.click)
                self.myBoard.append(ta)
                self.add_widget(ta)

    def reveal(self, touch):
        touch.hidden = False
        self.toExpose -= 1
        touch.source = str(touch.num) + ".png"
        if touch.num == 0:
            for x in self.myBoard:
                if x != touch and x.col in [touch.col, touch.col-1, touch.col+1] and x.line in [touch.line, touch.line-1, touch.line+1] and x.hidden:
                    self.reveal(x)

    def click(self, touch):
        if self.finished:
            sys.exit()
        if touch.last_touch.button == "left" and not touch.flagged and touch.hidden:
            if touch.num == -1:
                touch.source = "bomb.jpg"
                self.finished = True
                self.add_widget(Label(text="GAME OVER", font_size='20sp', color=(1, 0, 0, 1)))
            else:
                if self.firstMove:
                    self.firstMove = False
                    self.firstSquare = touch
                    self.randomBomb()
                    self.bombAmount.text = str(self.countBomb)
                    self.changeNumInCell()
                    self.add_widget(Label(text='num bombs', font_size='20sp'))
                    self.add_widget(self.bombAmount)
                self.reveal(touch)
                if self.toExpose == 0:
                    self.finished = True
                    self.add_widget(Label(text="YOU WIN", font_size='20sp', color=(0, 1, 0, 1)))
        elif touch.last_touch.button == "right":
            if touch.hidden:
                if not touch.flagged:
                    touch.source = "flag.jpg"
                    touch.flagged = True
                    self.countBomb -= 1
                else:
                    touch.source = "dolphin.png"
                    touch.flagged = False
                    self.countBomb += 1
                self.bombAmount.text = str(self.countBomb)

    def randomBomb(self):  # we are written this but the students wouldnt get this
        for ta in self.myBoard:
            x = random.randint(0, 6)  # normaly there is a 16% chance of cell to be a bomb. so we use random to decide witch is bomb and witch isn't
            if x == 1 and not (ta.col in (self.firstSquare.col, self.firstSquare.col-1, self.firstSquare.col+1) and ta.line in (self.firstSquare.line, self.firstSquare.line-1, self.firstSquare.line+1)):  # statistics of bombs
                ta.num = -1
                self.countBomb += 1
        self.toExpose = self.cols**2 - self.countBomb


    def changeNumInCell(self):
        for ta in self.myBoard:
            for neighborTa in self.myBoard:
                if (ta.num != -1):  # if it is not a bomb
                    if (neighborTa.num == -1):  # check if the neighbor is a bomb
                        if (ta.line + 1 == neighborTa.line and ta.col == neighborTa.col):
                            ta.num += 1
                        if (ta.line - 1 == neighborTa.line and ta.col == neighborTa.col):
                            ta.num += 1
                        if (ta.line + 1 == neighborTa.line and ta.col - 1 == neighborTa.col):
                            ta.num += 1
                        if (ta.line + 1 == neighborTa.line and ta.col + 1 == neighborTa.col):
                            ta.num += 1
                        if (ta.line - 1 == neighborTa.line and ta.col - 1 == neighborTa.col):
                            ta.num += 1
                        if (ta.line - 1 == neighborTa.line and ta.col + 1 == neighborTa.col):
                            ta.num += 1
                        if (ta.col + 1 == neighborTa.col and ta.line == neighborTa.line):
                            ta.num += 1
                        if (ta.col - 1 == neighborTa.col and ta.line == neighborTa.line):
                            ta.num += 1


class TestApp(App):
    def build(self):
        Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
        self.title = 'based graphics'
        return Board()


TestApp().run()