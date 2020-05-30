import cursor
from PIL import Image

class TerminalCanvas:
    def __init__(self, rows, cols, arender=True, empty=' '):
        self.cols = cols
        self.rows = rows
        self.data = []
        self.arender = arender
        self.empty = empty
        self.clear()
    
    def autoRender(self):
        if(self.arender == True):
            self.render()

    def render(self):
        z = 0
        print("\033c", end="")
        cursor.hide()
        try:
            for y in range(self.rows):
                for x in range(self.cols):
                    print(self.data[z], end="")
                    z = z + 1
                print("\n",end="")
        except:
            cursor.show()

    def clear(self):
        self.data.clear()
        for i in range(self.rows*self.cols):
            self.data.append(self.empty)
        self.autoRender()

    def insertRow(self, row, row_data, offset=0):  
        if(type(row_data) is list or type(row_data) is tuple):
            row_arr = row_data
        else:
            row_arr = list(row_data)

        for i in range(len(row_arr)):
            self.data[i+(self.cols * row)+offset] = row_arr[i]
        self.autoRender()

    def insertCol(self, col, col_data, offset=0):
        if(type(col_data) is list or type(col_data) is tuple):
            col_arr = col_data
        else:
            col_arr = list(col_data)

        for i in range(self.rows):
            try:
                self.data[(i+offset) * self.cols + col] = col_arr[i]
            except:
                break
        self.autoRender()

    def setChar(self, row, col, char):
        self.data[(self.cols*row) + col] = char
        self.autoRender()

    def getChar(self, row, col):
        return self.data[(self.cols*row) + col]

    def getRow(self, row):
        return_data = []
        for i in range(self.cols):
            return_data.append(self.data[(row * self.cols) + i])
        return return_data

    def getCol(self, col):
        return_data = []
        for i in range(self.rows):
            return_data.append(self.data[i * self.cols + col])
        return return_data

    def drawImage(self, path, mode="_bg", char=' ', size=(10,10)):
        trender = self.arender
        self.arender = False
        image = Image.open(path)
        image = image.resize((size[1], size[0]), Image.ANTIALIAS)
        if((size[0] * size[1]) > (self.cols * self.rows)):
            self.resize(size[0], size[1])
        for x in range(size[1]):
            for y in range(size[0]):
                pixel = image.getpixel((x, y))
                r = pixel[0]
                g = pixel[1]
                b = pixel[2]
                if(mode == "_fg"):
                    color_char = "\x1b[38;2;%d;%d;%dm%c\x1b[0m" % (r, g, b, char)
                elif(mode == "_bg"):
                    color_char = "\x1b[48;2;%d;%d;%dm%c\x1b[0m" % (r, g, b, char)
                self.setChar(y, x, color_char)

        self.arender = trender
        self.autoRender()

    def drawBlock(self, row, col, w, h, mode="_bg", char=' ', color=(255, 255, 255)):
        trender = self.arender
        self.arender = False
        for i in range(h):
            if(mode == "_fg"):
                color_char = "\x1b[38;2;%d;%d;%dm%c\x1b[0m" % (color[0], color[1], color[2], char)
                self.insertRow(i+row, [color_char]*w, col)              
            elif(mode == "_bg"):
                color_char = "\x1b[48;2;%d;%d;%dm%c\x1b[0m" % (color[0], color[1], color[2], char)
                self.insertRow(i+row, [color_char]*w, col)
        self.arender = trender
        self.autoRender()

    def resize(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.clear()
