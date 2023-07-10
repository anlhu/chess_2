import tkinter as tk
from PIL import Image, ImageTk
from Chess import Chess
from Card import CardCollection
from Window import Window

class GameWrapper:
    def __init__(self):
        self.selecting = True
        self.card_selecting = False
        self.team = 'w'
        self.turn_count = 1
        self.captures = {'w':[], 'b':[]}
        self.points = {'w':0, 'b':0}
        self.cards = {'w':[None, None, None], 'b':[None, None, None]}
        self.collection = CardCollection(self)
        self.window = Window(self.board_click, self.card_click)
        self.window.start_loop()

    def draw_card(self):
        for i in range(3):
            if self.cards[self.team][i] is None:
                self.cards[self.team][i] = self.collection.draw()
                self.window.draw_card(self.team, i, self.cards[self.team][i])
                break

    def board_click(self, window, index):
        if self.card_selecting is not False:
            success = self.card_selecting(self, window, index)
            self.card_selecting = False if success else self.card_selecting
            return

        if self.selecting is True:
            if window.get_piece(index) and window.get_piece(index).team != self.team:
                return
            moves = window.get_moves(index)
            if not moves[0] and not moves[1]:
                return
            window.draw_decor(moves)
            self.selecting = index
        else:
            if index == self.selecting:
                return
            window.remove_decor()
            if not window.chess.valid(self.selecting, index):
                self.selecting = True
                self.board_click(window, index)
                return
            cap, promote = window.move(self.selecting, index)
            self.points[self.team] += 1

            self.captures[self.team].extend(cap)
            for piece, loc in cap:
                self.points[self.team] += piece.points
                if piece.name == "King":
                    window.win('Black' if self.team=='b' else 'White')
                    return True
            
            if promote:
                window.promote(index)
            window.update_scores(self.points)
            self.draw_card()
            self.team = 'b' if self.team=='w' else 'w'
            self.turn_count += 1
            self.selecting = True
            return True

    def card_click(self, window, index):
        side = 'w' if index <= 4 else 'b'
        slot = (index-2)%3 + 1
        index = slot-1
        if self.team != side:
            return
        if self.cards[self.team][index] is None:
            return
        if self.cards[self.team][index].cost > self.points[self.team]:
            return
        if self.card_selecting is not False:
            return
        card = self.cards[self.team][index]
        self.cards[self.team][index] = None
        self.points[self.team] -= card.cost
        window.remove_decor()
        self.selecting = True
        card.funct()
        self.window.destroy_card(self.team, index)
        self.window.update_scores(self.points)

GW = GameWrapper()