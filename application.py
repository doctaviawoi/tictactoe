# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 18:48:07 2020 

@author: Dewi
""" 

from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp
import numpy as np

app = Flask(__name__)

#app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "X"
        session["winner_found"] = False
        session["winner"] = []
        session["draw"] = False
    
    session["winner_found"], session["winner"], session["draw"] = check_session_for_winner(session["board"])
    
    return render_template("game.html", 
                           game=session["board"], 
                           turn=session["turn"],
                           winner_found=session["winner_found"],
                           winner=session["winner"],
                           draw=session["draw"])

@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    session["board"][row][col] = session["turn"]
    
    if session["turn"] == "X":
        session["turn"] = "O"
    else:
        session["turn"] = "X"

    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
    session["turn"] = "X"
    session["winner_found"] = False
    session["winner"] = []
    session["draw"] = False
    
    return redirect(url_for("index"))


def check_session_for_winner(session_board):
    # to check: 1.rows(horizontal), 2.columns(vertical), 3.diagonal, 4. draw
    
    ## check rows
    for i in range(len(session_board)):
        if session_board[i][0] == None:
            break
        elif session_board[i][0] == session_board[i][1] == session_board[i][2]:
            session["winner_found"] = True
            session["winner"] = session_board[i][0]
            break
    
    ## check columns
    for i in range(len(session_board)):
        if session_board[0][i] == None:
            break
        elif session_board[0][i] == session_board[1][i] == session_board[2][i]:
            session["winner_found"] = True
            session["winner"] = session_board[0][i]
            break
        
    ## check diagonals
    session_board_ar = np.array(session_board)
    if all(session_board_ar.diagonal() != [None, None, None]) and len(set(session_board_ar.diagonal())) == 1:
        session["winner_found"] = True
        session["winner"] = list(set(session_board_ar.diagonal()))[0]
    elif all(np.fliplr(session_board_ar).diagonal() != [None, None, None]) and len(set(np.fliplr(session_board_ar).diagonal())) == 1:
        session["winner_found"] = True
        session["winner"] = list(set(np.fliplr(session_board_ar).diagonal()))[0]
             
    
    ## check for draw
    ### if there is no None values in board, and winner_found==False then it is a draw
    session["draw"] = False
    if all(np.ravel(session_board))==True and session["winner_found"]==False:
        session["draw"] = True
    
    return session["winner_found"], session["winner"], session["draw"]

if __name__ == "__main__":
    app.run(debug=True)       