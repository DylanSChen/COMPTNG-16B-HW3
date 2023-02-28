from flask import Flask, g, render_template, request

import sklearn as sk
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sqlite3

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/submit', methods=['POST','GET']) 
def submit_a_message():
    if request.method == 'GET':
        # if the user just visits the url
        return render_template('submit.html')
    else:
        # if the user submits the form
        message, handle = insert_message(request)
        return render_template('submit.html', thanks = True, name = handle)


def get_message_db():
  # write some helpful comments here
    try:
        return g.message_db
    except:
        g.message_db = sqlite3.connect("messages_db.sqlite")
        cmd = \
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            handle TEXT NOT null,
            message TEXT NOT null
        )
        """
        cursor = g.message_db.cursor()
        cursor.execute(cmd)        
        return g.message_db
    
    
def insert_message(request):
    message = request.form['message']
    handle = request.form['handle']
    db = get_message_db()
    cursor = db.cursor()
    
    cmd = \
    """
    INSERT INTO messages (handle, message) 
    VALUES('{place_a}', '{place_b}')
    """.format(place_a = handle, place_b = message)
    
    cursor.execute(cmd)
    db.commit() 
    db.close() 
    
    return message, handle
    
@app.route('/view')
def view_messages():
    dict = random_messages(4)
    return render_template('view.html', my_dict = dict)

def random_messages(n):
    g.message_db = sqlite3.connect("messages_db.sqlite")
    cursor = g.message_db.cursor()
    
    cmd = \
    """
    SELECT
        m.handle,
        m.message
    FROM messages m
    ORDER BY RANDOM()
    LIMIT '{place_a}'
    """.format(place_a = n)
    
    df = pd.read_sql_query(cmd, g.message_db)
    my_dict = {}
    
    for i in range(len(df)):
        my_dict[df.iloc[i,0]] = df.iloc[i,1]
        
    g.message_db.close() 
    
    return my_dict