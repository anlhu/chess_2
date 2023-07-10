import tkinter as tk
from PIL import Image, ImageTk

class Card:
    def __init__(self, wrapper, cost, col="#ec03fc"):
        self.wrapper = wrapper
        self.team = wrapper.team
        self.cost = cost
        self.bgColor = col

    def funct(self):
        pass
    
    @property
    def name(self):
        return type(self).__name__

class Double_Points(Card):
    def funct(self):
        self.wrapper.points[self.wrapper.team] *= 2

class Promote_Piece(Card):
    def funct(self):
        def promote_piece(wrap, window, index):
            piece = window.get_piece(index)
            if not piece or piece.team != wrap.team or piece.name == "King":
                return False
            window.promote(index)
            return True
        self.wrapper.card_selecting = promote_piece
        
class Skip(Card):
    def funct(self):
        def skip(wrap, window, index):
            f = wrap.card_selecting
            wrap.card_selecting = False
            r = wrap.board_click(window, index)
            if r is True:
                wrap.team = 'b' if wrap.team=='w' else 'w'
                wrap.turn_count -= 1
                return True
            wrap.card_selecting = f
            return False
        self.wrapper.card_selecting = skip

import random

class CardCollection:
    def __init__(self, w):
        self.collection = [Double_Points(w, 5, col="#fcdb00"), Promote_Piece(w, 10, col="#4287f5"), Skip(w, 1, col="#298c43")]
        self.probabilities = [0.3, 0.3, 0.4]
        assert 0 <= sum(self.probabilities) <= 1

    def draw(self):
        p = random.random()
        probability = 0
        for i in range(len(self.collection)):
            probability += self.probabilities[i]
            if p < probability:
                return self.collection[i]
