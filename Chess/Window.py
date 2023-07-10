import tkinter as tk
from PIL import Image, ImageTk
from Chess import Chess
import os

class Window:
    def __init__(self, function, card_function):
        self.chess = Chess()
        self.decor = []
        self.card_slots = {'b':[None, None, None], 'w':[None, None, None]}
        self.card_slot_card = {'b':[None, None, None], 'w':[None, None, None]}

        self.window, self.windowW, self.windowH = self.create_window()
        self.frame, self.frameS, self.frameP = self.create_frame()     
        self.create_slots()
        piece_list = ["Queen", "Bishop", "Knight", "Rook", "King", "Pawn"]
        self.card_pics = {file[:-4] : ImageTk.PhotoImage(Image.open(f"Cards/{file}").resize((self.frameS//8,self.frameS//8))) for file in os.listdir("Cards")}
        self.p_dict  = {f"w{piece}" : ImageTk.PhotoImage(Image.open(f"Pieces/Standard/w{piece}.png").resize((9*self.frameS//80,9*self.frameS//80))) for piece in piece_list} 
        self.p_dict |= {f"b{piece}" : ImageTk.PhotoImage(Image.open(f"Pieces/Standard/b{piece}.png").resize((9*self.frameS//80,9*self.frameS//80))) for piece in piece_list} 
        self.p_dict |= {'0' : ImageTk.PhotoImage(Image.open("Extra/blank.png"))}
        self.o_list = [ImageTk.PhotoImage(Image.open("Extra/dot.png").resize((9*self.frameS//80,9*self.frameS//80))), ImageTk.PhotoImage(Image.open("Extra/red.png").resize((9*self.frameS//80,9*self.frameS//80))), ImageTk.PhotoImage(Image.open("Extra/target.png").resize((9*self.frameS//80,9*self.frameS//80)))]
        self.board_list = self.create_board()
        self.window.bind("<Button 1>", self.get_click)
        self.function = function
        self.card_fuction = card_function
    def start_loop(self):
        self.window.mainloop()
    def create_window(self):
        window = tk.Tk()
        window.title("Super Chess")
        screenW, screenH = window.winfo_screenwidth(), window.winfo_screenheight() 
        windowW = screenW*4//5
        windowH = windowW*1080//1920
        window.geometry(f"{windowW}x{windowH}+{screenW//2-windowW//2}+{screenH//2-windowH//2-windowH//20}")
        # window.resizable(False,False)
        window.iconbitmap('Icon.ico')
        window.configure(bg="#c2c2c2")
        return window, windowW, windowH
    def create_frame(self):
        frame = tk.Frame(self.window, bg="#333231")
        num=16
        denom=num+1
        padding=(self.windowH-self.windowH*num//denom)//2
        frameH=self.windowH*num//denom
        frame.place(relx=1080/1920*1/34, rely=1/34, relheight=16/17, relwidth=1080/1920*16/17)
        # frame.place(x=padding, y=padding, height=frameH, width=frameH)
        return frame, frameH, padding
    def create_slots(self):
        self.frame_pos_x = 1080/1920*1/34
        self.frame_w = 1080/1920*16/17
        self.frame_pos_y = 1/34
        self.frame_h = 16/17
        remaining_width = 1-self.frame_pos_x-self.frame_w
        use_width = remaining_width-self.frame_pos_x*2
        self.slot_width = use_width*32/99
        extra_width = (use_width-3*self.slot_width)/2

        for s in range(3):
            slot = tk.Frame(self.window, bg="#333231")
            slot.place(relx=self.frame_w+2*self.frame_pos_x+s*(self.slot_width+extra_width), rely=self.frame_pos_y+self.frame_h-self.slot_width*2.66, relwidth=self.slot_width, relheight=self.slot_width*2.66)
            # slot.place(x=self.frameS+self.frameP+self.frameP+s*(slot_width+extra_width), y=self.frameP+self.frameS-slot_width*3//2, width=slot_width, height=slot_width*3//2)
            self.card_slots['w'][s] = slot
        for s in range(3):
            slot = tk.Frame(self.window, bg="#333231")
            # slot.place(x=self.frameS+self.frameP+self.frameP+s*(slot_width+extra_width), y=self.frameP, width=slot_width, height=slot_width*3//2)
            slot.place(relx=self.frame_w+2*self.frame_pos_x+s*(self.slot_width+extra_width), rely=self.frame_pos_y, relwidth=self.slot_width, relheight=self.slot_width*2.66)
            self.card_slots['b'][s] = slot

        self.white_pts = tk.Label(self.window, text="0", font=('Helvetica bold', 14), bg="#c2c2c2")
        self.white_pts.place(relx=self.frame_w+2*self.frame_pos_x, rely=self.frame_pos_y+self.frame_h-self.slot_width*3.05)
        self.black_pts = tk.Label(self.window, text="0", font=('Helvetica bold', 14), bg="#c2c2c2")
        self.black_pts.place(relx=self.frame_w+2*self.frame_pos_x, rely=self.frame_pos_y+self.slot_width*2.66)
    def create_board(self):
        frame_padding = self.frameS//20
        # squareS = (self.frameS - 2*frame_padding)//8
        board_list = []
        for r in range(8):
            for c in range(8):
                color = "#66bd90" if (r+c)%2 else "#dbb54b"
                board = tk.Canvas(self.frame, bg=color, highlightthickness=1)
                board.place(relx=(500+c*1125)/10000, rely=0.05+r*0.1125, relheight=0.1125, relwidth=0.1125)
                # board.place(x=frame_padding+c*squareS, y=frame_padding+r*squareS, height=squareS, width=squareS)
                board_list.append(board)
                board.create_image(0, 0, anchor="nw", image=self.p_dict[str(self.chess[(c,r)])])
        return board_list

    def get_piece(self, index):
        return self.chess[index]
    def get_moves(self, index):
        return self.chess.get_moves(index)

    def get_click(self, event):
        if str(event.widget) == ".":
            return
        f_names = str(event.widget).split(".!")[1:]
        if f_names[0] == "frame" and len(f_names) == 2:
            num = int(f_names[1][6:])-1 if f_names[1][6:] != '' else 0
            self.function(self, num)
        elif f_names[0][:-1] == "frame" and 1 < int(f_names[0][-1]) <= 7:
            self.card_fuction(self, int(f_names[0][-1]))
    
    def update_place(self, index):
        self.board_list[index].delete('all')
        self.board_list[index].create_image(0, 0, anchor="nw", image=self.p_dict[str(self.chess[index])])
    def move_visual(self, start, end):
        self.board_list[start].delete('all')
        self.board_list[end].delete('all')
        self.board_list[end].create_image(0, 0, anchor="nw", image=self.p_dict[str(self.chess[end])])
    def draw_decor(self, moveList):
        for i in range(2):
            for m in moveList[i]:
                self.board_list[m.toIndex()].create_image(0, 0, anchor="nw", image=self.o_list[i])
                self.decor.append(m)
    def remove_decor(self):
        for d in self.decor:
            self.update_place(d.toIndex())
    def update_scores(self, dict):
        self.black_pts.destroy()
        self.white_pts.destroy()
        self.white_pts = tk.Label(self.window, text=f"{dict['w']}", font=('Helvetica bold', 14), bg="#c2c2c2")
        self.white_pts.place(relx=self.frame_w+2*self.frame_pos_x, rely=self.frame_pos_y+self.frame_h-self.slot_width*3.05)
        self.black_pts = tk.Label(self.window, text=f"{dict['b']}", font=('Helvetica bold', 14), bg="#c2c2c2")
        self.black_pts.place(relx=self.frame_w+2*self.frame_pos_x, rely=self.frame_pos_y+self.slot_width*2.66)

    def move(self, start, end):
        captured, promote = self.chess.make_move(start, end)
        self.move_visual(start, end)
        for piece, location in captured:
            self.update_place(location.toIndex())
        if self.chess[end].name == "King" and abs(end-start)==2:
            self.chess.make_move(end+1, end-1)
            self.update_place(end-1)
            self.update_place(end+1)
        return captured, promote
    def promote(self, location):
        ops = ["Rook", "Knight", "Bishop", "Queen"]
        def select(event):
            s = str(event.widget)[-1]
            pick = ops[int(s)-1] if s != 's' else "Rook"
            self.chess.promote(location, pick)
            self.update_place(location)
            canvas.destroy()
            self.window.bind("<Button 1>", self.get_click)

        canvas = tk.Canvas(self.frame, bg="#267abf", highlightthickness=3)
        pad = self.frameS//20
        sq = (self.frameS - 2*pad)//8
        rows = (len(ops)-1)//4 + 1
        h, w = sq*5*rows//4, sq*(len(ops)+1)
        canvas.place(x=pad+4*sq-w//2, y=pad+4*sq-h//2, height=h, width=w)
        team = self.chess[location].team
        for i, option in enumerate(ops):
            piece = tk.Canvas(canvas, bg="#267abf", highlightthickness=0)
            piece.place(x=i*sq+(i+1)*sq//(len(ops)+1), y=h//2-sq//2+sq*(i//4), height=sq, width=sq)
            piece.create_image(0, 0, anchor="nw", image=self.p_dict[team+option])
            self.window.bind("<Button 1>", lambda event:None)
            piece.bind("<Button 1>", select)
    def win(self, winner):
        self.window.bind("<Button 1>", lambda event:None)
        l = tk.Label(self.window, bg="#267abf", text=f"{winner} wins!", font=('Helvetica bold', 26), relief="ridge", fg=winner)
        h, w = self.windowH//10, 2*self.windowW//10
        l.place(x=self.windowW//2-w//2, y=self.windowH//2-h//2, height=h, width=w)

    def draw_card(self, team, index, card):
        blank = self.card_slots[team][index]
        slot = tk.Canvas(blank, bg=card.bgColor, highlightthickness=1)
        self.card_slot_card[team][index] = slot
        # slot.create_image(0, 0, anchor="nw", image=img)
        slot.create_image(0, 0, anchor="nw", image=self.card_pics[card.name])
        slot.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
        title = tk.Label(slot, text=card.name.replace("_", ' '), font=('Helvetica bold', 12), bg=card.bgColor)
        title.place(relx=0, rely=0.5)
        cost = tk.Label(slot, text="Cost: "+str(card.cost), font=('Helvetica bold', 12), bg=card.bgColor)
        cost.place(relx=0, rely=0.7)
    
    def destroy_card(self, team, index):
        self.card_slot_card[team][index].delete("all")
        self.card_slot_card[team][index].destroy()
        self.card_slot_card[team][index] = None
