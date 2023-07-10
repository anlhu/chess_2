class Location:
    def __init__(self, input):
        if type(input) == tuple:
            self.row = input[1]
            self.col = input[0]
        elif type(input) == int:
            self.row = input//8
            self.col = input%8
        else:
            self.row = input.row
            self.col = input.col
    def __add__(self, other):
        row = self.row + other.row
        col = self.col + other.col
        return Location((col, row))
    def __sub__(self, other):
        row = self.row - other.row
        col = self.col - other.col
        return Location((col, row))
    def __mul__(self, constant):
        row = self.row*constant
        col = self.col*constant
        return Location((col, row))
    def toTuple(self):
        return (self.col, self.row)
    def __repr__(self):
        return f"L({self.col}, {self.row})"
    def __str__(self):
        return self.__repr__()
    def toIndex(self):
        return 8*self.row + self.col
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

class Board:
    def __init__(self, chess):
        self.board = []
        lineup = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        self.board.append([Pie('b', chess, False) for Pie in lineup])
        self.board.append([Pawn('b', chess, False) for _ in range(8)])
        for r in range(4):
            self.board.append([0 for _ in range(8)])
        self.board.append([Pawn('w', chess, False) for _ in range(8)])
        self.board.append([Pie('w', chess, False) for Pie in lineup])
    def __getitem__(self, index):
        index = Location(index)
        return self.board[index.row][index.col]
    def __setitem__(self, index, item):
        index = Location(index)
        self.board[index.row][index.col] = item
    def show(self):
        for r in self.board:
            print(r)

class Piece:
    def __init__(self, team, chess, moved):
        self.team = team
        self.chess = chess
        self.moved = moved
        self.points = 0
    def moves(self, location):
        move_list = []
        return move_list
    def __eq__(self, other):
        if type(other) != type(self):
            return False
    def __repr__(self):
        return self.team + type(self).__name__
    def __str__(self):
        return self.__repr__()

    @property
    def name(self):
        return type(self).__name__

class Pawn(Piece):
    def __init__(self, team, chess, moved):
        super().__init__(team, chess, moved)
        self.ep = False
        self.points = 1

    def moves(self, location):
        wCorrect = -1 if self.team == "w" else 1

        capture_list = []
        capture_directions = [Location((1, 1*wCorrect)), Location((-1, 1*wCorrect))]
        for dir in capture_directions:
            if self.chess[location+dir] and self.chess[location+dir].team != self.team:
                capture_list.append(location+dir)
        # fuck en passant
        en_directions = [Location((-1, 0)), Location((1, 0))]
        for dir in en_directions:
            side = self.chess[dir+location]
            if side and side.team != self.team and type(side) == Pawn and side.ep:
                capture_list.append(dir+location+Location((0, 1*wCorrect)))

        move_list = []
        forward = Location((0, 1*wCorrect))
        for dist in range(1,3):
            if self.moved and dist == 2:
                continue
            coords = location + forward*dist
            dest = self.chess[coords]
            if dest == 0:
                move_list.append(coords)
            else:
                break
        return (move_list, capture_list)

class Rook(Piece):
    def __init__(self, team, chess, moved):
        super().__init__(team, chess, moved)
        self.points = 5

    def moves(self, location):
        move_list = []
        capture_list = []
        directions = [Location((0, 1)), Location((1, 0)), Location((0, -1)), Location((-1, 0))]
        for dir in directions:
            for dist in range(1,8):
                coords = location + dir*dist
                dest = self.chess[coords]
                if dest == None:
                    break
                if dest == 0:
                    move_list.append(coords)
                    continue
                if dest.team != self.team:
                    capture_list.append(coords)
                break
        return (move_list, capture_list)

class Bishop(Piece):
    def __init__(self, team, chess, moved):
        super().__init__(team, chess, moved)
        self.points = 3

    def moves(self, location):
        move_list = []
        capture_list = []
        directions = [Location((1, 1)), Location((1, -1)), Location((-1, -1)), Location((-1, 1))]
        for dir in directions:
            for dist in range(1,8):
                coords = location + dir*dist
                dest = self.chess[coords]
                if dest == None:
                    break
                if dest == 0:
                    move_list.append(coords)
                    continue
                if dest.team != self.team:
                    capture_list.append(coords)
                break
        return (move_list, capture_list)

class Queen(Piece):
    def __init__(self, team, chess, moved):
        super().__init__(team, chess, moved)
        self.points = 9

    def moves(self, location):
        move_list = []
        capture_list = []
        directions = [Location((i,j)) for i in range(-1, 2) for j in range(-1, 2) if i!=0 or j!=0]
        for dir in directions:
            for dist in range(1,8):
                coords = location + dir*dist
                dest = self.chess[coords]
                if dest == None:
                    break
                if dest == 0:
                    move_list.append(coords)
                    continue
                if dest.team != self.team:
                    capture_list.append(coords)
                break
        return (move_list, capture_list)

class King(Piece):
    def __init__(self, team, chess, moved):
        super().__init__(team, chess, moved)
        self.points = 5

    def moves(self, location):
        move_list, capture_list = self.moves_without_castle(location)
        loc = self.castle(location, location+Location((2,0)), location+Location((3,0)), location+Location((1,0)))
        if loc:
            move_list.append(loc)
        return (move_list, capture_list)
    def castle(self, king_loc, king_end, rook_loc, rook_end):
        if self.moved == False:
            rook = self.chess[rook_loc]
            if rook and type(rook) == Rook and rook.team == self.team and rook.moved == False:
                cl = self.chess.check_list()['b' if self.team == 'b' else 'w']
                if king_loc.toTuple() not in cl:
                    if self.chess[rook_end] == 0 and rook_end.toTuple() not in cl:
                        if self.chess[king_end] == 0 and king_end.toTuple() not in cl:
                            return king_end
    def moves_without_castle(self, location):
        location = Location(location)
        move_list = []
        capture_list = []
        directions = [Location((i,j)) for i in range(-1, 2) for j in range(-1, 2) if i!=0 or j!=0]
        for dir in directions:
            coords = location + dir
            dest = self.chess[coords]
            if dest == 0:
                move_list.append(coords)
            if dest and dest.team != self.team:
                capture_list.append(coords)
        return (move_list, capture_list)

class Knight(Piece):
    def __init__(self, team, chess, moved):
        super().__init__(team, chess, moved)
        self.points = 3

    def moves(self, location):
        move_list = []
        capture_list = []
        directions = [Location((i,j)) for i in range(-2, 3) for j in range(-2, 3) if abs(i)!=abs(j) and i!=0 and j!=0]
        for dir in directions:
            coords = location + dir
            dest = self.chess[coords]
            if dest == 0:
                move_list.append(coords)   
            elif dest and dest.team != self.team:
                capture_list.append(coords)
        return (move_list, capture_list)

class Chess:
    def __init__(self):
        self.board = Board(self)
        self.ep = None
    def get_moves(self, index):
        index = Location(index)
        get = self[index]
        if not get:
            return [[], []]
        return get.moves(index)
    def valid(self, start, end):
        moves = self.get_moves(Location(start))
        return Location(end) in moves[0] or Location(end) in moves[1]
    def __getitem__(self, location):
        location = Location(location)
        if location.row < 0 or location.col < 0 or location.row > 7 or location.col > 7:
            return None
        return self.board[location]
    def pawn_stuff(self, piece, start, end):
        if self.ep:
            self.ep.ep = False
        self.ep = None
        if abs((end-start).row) == 2:
            piece.ep = True
            self.ep = piece
        elif abs((end-start).col) == 1 and self.board[end] == 0:
            cap_location = Location((end.col, start.row))
            capped = self.board[cap_location]
            self.board[cap_location] = 0
            return [(capped, cap_location)]
        return []
    def castle_move(self, rook_loc, end_rook_loc):
        self.board[end_rook_loc] = self.board[rook_loc]
        self.board[rook_loc] = 0
    def make_move(self, start, end):
        capture = []
        promote = False
        start = Location(start)
        end = Location(end)
        piece = self[start]
        if type(piece) == Pawn:
            promote = piece.team == 'w' and end.row == 0 or piece.team == 'b' and end.row == 7
            capture.extend(self.pawn_stuff(piece, start, end))
        if self.board[end] != 0:
            capture.append((self.board[end], end))
        self.board[start] = 0
        self.board[end] = piece
        piece.moved = True
        return capture, promote
    def promote(self, location, choice):
        location = Location(location)
        lineup = {"Rook": Rook, "Knight" : Knight, "Bishop" : Bishop, "Queen" : Queen}
        self.board[location] = lineup[choice](self.board[location].team, self, True)
    def check_list(self):
        checked_squares = {'b' : set(), 'w': set()}
        for i in range(64):
            piece = self[i]
            if type(piece) == King:
                for attackable in piece.moves_without_castle(i)[1]:
                    checked_squares[piece.team].add(attackable.toTuple())
            else:
                for attackable in self.get_moves(i)[1]:
                    checked_squares[piece.team].add(attackable.toTuple())
        return checked_squares
    def show(self):
        self.board.show()