from tkinter import *
import random


class Board:
    bg_color = {'2': '#eee4da', '4': '#ede0c8', '8': '#edc850', '16': '#edc53f', '32': '#f67c5f',
                '64': '#f65e3b', '128': '#edcf72', '256': '#edcc61', '512': '#f2b179', '1024': '#f59563',
                '2048': '#edc22e'}
    color = {'2': '#776e65', '4': '#f9f6f2', '8': '#f9f6f2', '16': '#f9f6f2', '32': '#f9f6f2',
             '64': '#f9f6f2', '128': '#f9f6f2', '256': '#f9f6f2', '512': '#776e65', '1024': '#f9f6f2',
             '2048': '#f9f6f2'}

    def __init__(self):
        self.n = 4
        self.mainwindow = Tk()
        self.mainwindow.title('2048 Game')
        self.gameArea = Frame(self.mainwindow, bg='azure3')
        self.board = []
        self.gridCell = [[0] * 4 for i in range(4)]
        self.compressed = False
        self.merged = False
        self.moved = False
        self.score = 0
        for i in range(4):
            rows = []
            for j in range(4):
                l = Label(self.gameArea, text='', bg='azure4',
                          font=('arial', 22, 'bold'), width=4, height=2)
                l.grid(row=i, column=j, padx=7, pady=7)
                rows.append(l);
            self.board.append(rows)
        self.gameArea.grid()

    def reverse(self):
        for ind in range(4):
            i = 0
            j = 3
            while (i < j):
                self.gridCell[ind][i], self.gridCell[ind][j] = self.gridCell[ind][j], self.gridCell[ind][i]
                i += 1
                j -= 1

    def transpose(self):
        self.gridCell = [list(t) for t in zip(*self.gridCell)]

    def compressGrid(self):
        self.compressed = False
        temp = [[0] * 4 for i in range(4)]
        for i in range(4):
            count = 0
            for j in range(4):
                if self.gridCell[i][j] != 0:
                    temp[i][count] = self.gridCell[i][j]
                    if count != j:
                        self.compressed = True
                    count += 1
        self.gridCell = temp

    def mergeGrid(self):
        self.merged = False
        for i in range(4):
            for j in range(4 - 1):
                if self.gridCell[i][j] == self.gridCell[i][j + 1] and self.gridCell[i][j] != 0:
                    self.gridCell[i][j] *= 2
                    self.gridCell[i][j + 1] = 0
                    self.score += self.gridCell[i][j]
                    self.merged = True

    def randomcell(self):
        cells = []
        for i in range(4):
            for j in range(4):
                if self.gridCell[i][j] == 0:
                    cells.append((i, j))
        current = random.choice(cells)
        i = current[0]
        j = current[1]
        self.gridCell[i][j] = 2

    def can_merge(self):
        for i in range(4):
            for j in range(3):
                if self.gridCell[i][j] == self.gridCell[i][j + 1]:
                    return True

        for i in range(3):
            for j in range(4):
                if self.gridCell[i + 1][j] == self.gridCell[i][j]:
                    return True
        return False

    def paintgrid(self):
        for i in range(4):
            for j in range(4):
                if self.gridCell[i][j] == 0:
                    self.board[i][j].config(text='', bg='azure4')
                else:
                    self.board[i][j].config(text=str(self.gridCell[i][j]),
                                            bg=self.bg_color.get(str(self.gridCell[i][j])),
                                            fg=self.color.get(str(self.gridCell[i][j])))


class Game:
    def __init__(self, gamepanel):
        self.gamepanel = gamepanel
        self.end = False
        self.won = False

    def start(self):
        self.gamepanel.randomcell()
        self.gamepanel.randomcell()
        self.gamepanel.paintgrid()
        self.gamepanel.mainwindow.bind('<Key>', self.linkkeys)
        self.gamepanel.mainwindow.mainloop()

    def linkkeys(self, event):
        if self.end or self.won:
            return
        self.gamepanel.compressed = False
        self.gamepanel.merged = False
        self.gamepanel.moved = False
        presedkey = event.keysym
        if presedkey == 'Up':
            self.gamepanel.transpose()
            self.gamepanel.compressGrid()
            self.gamepanel.mergeGrid()
            self.gamepanel.moved = self.gamepanel.compressed or self.gamepanel.merged
            self.gamepanel.compressGrid()
            self.gamepanel.transpose()
        elif presedkey == 'Down':
            self.gamepanel.transpose()
            self.gamepanel.reverse()
            self.gamepanel.compressGrid()
            self.gamepanel.mergeGrid()
            self.gamepanel.moved = self.gamepanel.compressed or self.gamepanel.merged
            self.gamepanel.compressGrid()
            self.gamepanel.reverse()
            self.gamepanel.transpose()
        elif presedkey == 'Left':
            self.gamepanel.compressGrid()
            self.gamepanel.mergeGrid()
            self.gamepanel.moved = self.gamepanel.compressed or self.gamepanel.merged
            self.gamepanel.compressGrid()
        elif presedkey == 'Right':
            self.gamepanel.reverse()
            self.gamepanel.compressGrid()
            self.gamepanel.mergeGrid()
            self.gamepanel.moved = self.gamepanel.compressed or self.gamepanel.merged
            self.gamepanel.compressGrid()
            self.gamepanel.reverse()
        else:
            pass
        self.gamepanel.paintgrid()
        print(self.gamepanel.score)
        flag = 0
        for i in range(4):
            for j in range(4):
                if (self.gamepanel.gridCell[i][j] == 2048):
                    flag = 1
                    break
        if (flag == 1):  # found 2048
            self.won = True
            messagebox.showinfo('2048', message='You Wonnn!!')
            print("won")
            return
        for i in range(4):
            for j in range(4):
                if self.gamepanel.gridCell[i][j] == 0:
                    flag = 1
                    break
        if not (flag or self.gamepanel.can_merge()):
            self.end = True
            messagebox.showinfo('2048', 'Game Over!!!')
            print("Over")
        if self.gamepanel.moved:
            self.gamepanel.randomcell()

        self.gamepanel.paintgrid()


gamepanel = Board()
game2048 = Game(gamepanel)
game2048.start()
