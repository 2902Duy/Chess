import os
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
    loadImage()
    running=True
    while running:
        for e in p.event.get():
            if e.type ==p.QUIT:
                running=False
        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen,gs):
    drawBoard(screen)
    drawPieces(screen,gs.board)

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