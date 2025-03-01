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
        self.enpassantPossible=()
        self.currentCastlingRight=CastleRight(True,True,True,True)
        self.castleRightLog = [CastleRight(self.currentCastlingRight.wks,self.currentCastlingRight.bks,
                               self.currentCastlingRight.wqs,self.currentCastlingRight.bqs)]
        self.whiteKingCastle=False
        self.blackKingCastle=False

    def makeMove(self,move):
        self.board[move.startRow][move.startCol]="__"
        self.board[move.endRow][move.endCol]=move.pieceMoved
        self.movelog.append(move)
        self.whiteToMove =not self.whiteToMove
        #update king location
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow,move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        #pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol]=move.pieceMoved[0]+'Q'

        #enpassant move
        if move.pieceMoved[1]=='P' and (move.endRow,move.endCol)==self.enpassantPossible:
            move.isEnpassantMove=True
        if move.isEnpassantMove :
            self.board[move.startRow][move.endCol] = '__'
            print("En passant capture!")
        if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.startRow + move.endRow) // 2, move.startCol)
        else:
            self.enpassantPossible = ()

        #print('CastMove:' + str(move.isCastleMove))
        if move.pieceMoved[1]=='K' and abs(move.endCol-move.startCol)==2:
            if move.pieceMoved == 'wK':
                print("Nhập thành Vua trắng!")
            elif move.pieceMoved == 'bK':
                print("Nhập thành Vua đen!")
            if move.endCol - move.startCol ==2:
                print("cast xe king:"+self.board[move.endRow][move.endCol] +","
                      +self.board[move.endRow][move.endCol+1] +","+self.board[move.endRow][move.endCol-1])
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol +1] = '__'
            else:
                print("cast xe queen:"+self.board[move.endRow][move.endCol -2])
                self.board[move.endRow][move.endCol +1] = self.board[move.endRow][move.endCol -2]
                self.board[move.endRow][move.endCol - 2]='__'
            self.isCastleMove=True
        #castle Right
        self.updateCastleRights(move)
        self.castleRightLog.append(CastleRight(self.currentCastlingRight.wks,self.currentCastlingRight.bks,
                               self.currentCastlingRight.wqs,self.currentCastlingRight.bqs))

    def undoMove(self):
        if len(self.movelog)!=0:
            move = self.movelog.pop()
            self.board[move.startRow][move.startCol]= move.pieceMoved
            self.board[move.endRow][move.endCol]= move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == 'wK':
                self.whiteKingLocation=(move.startRow,move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '__'
                self.board[move.startRow][move.endCol] = 'bP' if self.whiteToMove else 'wP'
                self.enpassantPossible=(move.endRow,move.endCol)
            if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()


            #undo castle
            self.castleRightLog.pop()
            self.currentCastlingRight = self.castleRightLog[-1]

            #print('CastMove:' + str(move.isCastleMove))
            if self.checktoUndoCastleMoves(move):
                if move.pieceMoved == 'wK':
                    print("hoàn tác nhập thành vua trắng!")
                elif move.pieceMoved == 'bK':
                    print("hoàn tác nhập thành vua đen")
                if move.endCol-move.startCol==2:
                    print("cast xe king:" + self.board[move.endRow][move.endCol] + ","
                        +self.board[move.endRow][move.endCol+1] +","+self.board[move.endRow][move.endCol-1])
                    self.board[move.endRow][move.endCol +1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = '__'
                else:
                    self.board[move.endRow][move.endCol -2] = self.board[move.endRow][move.endCol +1]
                    self.board[move.endRow][move.endCol +1] = '__'

    """
    All move valid
    """
    def checkCastleMoves(self,move):
        if move.endRow==0 and move.endCol==2 and self.currentCastlingRight.bqs:
            return True
        elif move.endRow==0 and move.endCol==6 and self.currentCastlingRight.bks:
            return True
        elif move.endRow==7 and move.endCol==2 and self.currentCastlingRight.wqs:
            return True
        elif move.endRow==7 and move.endCol==6 and self.currentCastlingRight.wks:
            return True
        return False

    def checktoUndoCastleMoves(self,move):
        if move.pieceMoved=='wK' and abs(move.endCol-move.startCol)==2:
            return True
        if move.pieceMoved == 'bK' and abs(move.endCol - move.startCol) == 2:
            return True
        return False


    def updateCastleRights(self,move):
        if move.pieceMoved== 'wK':
            self.currentCastlingRight.wks=False
            self.currentCastlingRight.wqs=False
        elif move.pieceMoved== 'bK':
            self.currentCastlingRight.bks=False
            self.currentCastlingRight.bqs=False
        elif move.pieceMoved=='wR':
            if move.startRow==7 :
                if move.startCol==0:
                    self.currentCastlingRight.wqs=False
                elif move.startCol==7:
                    self.currentCastlingRight.wks=False
        elif move.pieceMoved=='bR':
            if move.startRow==0 :
                if move.startCol==0:
                    self.currentCastlingRight.bqs=False
                elif move.startCol==7:
                    self.currentCastlingRight.bks=False


    def getValidMoves(self):
        # for log in self.castleRightLog:
        #     print(log.wks,log.wqs,log.bks,log.bqs,end=",")
        # print()
        tempEnpassantPossible = self.enpassantPossible
        tempCastleRights= CastleRight(self.currentCastlingRight.wks,self.currentCastlingRight.bks,
                                      self.currentCastlingRight.wqs,self.currentCastlingRight.bqs)

        # 1. Generate all possible moves

        moves = self.getAllPossibleMove()
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0],self.whiteKingLocation[1],moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0],self.blackKingLocation[1],moves)
        #2. For each move, make the move
        validMoves = []
        for move in moves:
            self.makeMove(move)
            if not self.inCheck():  # Chỉ lưu nước đi nếu không bị chiếu
                validMoves.append(move)
            self.undoMove() # Hoàn tác nước đi thử nghiệm

        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True

        self.enpassantPossible = tempEnpassantPossible
        self.currentCastlingRight= tempCastleRights
        print("end:",self.currentCastlingRight.wks,self.currentCastlingRight.bks,
                                      self.currentCastlingRight.wqs,self.currentCastlingRight.bqs,end=".")
        print('isCastMove:'+str(move.isCastleMove))
        self.isCastleMove=move.isCastleMove
        return validMoves

    def inCheck(self):
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
                elif (r-1,c-1)==self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c+1 <=7:
                if self.board[r-1][c+1][0]=='b':
                    moves.append(Move((r , c), (r - 1 , c + 1), self.board))
                elif (r - 1, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
        else:
            if self.board[r + 1][c] == "__":
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "__":
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                elif (r+1,c-1)==self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                elif (r+1,c+1)==self.enpassantPossible:
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
        #self.getCastleMoves(r,c,moves)

    def getCastleMoves(self,r,c,moves):
        if self.squareUnderAttack(r,c):
            return
        if (self.whiteToMove and self.currentCastlingRight.wks)or(not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingSideCastleMoves(r,c,moves);
        if (self.whiteToMove and self.currentCastlingRight.wqs)or(not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueenSideCastleMoves(r,c,moves)
    def getKingSideCastleMoves(self,r,c,moves):
        if self.board[r][c+1]=='__' and self.board[r][c+2]=='__':
            if not self.squareUnderAttack(r,c+1) and not self.squareUnderAttack(r,c+2):
                moves.append(Move((r,c),(r,c+2),self.board,isCastleMove=True))


    def getQueenSideCastleMoves(self, r, c, moves):
        if self.board[r][c - 1] == '__' and self.board[r][c - 2] == '__'and self.board[r][c - 3] == '__':
            if not self.squareUnderAttack(r, c - 1) and not self.squareUnderAttack(r, c - 2) :
                moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove=True))

class Move():
    # maps keys to values
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}

    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles={v:k for k,v in filesToCols.items()}

    def __init__(self,startSq,endSq,board,isEnpassantMove=False,isCastleMove=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol=endSq[1]
        self.pieceMoved= board[self.startRow][self.startCol]
        self.pieceCaptured =board[self.endRow][self.endCol]
        self.moveID=self.startRow*1000+self.startCol*100+self.endRow*10+self.endCol

        self.isPawnPromotion =False
        self.promotionChoice='Q'
        if (self.pieceMoved =='wP' and self.endRow==0)or (self.pieceMoved =='bP' and self.endRow==7):
            self.isPawnPromotion=True

        self.isEnpassantMove = isEnpassantMove
        self.prevEnpassantPossible= ()
        if self.isEnpassantMove:
            self.pieceCaptured='wP' if self.pieceMoved=='bP' else 'bP'

        self.isCastleMove = isCastleMove
    def setPreEnpassantPossible(self,r,c):
        self.prevEnpassantPossible=(r,c)
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


class CastleRight():
    def __init__(self,wks,bks,wqs,bqs):
        self.wks = wks
        self.bks =bks
        self.wqs=wqs
        self.bqs=bqs
        self.wkm = False
        self.bkm = False