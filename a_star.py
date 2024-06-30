import tkinter
import tkinter.messagebox

window = tkinter.Tk()

#변수 설정
size_r = 40
size_c = 70
mode = 2
openlist = []
closelist = []
finding = 0

#모드 선택
def select_start():
    global mode
    mode = 2
def select_end():
    global mode
    mode = 3
def select_wall():
    global mode
    mode = 1

#길 찾기
def find_path():
    global finding
    finding = 1
    if Map.start != None and Map.end != None:
        dx = [0,1,1,1,0,-1,-1,-1]
        dy = [1,1,0,-1,-1,-1,0,1]
        
        openlist.append(Map.data[Map.start[0]][Map.start[1]])
        
        while openlist != 0 and Map.data[Map.end[0]][Map.end[1]] not in openlist:
            current_node = None
            temp = -1
            for i in openlist:
                if temp == -1 or i.f < temp:
                    temp = i.f
                    current_node = i
            
            current_node.addclose()

            for i in range(8):
                ax = current_node.row + dx[i]
                ay = current_node.col + dy[i]
                if 0<=ax<Map.rows and 0<=ay<Map.cols:
                    select_node = Map.data[ax][ay]
                    if select_node.state != 1 and select_node not in closelist:
                        if i%2 == 0 or Map.data[ax][current_node.col].state != 1 or Map.data[current_node.row][ay].state != 1:
                            if select_node not in openlist:
                                select_node.addopen()
                                if i%2 == 0:
                                    select_node.g = current_node.g + 10
                                else:
                                    select_node.g = current_node.g + 14
                                select_node.h = (abs(Map.end[0] - select_node.row)* 10) + (abs(Map.end[1] - select_node.col))
                                select_node.f = select_node.g + select_node.h
                                select_node.parent = current_node
                            else:
                                if (i%2 == 0 and current_node.g + 10 < select_node.g) or (i%2 == 1 and current_node.g + 14 < select_node.g):
                                    if i%2 == 0:
                                        select_node.g = current_node.g + 10
                                    else:
                                        select_node.g = current_node.g + 14
                                    select_node.f = select_node.g + select_node.h
                                    select_node.parent = current_node
        
        if Map.data[Map.end[0]][Map.end[1]] in openlist:
            current_node = Map.data[Map.end[0]][Map.end[1]]
            while current_node != Map.data[Map.start[0]][Map.start[1]]:
                if current_node != Map.data[Map.end[0]][Map.end[1]]:
                    Map.canvas.itemconfig(f"({current_node.row},{current_node.col})",fill="orange")
                current_node = current_node.parent
        else:
            tkinter.messagebox.showerror("ERROR","길을 찾을 수 없습니다.")

    else:
        tkinter.messagebox.showerror("ERROR","출발점과 도착점을 지정해주세요.")



#길 초기화
def reset_path():
    global openlist,closelist,finding
    finding = 0
    openlist = []
    closelist = []
    
    for r in range(Map.rows):
        for c in range(Map.cols):
            Map.data[r][c].reset()

#맵 초기화
def reset_map():
    global openlist,closelist,finding
    finding = 0
    openlist = []
    closelist = []
    
    for r in range(Map.rows):
        for c in range(Map.cols):
            Map.data[r][c].f = 0
            Map.data[r][c].g = 0
            Map.data[r][c].h = 0
            Map.data[r][c].parent = 0
            Map.data[r][c].state = 0
            Map.canvas.itemconfig(f"({r},{c})",fill="white")

def set_map():
    def apply_size():
        global size_r, size_c, Map
        try:
            size_r = int(entry_rows.get())
            size_c = int(entry_cols.get())
            if size_r > 0 and size_c > 0:
                new_window.destroy()
                reset_map()
                Map.canvas.destroy()
                Map = NodeMap(window, size_r, size_c, 15)
            else:
                tkinter.messagebox.showerror("ERROR", "행과 열의 값은 양수여야 합니다.")
        except ValueError:
            tkinter.messagebox.showerror("ERROR", "유효한 숫자를 입력해주세요.")
    
    new_window = tkinter.Toplevel(window)
    new_window.title("맵 크기 설정")
    
    tkinter.Label(new_window, text="행 (Rows):").pack()
    entry_rows = tkinter.Entry(new_window)
    entry_rows.pack()
    
    tkinter.Label(new_window, text="열 (Cols):").pack()
    entry_cols = tkinter.Entry(new_window)
    entry_cols.pack()
    
    tkinter.Button(new_window, text="적용", command=apply_size).pack()
    tkinter.Button(new_window, text="취소", command=new_window.destroy).pack()


class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.parent = None
        self.state = 0
        self.f = 0
        self.g = 0
        self.h = 0

    def addopen(self):
        openlist.append(Map.data[self.row][self.col])
        if Map.canvas.itemcget(f"({self.row},{self.col})","fill") != "red":
            Map.canvas.itemconfig(f"({self.row},{self.col})",fill="cyan")
            self.state = 4

    def addclose(self):
        openlist.remove(Map.data[self.row][self.col])
        closelist.append(Map.data[self.row][self.col])
        if Map.canvas.itemcget(f"({self.row},{self.col})","fill") != "green":
            Map.canvas.itemconfig(f"({self.row},{self.col})",fill="dodgerblue")
            self.state = 5
    
    def reset(self):
        if self.state == 4 or self.state == 5:
            self.state = 0
            Map.canvas.itemconfig(f"({self.row},{self.col})",fill="white")
            self.f = 0
            self.h = 0
            self.g = 0
            self.parent = None

#맵 클래스
class NodeMap:
    def __init__(self, window, rows, cols, pixel_size):
        self.rows = rows
        self.cols = cols
        self.pixel_size = pixel_size
        self.canvas = tkinter.Canvas(window, width=cols*pixel_size, height=rows*pixel_size)
        self.canvas.pack()

        for row in range(rows):
            for col in range(cols):
                x1 = col * pixel_size
                y1 = row * pixel_size
                x2 = x1 + pixel_size
                y2 = y1 + pixel_size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="white", tags=f"({row},{col})")
        
        self.data = [[Node(row,col) for col in range(cols)] for row in range(rows)]
        self.current_color = ""
        self.pre_start = None
        self.pre_end = None
        self.start = None
        self.end = None

        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<B1-Motion>", self.drag)

    def click(self, event):
        if finding == 0:
            col = event.x // self.pixel_size
            row = event.y // self.pixel_size
            if 0 <= row < self.rows and 0 <= col < self.cols:
                if mode == 1:
                    self.current_color = self.canvas.itemcget(f"({row},{col})", "fill")
                    self.change_color(row, col)
                elif mode == 2:
                    if self.pre_start and (self.pre_start[0], self.pre_start[1]) != (row, col):
                        self.canvas.itemconfig(f"({self.pre_start[0]},{self.pre_start[1]})", fill=self.pre_start[2])
                    self.pre_start = (row, col, self.canvas.itemcget(f"({row},{col})", "fill"))
                    self.change_color(row, col)
                elif mode == 3:
                    if self.pre_end and (self.pre_end[0], self.pre_end[1]) != (row, col):
                        self.canvas.itemconfig(f"({self.pre_end[0]},{self.pre_end[1]})", fill=self.pre_end[2])
                    self.pre_end = (row, col, self.canvas.itemcget(f"({row},{col})", "fill"))
                    self.change_color(row, col)

    def drag(self, event):
        if finding == 0:
            col = event.x // self.pixel_size
            row = event.y // self.pixel_size
            if 0 <= row < self.rows and 0 <= col < self.cols:
                if mode == 1:
                    self.change_color(row, col)
                elif mode == 2:
                    if self.pre_start and (self.pre_start[0], self.pre_start[1]) != (row, col):
                        self.canvas.itemconfig(f"({self.pre_start[0]},{self.pre_start[1]})", fill=self.pre_start[2])
                        self.pre_start = (row, col, self.canvas.itemcget(f"({row},{col})", "fill"))
                        self.change_color(row, col)
                elif mode == 3:
                    if self.pre_end and (self.pre_end[0], self.pre_end[1]) != (row, col):
                        self.canvas.itemconfig(f"({self.pre_end[0]},{self.pre_end[1]})", fill=self.pre_end[2])
                        self.pre_end = (row, col, self.canvas.itemcget(f"({row},{col})", "fill"))
                        self.change_color(row, col)

    def change_color(self, row, col):
        if mode == 1:
            if self.current_color == "black":
                self.data[row][col].state = 0
                self.canvas.itemconfig(f"({row},{col})", fill="white")
            elif self.current_color == "white":
                self.data[row][col].state = 1
                self.canvas.itemconfig(f"({row},{col})", fill="black")
        elif mode == 2:
            self.data[row][col].state = 2
            self.canvas.itemconfig(f"({row},{col})", fill="green")
            self.start = (row,col)
        elif mode == 3:
            self.data[row][col].state = 3
            self.canvas.itemconfig(f"({row},{col})", fill="red")
            self.end = (row,col)

#맵 설정
Map = NodeMap(window, size_r, size_c, 15)

# tkinter setting
window.title("A* 구현")
window.resizable(False, False)

menubar = tkinter.Menu(window)
menu1 = tkinter.Menu(menubar, tearoff=0)
menu1.add_command(label="start", command=select_start)
menu1.add_command(label="end", command=select_end)
menu1.add_command(label="wall", command=select_wall)
menubar.add_cascade(label="Mode", menu=menu1)

menu2 = tkinter.Menu(menubar, tearoff=0)
menu2.add_command(label="Path Find",command=find_path)
menu2.add_command(label="Reset Path",command=reset_path)
menu2.add_command(label="Reset Map",command=reset_map)
menu2.add_separator()
menu2.add_command(label="Set Map",command=set_map)
menubar.add_cascade(label="Menu", menu=menu2)

window.config(menu=menubar)

window.mainloop()