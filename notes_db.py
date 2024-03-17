import sqlite3, datetime
from app import session, app1
from database import get_db
from flask import g

date_time = datetime.date.today()
# Convert datetime object to string
datetime_str = date_time.strftime('%Y-%m-%d')

#This function will add notes to db
def add_note(note1):
    conn = get_db()
    conn.execute('''
                 CREATE TABLE IF NOT EXISTS usernotes (
                 note_id TEXT PRIMARY KEY,
                 notes TEXT,
                 id INTEGER,
                 FOREIGN KEY (id) REFERENCES userdata(id)
                 )
                 ''')
    conn.commit()

    #NEED TO MODIFY AS YOU HAVE MADE A SEPERATE FUNCTION
    cur = conn.execute('''
        SELECT note_id FROM usernotes
        WHERE id = ? AND note_id = ?
    ''', (session['userId'], datetime_str))
    
    row = cur.fetchone()
    new_value = note1
    if row is not None:
        #first we need to retrive the existig value and concatinate with new one
        cur = conn.execute(f"SELECT notes FROM usernotes WHERE note_id = {datetime_str} AND id = {session['userId']}")
        for row in cur:
            new_value = row[0] + new_value
            break

        #here we will update the column as per todays date
        conn.execute(f'''
                    UPDATE usernotes SET notes = ? WHERE note_id = ? AND id = ?
                    ''', (new_value, datetime_str, session['userId']))
        conn.commit()   

    #If that 'if'condition didn't works means we have to create a new row
    else: 
        cur =  conn.execute("INSERT INTO usernotes (note_id, notes, id) VALUES (?, ?, ?)", (datetime_str, new_value, session['userId']))
        conn.commit()

def get_note():
    conn = get_db()

    conn.execute('''
                 CREATE TABLE IF NOT EXISTS usernotes (
                 note_id TEXT PRIMARY KEY,
                 notes TEXT,
                 id INTEGER,
                 FOREIGN KEY (id) REFERENCES userdata(id)
                 )
                 ''')
    conn.commit()

    cur = conn.execute('''
        SELECT notes FROM usernotes
        WHERE id = ? AND note_id = ?
    ''', (session['userId'], datetime_str))
    
    row = cur.fetchone()
    if row is not None:
        return row[0]
    return ''

