from .hex import Hex
from .piece import Piece
from .board import Board

                    # (q,r)
ITERATIVE_MOVES = { [0,1],[1,0],
                    [-1,0],[-1,1],
                    [0,-1],[1,-1]
                    }

class Beetles(Piece):
    count = 2

    def __init__(self,difficulty:int ):
        self.difficulty = difficulty
        
    """ 
    my_moves = []

    Check on the board if there is a queen with same type of beetle:
     Queen_Placed=true: beetle can move if it is already placed
     Queen_Placed=false: beetle can't move OR if it is not placed find legal moves by looping over the board using BFS

    if this piece is placed:
        if Queen_Placed:
                loop over iterative moves:
                    add iterative moves to currenthex
                    loop over board:
                        if a piece found with same hex: (Go on top of another piece regardless of its color)
                            push new hex to my_moves
                    else if new hex has no piece :
                        valid = 0
                        for each move from this new hex in iterative moves:
                            if it has a piece :
                                valid = 1
                        if valid:
                           push newhex to my_moves 
    else : (Not placed)
        if board is at initial state (black_pieces_placed == white_pieces_placed == 0):
            return (0,0,0)
        else if board has one play (ex: currentpiece is white , there is 1 black_pieces_placed && 0 white_pieces_placed) 
            loop over iterative moves and push all
        else: (in middle of game)
            for each piece in board:
                if piece color not same as current OR piece is at its initial state:
                    pass
                else
                    loop over iterative moves:
                        add iterative moves to piece hex
                        if new hex has a same color piece :
                            pass
                        else if new hex has no piece :
                            valid = 1
                            for each move in iterative moves:
                                if any has a piece with pieceColor not same as beetle :
                                    valid = 0
                            if valid:
                                push newhex to my_moves
                         
              
    """

    

    def get_legal_moves(self,board:Board):
       
        legal_moves = []
        # just to know initial state of this piece
        initialHex = None
        if(self.piece_type == "white"):
            initialHex = Hex(8,-2)
        else:
            initialHex = Hex(-8,6)
        isQueenPlaced = self.__isQueenPlaced(board)

        current_Hex = self.hex
    
        
        # Algorithm
        
        # If this piece is placed:
        if(self.is_placed):
            # if Queen_Placed:
            if(isQueenPlaced):
                # loop over iterative moves:
                for move in ITERATIVE_MOVES:
                    # add iterative moves to currenthex
                    new_Hex = Hex(current_Hex.q + move[0],current_Hex.r + move[1])
                    #  if a piece found with same hex: (Go on top of another piece regardless of its color)
                    if(self.__isPieceFound(board,new_Hex)):
                        
                        legal_moves.append(new_Hex)        
                    #else if new hex has no piece 
                    else:
                        # for each move from the new hex in iterative moves
                        for m in ITERATIVE_MOVES:
                            
                            hexadjacent = Hex(new_Hex.q + m[0],new_Hex.r + m[1])
                            # if it has a piece
                            
                            if (self.__isPieceFoundAndNotSame(board,hexadjacent) ):
                            #    push newhex to my_moves
                                legal_moves.append(new_Hex)    
        else: # Not placed
            # if board is at initial state (black_pieces_placed == white_pieces_placed == 0):
            if(board.is_first_move == False):
                # return (0,0,0)     
                legal_moves.append(Hex(0,0))  
            # else if board has one play (ex: currentpiece is white , there is 1 black_pieces_placed && 0 white_pieces_placed)
            elif(self.__hasOnePlay(board)): 
                # loop over iterative moves and push all
                for move in ITERATIVE_MOVES:
                    new_Hex = Hex(board.board[0].hex.q + move[0],board.board[0].hex.r + move[1])
                    legal_moves.append(new_Hex)

            else:   # in middle of game
                # for each piece in board:
                for piece in board.board:
                    # if piece color not same as current OR piece is at its initial state:
                    if(piece.piece_type != self.piece_type or piece.is_placed== False):
                        pass
                    else:
                        # loop over iterative moves:
                        for m in ITERATIVE_MOVES:
                            # add iterative moves to piece hex
                            new_Hex = Hex(piece.hex.q + m[0],piece.hex.r + m[1])
                            # if new hex has no piece :
                            if(self.__isPieceFound(board,new_Hex) == False):
                                
                            #   for each move in iterative moves:
                                for x in ITERATIVE_MOVES:
                                    valid = 0
                            #       if any has a piece with pieceColor not same as beetle :
                                    hexadjacent = Hex(new_Hex.q + x[0],new_Hex.r + x[1])
                            #                 
                                    for piece in board.board:
                                        # get piece with same hex 
                                        if(piece.hex == new_Hex and piece.piece_type != self.piece_type): # not sure about syntax
                                            valid = 1
                                    if (valid):
                                        #  push newhex to my_moves
                                        legal_moves.append(new_Hex)
      
        # unique_pieces = list(set(legal_pieces)) # to remove duplicates
        unique_moves = list({(p.hex.q, p.hex.r): p for p in legal_moves}.values())
        return unique_moves    
    



    """ ***************************** Helper Functions *******************************************    """
    
    def __isQueenPlaced(board:Board):
        isPlaced = False

        for piece in board.board:
            if(piece.piece_name == "queen" and piece.is_placed):
                isPlaced = True
            else:
                pass    

        return isPlaced
    
    # if board has one play (ex: currentpiece is white , there is 1 black_pieces_placed && 0 white_pieces_placed)
    def __hasOnePlay(board:Board):
        Turns = 0
        for piece in board.board:
            if(piece.is_placed):
                Turns +=1
        return (Turns == 1)

    def __isPieceFound(board:Board,new_Hex:Hex):
        for piece in board.board:
            # get piece with same hex 
            if(piece.hex == new_Hex ): # not sure about syntax
                return True
        return False                
    
    def __isPieceFoundAndNotSame(self, board:Board,new_Hex:Hex):
        for piece in board.board:
            # get piece with same hex 
            if(piece.hex == new_Hex and self is piece ): # not sure about syntax
                return True
        return False       