#!/usr/bin/env python
#
# Julian Morris & Alvaro Antunez
#
# Game Programming, Level 1 Project
#
# RUSH HOUR
#
# A simple puzzle game, based on the physical game of the same name 
# by Binary Arts Corp


"""
FEED BACK ABOUT THE PROJECT:
This was an enjoyable project. It was really hard, because we weren't very
experienced with python. We spent about 30 hours total on this project.
We would like it if we were explained more about each step of what we must
do.
"""


from graphics import *

width,height=75,75
margin=10
GRID_SIZE=6
screenSize=575
win=GraphWin('Rush',screenSize,screenSize)
GRID_SIZE = 6
grid=[]
drawcheck=[]
sidetoside = ['A','C','X']
updown = ['B','O','P']
car = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','X']
Truck = ['O','P','Q','R','S','T','U','V','W','Y','Z']
maincar = ['X']
pieceName = ['A','B','C','O','P','X']
direction = ['u','d','l','r']
number = [1,2,3,4]
level0="A21dB31rC51dD61dE42dF63dI34rH45dX23r"
level1="A21dB31rC51rD42dE52rF63dG35dH65dX13rP14dQ24rO53d"
level2="A11rB31rC51dD32dE23dF44rG45dH55rI26rK56rX43rO62dP14d"
level3="A11dB22rC42dD33dE35dF45rX13rO41rP63dQ46r"
level4="A11dB22r"

# fail somewhat gracefully

def fail (msg):
    raise StandardError(msg)

"""Creates the empty coordinates of the board with a list.
It also creates drawcheck, which will be used to check if a
square has been drawn."""

def createGrid():
    for column in range(GRID_SIZE):
        grid.append([])
        for row in range(GRID_SIZE):
            grid[column].append('.')
            
    for column in range(GRID_SIZE):
        drawcheck.append([])
        for row in range(GRID_SIZE):
            drawcheck[column].append('.')
    return grid

"""Gets the x or y coordinates of where a car is, in the coordinates
that it can move."""

def getCoordinates (piecename):
    xcoordinates = []
    ycoordinates = []
    
    for index, value in enumerate(grid):
        for i in range(GRID_SIZE):
            if value[i] == piecename:
                ycoordinates.append(index)
                xcoordinates.append(i)
    
    if piecename in sidetoside:
        return xcoordinates
    else:
        return ycoordinates
        
"""Gets the other coordinates of where a car is, in the coordinates 
that the car cannot move."""

def getOtherCoordinates(piecename):
    xcoordinates = []
    ycoordinates = []
    
    for index, value in enumerate(grid):
        for i in range(GRID_SIZE):
            if value[i] == piecename:
                ycoordinates.append(index)
                xcoordinates.append(i)
    
    if piecename in sidetoside:
        return ycoordinates
    else:
        return xcoordinates

"""
We will represent a move by a triple  (p,d,n)  
where  p is the name of the piece as a string consisting of a 
single capital letter ('A', 'B', 'X'), d is a direction as a string
 'u', 'd', 'l', or 'r', and n is a digit between 1 and 6. 
 Thus, ('O','u',3) represents the move of piece O up three positions
 . The function validate_move (board,move) takes a board
 representation and a move and returns True if the move is a valid 
 and False otherwise. A move is valid if the piece described by the
 move is on the board, if the direction is compatible with the
 orientation of the piece, if the path to the target position is
 clear, and if the final position is within the bounds of the board. 
"""

def validate_move (brd,move):
    #move(0)=piecename move(1)=direction move(2)=number of moves
    
    pieceCoordinates=getCoordinates(move[0])
    otherCoordinates=getOtherCoordinates(move[0])
    if move == 'q':
        return True
    elif move[0] in pieceName and move[1] in direction and move[2] in number:
        if move[0] in sidetoside and (move[1]=='u'or move[1]=='d'):
            return False
        elif move[0] in updown and (move[1]=='l' or move[1]=='r'):
            return False
        elif move[1] =='d' or move[1]=='r':
            if pieceCoordinates[-1]+move[2]>5: 
                return False
            else:
                if move[1]=='r':
                    for i in range(pieceCoordinates[-1]+1,pieceCoordinates[-1]+move[2]+1):
                        if brd[otherCoordinates[-1]][i]!='.':
                            return False
                    return True
                elif move[1]=='d':
                    for i in range(pieceCoordinates[-1]+1,pieceCoordinates[-1]+move[2]+1):
                        if brd[i][otherCoordinates[0]]!='.':                                                                                  
                            return False
                    return True
       
        elif move[1] =='u' or move[1]=='l':
            if pieceCoordinates[0]-move[2]<0: 
                return False
            else: 
                if move[1]=='l':
                    for i in range(pieceCoordinates[0]-move[2],pieceCoordinates[0]):
                        if brd[otherCoordinates[0]][i]!='.':
                            return False
                    return True
                
                elif move[1]=='u':
                    for i in range(pieceCoordinates[0]-move[2],pieceCoordinates[0]):
                        if brd[i][otherCoordinates[0]]!='.':
                            return False
                    return True              
        else:
            return True
    else:    
        return False

"""Reads two mouse clicks from the user, and returns a tuple in the
form (piecename,direction,magnitude of move). This was done so that the
update_board and validate_move functions from the rush.py can be used.
Note that these two functions are not imported from rush.py, but copied
directly.
"""

def read_player_input(brd):
    lstmove=[]
    
    firstSelectedPoint=givesCoordinate()
    x1=firstSelectedPoint[0]
    y1=firstSelectedPoint[1]
    
    a=brd[y1][x1]
    lstmove.append(a)
    
    secondSelectedPoint=givesCoordinate()
    x2=secondSelectedPoint[0]
    y2=secondSelectedPoint[1]
    
    moveX=x2-x1
    moveY=y2-y1
    
    if moveX!=0 and moveY==0:
        if moveX>0:
            lstmove.append('r')
            lstmove.append(moveX)
            return tuple(lstmove)
            
        else:
            lstmove.append('l')
            lstmove.append(-moveX)
            return tuple(lstmove)
            
    elif moveX==0 and moveY!=0:
        if moveY>0:
            lstmove.append('d')
            lstmove.append(moveY)
            return tuple(lstmove)
            
        else:
            lstmove.append('u')
            lstmove.append(-moveY)
            return tuple(lstmove)
    else:
        lstmove.append('u')
        lstmove.append(moveX)
        return tuple(lstmove)

"""The update board function updates the board in a list of lists called grid.
This grid will be used to redraw the new board.
"""
def update_board (brd,move):
    global drawcheck;
    drawcheck=[]
    for column in range(GRID_SIZE):
        drawcheck.append([])
        for row in range(GRID_SIZE):
            drawcheck[column].append('.')
    if validate_move(brd,move)==True:
        pieceCoordinates=getCoordinates(move[0])
        otherCoordinates=getOtherCoordinates(move[0])
        if move=='q':
            exit(0)
        elif move[1]=='r':
            for i in pieceCoordinates:
                brd[otherCoordinates[0]][i]='.'
            newCoordinates=[oldposition+move[2] for oldposition in pieceCoordinates]
            for i in newCoordinates:
                brd[otherCoordinates[0]][i]=move[0]
            return brd
        elif move[1]=='d':
            for i in pieceCoordinates:
                brd[i][otherCoordinates[0]]='.'
            newCoordinates=[oldposition+move[2] for oldposition in pieceCoordinates]
            for i in newCoordinates:
                brd[i][otherCoordinates[0]]=move[0]
            return brd
        elif move[1]=='l':
            for i in pieceCoordinates:
                brd[otherCoordinates[0]][i]='.'
            newCoordinates=[oldposition-move[2] for oldposition in pieceCoordinates]
            for i in newCoordinates:
                brd[otherCoordinates[0]][i]=move[0]
            return brd
        elif move[1]=='u':
            for i in pieceCoordinates:
                brd[i][otherCoordinates[0]]='.'
            newCoordinates=[oldposition-move[2] for oldposition in pieceCoordinates]
            for i in newCoordinates:
                brd[i][otherCoordinates[0]]=move[0]
            return brd
        else:
            return brd
    else:
        return brd
 
"""Prints the board in a different screen. After the update function, the board is
redrawn by filling the entire board with white, and redrawing the whole board.
This is not the best way to do it because it would be better to just redraw the
section that was changed, but this design was easier to implement, so we stuck
with it.
"""       
def print_board (brd):
    global screenSize
    rect=Rectangle(Point(0,0),Point(screenSize,screenSize))
    rect.setFill('white')
    rect.draw(win)
    for row in range(6):
        for column in range(6):           
            if brd[column][row] in maincar:
                if drawcheck[column][row]!="drawn":
                    rect=Rectangle(Point(margin*(row+1)+width*row,margin*(column+1)+height*column),Point((width+margin)*(row+2),(height+margin)*(column+1)))
                    rect.setFill('red')
                    rect.draw(win)
                    drawcheck[column][row] ="drawn";drawcheck[column][row+1]="drawn"
                else:
                    pass
           
            elif brd[column][row] in car:
                if drawcheck[column][row]!="drawn":
                    if grid[column][row] in sidetoside:
                        rect= Rectangle(Point(margin*(row+1)+width*row,margin*(column+1)+height*column),Point((width+margin)*(row+2),(height+margin)*(column+1)))
                        rect.draw(win)
                        rect.setFill('blue')
                        drawcheck[column][row] ="drawn";drawcheck[column][row+1]="drawn"
                    else:
                        rect= Rectangle(Point(margin*(row+1)+width*row,margin*(column+1)+height*(column)),Point((width+margin)*(row+1),(height+margin)*(column+2)))                         
                        rect.draw(win)
                        rect.setFill('blue')
                        drawcheck[column][row] ="drawn";drawcheck[column+1][row]="drawn"
                else: 
                    pass
                                                                                                                  
            elif brd[column][row] in Truck:
                if drawcheck[column][row]!="drawn":
                    if grid[column][row] in sidetoside:
                        rect= Rectangle(Point(margin*(row+1)+width*row,margin*(column+1)+height*column),Point((width+margin)*(row+3),(height+margin)*(column+1)))
                        rect.draw(win)
                        rect.setFill('green')
                        drawcheck[column][row] ="drawn";drawcheck[column][row+1]="drawn";drawcheck[column][row+2]="drawn";
                    else:
                        rect= Rectangle(Point(margin*(row+1)+width*row,margin*(column+1)+height*(column)),Point((width+margin)*(row+1),(height+margin)*(column+3)))                         
                        rect.draw(win)
                        rect.setFill('green')
                        drawcheck[column][row] ="drawn";drawcheck[column+1][row]="drawn";drawcheck[column+2][row]="drawn";
                else: 
                    pass
            else:
                rect= Rectangle(Point(margin*(row+1)+width*row,margin*(column+1)+height*column),Point((width+margin)*(row+1),(height+margin)*(column+1)))
                rect.draw(win)
    
    rect= Rectangle(Point(margin*6.5+width*6,margin*3+height*2),Point((width+margin)*6+margin,(height+margin)*(3)))
    rect.draw(win)
    rect.setFill('red')

"""If the main car reaches the exit, the done function will return true.
"""
def done (brd):
    if grid[2][5]=="X":
        return True
    else:
        return False
"""Creates the default level for the game.
"""
def create_initial_level ():  
    
    grid[2][1]="X"; grid[2][2]="X";
    grid[3][1]="A"; grid[3][2]="A";
    grid[4][1]="B"; grid[5][1]="B";
    grid[5][2]="C"; grid[5][3]="C";
    grid[2][3]="O"; grid[3][3]="O";grid[4][3]="O";
    grid[3][5]="P"; grid[4][5]="P";grid[5][5]="P";
    return grid

"""Returns the coordinates of a mouse click in terms of the grid of 
6 by 6"""

def givesCoordinate():
    pos = win.getMouse()
    x=pos.getX()
    y=pos.getY()
    row = (x-margin)//(width+margin)
    column = (y-margin)//(height+margin)
    return row, column

"""The function that is run when the user wants to make his own game
stage. It takes a string in the format 'car name,x1,y1,direction' for each
car, where all cars must be specified in a single string. The for loops in
the function creates the initial game state, and the while loop is repeated
while the game is played. The game ends when the player hits 'q' or the player
wins the game.
"""
def main_with_initial(desc):
    global sidetoside;global updown;global pieceName
    sidetoside=[]
    updown=[]
    pieceName=[]
    brd=createGrid()
    a=[desc[i:i+4] for i in range(0, len(desc), 4)]

    for i in a:
        pieceName.append(i[0])
        xvalue=int(i[1])
        yvalue=int(i[2])
        if i[3]=='r':
            grid[yvalue-1][xvalue-1]=i[0]
            grid[yvalue-1][xvalue]=i[0]
            sidetoside.append(i[0])
            if i[0] in Truck:
                grid[yvalue-1][xvalue+1]=i[0]
        if i[3]=='d':
            grid[yvalue-1][xvalue-1]=i[0]
            grid[yvalue][xvalue-1]=i[0]
            updown.append(i[0])
            if i[0] in Truck:
                grid[yvalue+1][xvalue-1]=i[0]
    brd = grid
    print_board(brd)
    win.setBackground('white')


    while not done(brd):
        move=read_player_input(brd)
        brd=update_board(brd,move)
        print_board(brd)
        
        if win.checkKey()=='q':
            win.close()
            break
        
    if done(brd)==True:
        print 'YOU WIN! (Yay...)\n'
        win.close()

"""This function is very similar to the main_with_initial function, except
the main function creates a default initial level for you.
"""
def main ():
    createGrid()
    brd = create_initial_level()
    print_board(brd)
    win.setBackground('white')
   
    while not done(brd):
        move=read_player_input(brd)
        brd=update_board(brd, move)
        print_board(brd)
        
        if win.checkKey()=='q':
            win.close()
            break


    if done(brd)==True:
        print 'YOU WIN! (Yay...)\n'
        win.close()

if __name__ == '__main__':
    #main_with_initial(level3)
    main()
"""    
    import sys
    if len(sys.argv) > 1:
        main_with_initial (sys.argv[1])
    else:
        main()
"""
