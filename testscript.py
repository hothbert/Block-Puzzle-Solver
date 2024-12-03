# Reads and returns a set of puzzle files and their expected results
import csv
from sliding3 import *


def getPuzzleFiles(filename):
    puzzleFiles = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        # Skip first row
        next(reader)
        for entry in reader:
            data = entry[0].strip('(),').split(',')
            boardName = entry[0].strip('("')
            goalName = entry[1].strip(' "')
            expectedResult = entry[2].strip(')')
            # Append puzzle data to the list
            puzzleFiles.append([boardName, goalName, expectedResult])
    return puzzleFiles


def solvePuzzles(puzzles, fileName):
    if fileName == 'medium':
        points = 19
    elif fileName == 'hard':
        points = 41
    else:
        points = 40
    for puzzle in puzzles[fileName]:
        boardName, goalName, expectedResult = puzzle
        print('\n', boardName, goalName)
        success = main(fileName + '/' + boardName, fileName + '/' + goalName)
        if success:
            print("Puzzle solved successfully!")
        else:
            print("Puzzle failed to solve:")

        if fileName == 'medium' and success is False:
            points -= 0.5
        if fileName == 'hard' and success is False:
            points -= 1.5
    return points


def testing():
    score = 0
    puzzles = {}
    print('easy')
    puzzles['easy'] = getPuzzleFiles('easy_puzzles.csv')
    print('medium')
    puzzles['medium'] = getPuzzleFiles('medium_puzzles.csv')
    print('hard')
    puzzles['hard'] = getPuzzleFiles('hard_puzzles.csv')

    print('easy')
    score += solvePuzzles(puzzles, 'easy')
    print('\n', score, " POINTS")
    print('medium')
    score += solvePuzzles(puzzles, 'medium')
    print('\n', score, " POINTS")
    print('hard')
    score += solvePuzzles(puzzles, 'hard')
    print('\n', score, " POINTS")


testing()
