from operator import truediv


class GameState():
    def __init__(self):
        self.board=[
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['__', '__', '__', '__', '__', '__', '__', '__'],
            ['__', '__', '__', '__', '__', '__', '__', '__'],
            ['__', '__', '__', '__', '__', '__', '__', '__'],
            ['__', '__', '__', '__', '__', '__', '__', '__'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]
        self.moveFunction= {'P':self.getPawnMoves,'R':self.getRookMoves,
                            'N':self.getKnightMoves,'B':self.getBishopMoves,
                            'Q':self.getQueenMoves,'K':self.getKingMoves}
        self.whiteToMove = True
        self.movelog = []
        self.whiteKingLocation=(7,4)
        self.blackKingLocation=(0,4)

    def makeMove(self,move):
        self.board[move.startRow][move.startCol]="__"
        self.board[move.endRow][move.endCol]=move.pieceMove
        self.movelog.append(move)
        self.whiteToMove =not self.whiteToMove
        #update king location
        if move.pieceMove == 'wK':
            self.whiteKingLocation = (move.endRow,move.endCol)
        elif move.pieceMove == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

    def undoMove(self):
        if len(self.movelog)!=0:
            move = self.movelog.pop()
            self.board[move.startRow][move.startCol]= move.pieceMove
            self.board[move.endRow][move.endCol]= move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMove == 'wK':
                self.whiteKingLocation=(move.startRow,move.startCol)
            elif move.pieceMove == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

    """
    All move valid
    """

    def getValidMoves(self):
        moves = self.getAllPossibleMove()
        valid_moves = []
        for move in moves:
            self.makeMove(move)
            self.whiteToMove = not self.whiteToMove  # Đảo lượt chơi để kiểm tra
            if not self.incheck():  # Nếu vua không bị chiếu, thêm nước đi vào danh sách hợp lệ
                valid_moves.append(move)
            self.whiteToMove = not self.whiteToMove  # Khôi phục lượt chơi
            self.undoMove()  # Hoàn tác nước đi thử nghiệm

        if len(valid_moves) == 0:
            if self.incheck():
                print("Chiếu tướng!")
                self.checkMate = True
            else:
                print("Hết cờ!")
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        return valid_moves

    def incheck(self):
        kingPos = self.whiteKingLocation if self.whiteToMove else self.blackKingLocation
        return self.squareUnderAttack(kingPos[0], kingPos[1])

    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMove()
        self.whiteToMove = not self.whiteToMove

        # Kiểm tra xem có quân nào tấn công ô (r, c) không
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True

        return False  # Không có quân nào tấn công ô (r, c)

    def getAllPossibleMove(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunction[piece](r, c, moves)
        return moves

    def getPawnMoves(self,r,c,moves):
        if self.whiteToMove:
            if self.board[r-1][c]=="__":
                moves.append(Move((r,c),(r-1,c),self.board))
                if r==6 and self.board[r-2][c]=="__":
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c-1>=0:
                if self.board[r-1][c-1][0]=='b':
                    moves.append(Move((r , c), (r - 1 , c - 1), self.board))
            if c+1 <=7:
                if self.board[r-1][c+1][0]=='b':
                    moves.append(Move((r , c), (r - 1 , c + 1), self.board))
        else:
            if self.board[r + 1][c] == "__":
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "__":
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

    def getRookMoves(self,r,c,moves):
        directions=((-1,0),(0,-1),(1,0),(0,1)) # up, left, down, right
        enemyColor ='b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1,8):
                endRow=r + d[0]*i
                endCol=c + d[1]*i
                if 0 <=endRow<8 and 0<=endCol<8:
                    endPiece= self.board[endRow][endCol]
                    if endPiece =='__':
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0]==enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKnightMoves(self,r,c,moves):
        knightMoves=((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        allyColor = 'w' if self.whiteToMove else 'b'
        for m in knightMoves:
            endRow = r+m[0]
            endCol = c+m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getBishopMoves(self,r,c,moves):
        directions = ((-1, -1),(-1, 1),(1, 1),(1, -1))
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '__':
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getQueenMoves(self,r,c,moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1),(-1, -1),(-1, 1),(1, 1),(1, -1))
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '__':
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKingMoves(self,r,c,moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, 1), (1, -1))
        allyColor = 'w' if self.whiteToMove else 'b'
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))


class Move():
    # maps keys to values
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}

    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles={v:k for k,v in filesToCols.items()}

    def __init__(self,startSq,endSq,board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol=endSq[1]
        self.pieceMove= board[self.startRow][self.startCol]
        self.pieceCaptured =board[self.endRow][self.endCol]
        self.moveID=self.startRow*1000+self.startCol*100+self.endRow*10+self.endCol

    """
    Overriding the equals method
    """

    def __eq__(self, other):
        if isinstance(other,Move):
            return self.moveID== other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow,self.startCol)+self.getRankFile(self.endRow,self.endCol)

    def getRankFile(self,r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]