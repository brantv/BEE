from hashlib import algorithms_available
from operator import truediv
import numpy as np
import matplotlib as plt
import cv2

class Animal:
    alive = True
    index = -1
    location = [0, 0]
    color = [0, 0, 0]

    def __init__(self, index, boardSize):
        self.index = index
        self.location = [np.random.randint(1, boardSize[0]-1), np.random.randint(1, boardSize[1]-1)]
        self.color = [np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255)]

    def action(self, game):
        # random movement as placeholder for now
        actionDecision = np.random.randint(0, 4)
        if actionDecision == 0:
            location = [self.location[0]+1, self.location[1]]
        elif actionDecision == 1:
            location = [self.location[0], self.location[1]+1]
        elif actionDecision == 2:
            location = [self.location[0]-1, self.location[1]]
        elif actionDecision == 3:
            location = [self.location[0], self.location[1]-1]
        
        if game.isValidMove(location):
            self.location = location

    def printStats(self):
        print("Animal number: ", self.index)
        print("     Alive: ", self.alive)
        print("     Location: ", self.location[0], ', ', self.location[1])


class GameBoard:
    board = []
    boardSize = [0, 0]
    animalList = []
    stepNum = 0
    genNum = 0

    def __init__(self, boardSize):
        self.boardSize = boardSize
        self.board = np.full((boardSize[0], boardSize[1]), fill_value=-1, dtype=np.int8)
        self.board[1:-1, 1:-1] = 0

    def addAnimal(self, animal):
        self.animalList.append(animal)
        self.board[animal.location[0], animal.location[1]] = animal.index

    def isValidMove(self, loc):
        # checks if space is not border or occupied

        if self.board[loc[0], loc[1]] != 0:
            return False
        return True

    def doStep(self):
        # each animal computes its action then redraws the board

        for animal in self.animalList:
            animal = animal.action(self)

        self.board = np.full((self.boardSize[0], self.boardSize[1]), fill_value=-1, dtype=np.int8)
        self.board[1:-1, 1:-1] = 0

        for animal in self.animalList:
            self.board[animal.location[0], animal.location[1]] = animal.index


def boardToImage(game, padding):
    #convert (x,y) board into (x,y,3) board with appropriate colors

    board = np.pad(game.board, pad_width=padding, mode='constant', constant_values=0)
    img = np.zeros((game.boardSize[0]+2*padding, game.boardSize[1]+2*padding, 3), dtype=np.uint8)

    for i in range(game.boardSize[0]+2*padding):
        for j in range(game.boardSize[1]+2*padding):
            # is border
            if board[i,j] == -1:
                img[i,j] = [0,0,0]
            # is open
            elif board[i,j] == 0:
                img[i,j] = [255,255,255]
            # is animal
            else:
                animalIdx = board[i, j]
                animal = game.animalList[int(animalIdx)]
                img[i,j] = animal.color
    
    return img

def main():
    
    boardSize = [100, 100]
    game = GameBoard(boardSize)

    for i in range(30):
        animal = Animal(len(game.animalList), boardSize)
        game.addAnimal(animal)

    boardList = []
    padding = 20
    for i in range(75):
        boardList.append(boardToImage(game, padding))
        game.doStep()

    resX = 500
    resY = 500
    out = cv2.VideoWriter('BEE.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 15, (resX, resY))
    for frame in range(len(boardList)):
        frame = cv2.resize(boardList[frame], (resX, resY), interpolation=cv2.INTER_NEAREST)
        out.write(frame)
    out.release()




if __name__ == "__main__":
    main()