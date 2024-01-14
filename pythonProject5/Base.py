import sqlite3

class User_Database:
    def __init__(self, filename='users.db'):
        self.filename = filename
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        received_messages TEXT,
        sent_messages TEXT,
        password TEXT NOT NULL
        )
        ''')

        connection.commit()
        connection.close()
        self.user = list()
        self.users = list()
    def output_from_sql(self):
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM Users')
        self.users = cursor.fetchall()
        connection.commit()
        connection.close()

    def add_users(self, username, email, password):
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO Users (username, email, password) VALUES (?, ?, ?)',
                        (username, email, password))
        connection.commit()
        connection.close()

    def push_sent_message(self, email, message):

        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()

        cursor.execute('SELECT sent_messages FROM Users WHERE email = ?', (email,))
        sent_messages = cursor.fetchall()
        #print(sent_messages)
        if sent_messages == [(None,)]:
            s = [message]
        else:
            s = sent_messages[0][0].split("', '")
            #print(s)
            s.append(message)
        self.sent_mess = s
        sent_messages = ("', '").join(s)+"'"
        #print(sent_messages)
        cursor.execute('UPDATE Users SET sent_messages = ? WHERE email = ?', (sent_messages, email))
        connection.commit()
        connection.close()

    def push_received_message(self, email, message):

        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()

        cursor.execute('SELECT received_messages FROM Users WHERE email = ?', (email,))
        recieved_messages = cursor.fetchall()
        #print(recieved_messages)
        if recieved_messages == [(None,)]:
            s = [message]
        else:
            s = recieved_messages[0][0].split("', '")
            #print(s)
            s.append(message)
        self.recieved_mess = s
        recieved_messages = ("', '").join(s)
        #print(recieved_messages)
        cursor.execute('UPDATE Users SET received_messages = ? WHERE email = ?', (recieved_messages, email))
        connection.commit()
        connection.close()
    def sent_message_func(self,email):
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()

        cursor.execute('SELECT sent_messages FROM Users WHERE email = ?', (email,))
        sent_messages = cursor.fetchall()
        # print(sent_messages)
        if sent_messages == [(None,)]:
            s = ["У тебя нет исходящих сообщений"]
        else:
            s = sent_messages[0][0].split("', '")
        self.sent_mess = s
        # print(sent_messages)
        connection.commit()
        connection.close()

    def recieved_message_func(self, email):
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()

        cursor.execute('SELECT received_messages FROM Users WHERE email = ?', (email,))
        recieved_messages = cursor.fetchall()
        #print(recieved_messages)
        if recieved_messages == [(None,)]:
            s = ["У тебя нет входящих сообщений"]
        else:
            s = recieved_messages[0][0].split("', '")
        self.recieved_mess = s
        #print(recieved_messages)
        connection.commit()
        connection.close()

    def delete_user(self, id=0, username=""):
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()

        if id != 0:
            cursor.execute('DELETE FROM Users WHERE id = ?', (id,))
        elif username != '':
            cursor.execute('DELETE FROM Users WHERE username = ?', (username,))

        connection.commit()
        connection.close()
    def find_email(self, email):
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Users WHERE email = ?', (email,))

        self.user = cursor.fetchone()

        connection.commit()
        connection.close()

        if self.user != None:
            return True
        else:
            return False
    def User(self):
        return self.user
class Message_Database:
    def __init__(self,filename="message.db"):
        self.filename = filename

        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()

        cursor.execute('''
                CREATE TABLE IF NOT EXISTS Messages (
                id INTEGER PRIMARY KEY,
                header TEXT NOT NULL,
                sender_username TEXT NOT NULL,
                sender_id INTEGER,
                receiver_username TEXT NOT NULL,
                receiver_id INTEGER,
                text TEXT,
                time TEXT
                )
                ''')

        cursor.execute('SELECT * FROM Messages')
        self.messages = cursor.fetchall()
        connection.commit()
        connection.close()

    def output_from_sql_message(self):
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM Messages')
        self.messages = cursor.fetchall()
        connection.commit()
        connection.close()

    def add_message(self, sender, receiver, header, text):
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()

        cursor.execute('INSERT INTO Messages (sender_username, receiver_username, header, text) VALUES (?, ?, ?, ?)',
                       (sender, receiver,header, text,))



        connection.commit()
        connection.close()

