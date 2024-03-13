import sqlite3
import hashlib
from flask import g 
from app import app1


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('Facts.db')
    return g.db

@app1.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def addUser( mail, name, password):
    conn = get_db()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS userdata (
                       id INTEGER AUTO_INCREMENT PRIMARY KEY ,
                       email VARCHAR(255) NOT NULL,
                       username VARCHAR(255) NOT NULL,
                       password VARCHAR(255) NOT NULL
    )
                       ''')
    conn.commit()
    
    cur = conn.execute('SELECT email from userdata')
    for _mail in cur:
        if(_mail == mail): return False
    
    password = hashlib.sha256(password).hexdigest()
    conn.execute('''
    INSERT INTO userdata ( email, username, password)
    VALUES ( ?, ?, ?)
    ''', ( mail, name, password))
    conn.commit()

    print("DATA STORED")
    return True


def loginCheck(mail, password):
    password = password.encode()
    password = hashlib.sha256(password).hexdigest()
    conn = get_db()
    cur = conn.execute('SELECT email, password from userdata')
    for row in cur:
        if row[0]==mail and row[1]==password : return True
    return False