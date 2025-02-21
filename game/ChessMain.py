import os
from calendar import month
from tkinter.font import names

import pygame as p

from game import ChessEngine

p.display.set_caption("Cờ vua")
WIDTH=HEIGHT=512
DIMENSION=8
SQUARE_SIZE=HEIGHT// DIMENSION
MAX_FPS=15
IMAGES ={}

piece_names = ['bB', 'bK', 'bN', 'bP', 'bQ', 'bR', 'wB', 'wK', 'wN', 'wP', 'wQ', 'wR']
def loadImage():
    for name in piece_names:
        IMAGES[name]= p.transform.scale(
            p.image.load(os.path.join("images/", f"{name}.png"))
            ,(SQUARE_SIZE,SQUARE_SIZE)
        )



def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves=gs.getValidMoves()
    moveMade =False
    loadImage()
    running=True
    sqSelected=()
    playerClicks=[]
    while running:
        for e in p.event.get():
            if e.type ==p.QUIT:
                running=False
            elif e.type== p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col=location[0]//SQUARE_SIZE
                row=location[1]//SQUARE_SIZE
                if sqSelected==(row,col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected=(row,col)
                    playerClicks.append(sqSelected)
                if len(playerClicks)==2:
                    move = ChessEngine.Move(playerClicks[0],playerClicks[1],gs.board)

                    if move in validMoves:
                        player = "white" if gs.whiteToMove else "black"
                        print(player + ":" + move.getChessNotation())
                        gs.makeMove(move)
                        moveMade=True
                        sqSelected=()
                        playerClicks = []

                    else:
                        playerClicks= [sqSelected]
            elif e.type==p.KEYDOWN:
                if e.key ==p.K_z:
                    gs.undoMove()
                    moveMade = True
        if moveMade:
            validMoves= gs.getValidMoves()
            moveMade=False
        drawGameState(screen,gs,validMoves, sqSelected)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen,gs,validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen,gs.board)

def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():  # Kiểm tra nếu đã chọn ô
        r, c = sqSelected
        if gs.board[r][c] != "__" and (gs.board[r][c][0] == ("w" if gs.whiteToMove else "b")):
            # Tạo hiệu ứng chọn quân cờ
            s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100)  # Độ trong suốt
            s.fill(p.Color("yellow"))
            screen.blit(s, (c * SQUARE_SIZE, r * SQUARE_SIZE))

            # Kiểm tra nếu đang bị chiếu
            inCheck = gs.incheck()

            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
                    s.set_alpha(150)  # Độ trong suốt
                    endPiece = gs.board[move.endRow][move.endCol]
                    if endPiece != "__" and endPiece[0] != ("w" if gs.whiteToMove else "b"):
                        s.fill(p.Color(BRIGHTRED))  # Nếu là nước ăn quân, tô màu đỏ
                    elif inCheck:
                        s.fill(p.Color(BRIGHTRED))  # Nếu đang bị chiếu, tô màu đỏ
                    else:
                        s.fill(p.Color(SKYBLUE))  # Bình thường, tô màu xanh dương
                    screen.blit(s, (move.endCol * SQUARE_SIZE, move.endRow * SQUARE_SIZE))
            # Kiểm tra nếu vua bị chiếu và tô màu đỏ
            whiteKingPos, blackKingPos = gs.whiteKingLocation, gs.blackKingLocation
            whiteInCheck = gs.squareUnderAttack(whiteKingPos[0], whiteKingPos[1])
            blackInCheck = gs.squareUnderAttack(blackKingPos[0], blackKingPos[1])

            if whiteInCheck:
                s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
                s.set_alpha(200)
                s.fill(p.Color(BRIGHTRED))  # Luôn tô đỏ nếu vua trắng bị chiếu
                screen.blit(s, (whiteKingPos[1] * SQUARE_SIZE, whiteKingPos[0] * SQUARE_SIZE))

            if blackInCheck:
                s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
                s.set_alpha(200)
                s.fill(p.Color(BRIGHTRED))  # Luôn tô đỏ nếu vua đen bị chiếu
                screen.blit(s, (blackKingPos[1] * SQUARE_SIZE, blackKingPos[0] * SQUARE_SIZE))

BRIGHTRED=(235, 64, 52)
SKYBLUE=(52, 180, 235)
BROWN = (184, 139, 74)
BEIGE = (227, 193, 111)
def drawBoard(screen):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = BROWN if (row + col) % 2 == 0 else BEIGE
            p.draw.rect(screen, color, p.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def drawPieces(screen,board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != '__':
                screen.blit(IMAGES[piece],p.Rect(col*SQUARE_SIZE,row*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))

if __name__ =="__main__":
    main()