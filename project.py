from splinter import Browser
import time
from config import username, password
import numpy as np

def convertCoordinates(boardPositions = []):
    boardLayout = """
 a8 | b8 | c8 | d8 | e8 | f8 | g8 | h8 |
----+----+----+----+----+----+----+----|
 a7 | b7 | c7 | d7 | e7 | f7 | g7 | h7 |
----+----+----+----+----+----+----+----|
 a6 | b6 | c6 | d6 | e6 | f6 | g6 | h6 |
----+----+----+----+----+----+----+----|
 a5 | b5 | c5 | d5 | e5 | f5 | g5 | h5 |
----+----+----+----+----+----+----+----|
 a4 | b4 | c4 | d4 | e4 | f4 | g4 | h4 |
----+----+----+----+----+----+----+----|
 a3 | b3 | c3 | d3 | e3 | f3 | g3 | h3 |
----+----+----+----+----+----+----+----|
 a2 | b2 | c2 | d2 | e2 | f2 | g2 | h2 |
----+----+----+----+----+----+----+----|
 a1 | b1 | c1 | d1 | e1 | f1 | g1 | h1 |"""
    boardTestLayout = np.ndarray(shape=(8,8), dtype='U2')
    convertedPositions = []
    for pos in boardPositions:
        if pos[0] == "0":
            boardColumn = 0
            column = "a"
            if pos[5] == "0":
                row = 8
            else:
                row = 8-(int(pos[5:8])/117)
        else:
            column = int(pos[0:3])/117
            boardColumn = column
            if column == 1:
                column = "b"
            elif column == 2:
                column = "c"
            elif column == 3:
                column = "d"
            elif column == 4:
                column = "e"
            elif column == 5:
                column = "f"
            elif column == 6:
                column = "g"
            else:
                column = "h"
            if pos[7] == "0":
                row = 8
            else:
                row = 8-(int(pos[7:10])/117)
        newPos = column+str(int(row))
        convertedPositions.append(newPos)
        boardLayout = boardLayout.replace(newPos, pos[len(pos)-2:])
        # for newPos in boardPositions:
        boardRow = row-1
        # print(str(boardColumn) + " " + str(boardRow))
        boardTestLayout[int(boardRow), int(boardColumn)] = pos[len(pos)-2:]
    count = 0
    rowCount = 0
    boardString = ""
    boardFinal = np.rot90(boardTestLayout, 3)
    print(boardFinal)
    boardFinal = np.flip(boardFinal, 0)
    print(boardFinal)
    for x in np.nditer(boardFinal):
        count += 1
        if x != "":
            boardString += " " + str(x) + " |"
        else:
            boardString += "  " + str(x) + "  |"
        if count == 8:
            rowCount += 1
            if rowCount != 8:
                boardString += "\n----+----+----+----+----+----+----+----|"
            print(boardString)
            boardString = ""
            count = 0
    return convertedPositions

def printBoard(boardPositions = []):
    placeholders = ["a1","a2","a3","a4","a5","a6","a7","a8",
                    "b1","b2","b3","b4","b5","b6","b7","b8",
                    "c1","c2","c3","c4","c5","c6","c7","c8",
                    "d1","d2","d3","d4","d5","d6","d7","d8",
                    "e1","e2","e3","e4","e5","e6","e7","e8",
                    "f1","f2","f3","f4","f5","f6","f7","f8",
                    "g1","g2","g3","g4","g5","g6","g7","g8",
                    "h1","h2","h3","h4","h5","h6","h7","h8"]
#     boardLayout = """
#  a8 | b8 | c8 | d8 | e8 | f8 | g8 | h8 |
# ----+----+----+----+----+----+----+----|
#  a7 | b7 | c7 | d7 | e7 | f7 | g7 | h7 |
# ----+----+----+----+----+----+----+----|
#  a6 | b6 | c6 | d6 | e6 | f6 | g6 | h6 |
# ----+----+----+----+----+----+----+----|
#  a5 | b5 | c5 | d5 | e5 | f5 | g5 | h5 |
# ----+----+----+----+----+----+----+----|
#  a4 | b4 | c4 | d4 | e4 | f4 | g4 | h4 |
# ----+----+----+----+----+----+----+----|
#  a3 | b3 | c3 | d3 | e3 | f3 | g3 | h3 |
# ----+----+----+----+----+----+----+----|
#  a2 | b2 | c2 | d2 | e2 | f2 | g2 | h2 |
# ----+----+----+----+----+----+----+----|
#  a1 | b1 | c1 | d1 | e1 | f1 | g1 | h1 |"""
    boardPositions = convertCoordinates(boardPositions)
    # for newPos in boardPositions:
    #     boardLayout = boardLayout.replace(newPos, pos[len(pos)-2:])
    # for ph in placeholders:
    #     boardLayout = boardLayout.replace(ph, "  ")
    # print(boardLayout)

entryURL = "https://www.chess.com/login"
secondaryURL = "https://www.chess.com/tactics"
browser = Browser()
browser.visit(entryURL)
browser.driver.set_window_position(0,0, windowHandle='current')
browser.driver.set_window_size(1920, 1080, windowHandle='current')
browser.find_by_id("username").first.fill(username)
browser.find_by_id("password").first.fill(password)
browser.click_link_by_id("login")
browser.visit(secondaryURL)
startBtn = browser.driver.find_element_by_css_selector("#sidebar .tactics-sidebar .btn-primary.btn-start")
startBtn.click()
styles = []
locations = []
lastMove = []
lastCapture = ""
time.sleep(3)
elements = browser.driver.find_element_by_id("chess_com_tactics_board_boardarea").find_elements_by_tag_name("img")
lastMovePositions = browser.driver.find_element_by_id("chess_com_tactics_board_boardarea").find_elements_by_tag_name("div")
index = lastMovePositions[len(lastMovePositions)-1].get_attribute("style").find("translate(")
index += 10
# lastMove = lastMovePositions[len(lastMovePositions)-1].get_attribute("style")[index:len(lastMovePositions[len(lastMovePositions)-1])-2]
for item in elements:
    if item.get_attribute("style").find("translate(") > 0 and item.get_attribute("class") != "":
        index = item.get_attribute("style").find("translate(")
        index += 10
        locations.append(item.get_attribute("style")[index:len(item.get_attribute("style"))-2] + ", " + item.get_attribute("src")[len(item.get_attribute("src"))-6:len(item.get_attribute("src"))-4])
    elif item.get_attribute("style").find("translate(") > 0 and item.get_attribute("class") == "":
        index = item.get_attribute("style").find("translate(")
        index += 10
        lastCapture = item.get_attribute("style")[index:len(item.get_attribute("style"))-24] + ", " + item.get_attribute("src")[len(item.get_attribute("src"))-6:len(item.get_attribute("src"))-4]
printBoard(locations)
# for item in lastMovePositions:
#     print(item.get_attribute("style"))
if lastCapture == "":
    lastCapture = "No piece captured."
print(lastCapture)