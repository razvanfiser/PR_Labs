from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import requests
import time
import json

import sqlite3
import pandas as pd
import numpy as np
import re

# Import data that is going to be used for database from a CSV file

df = pd.read_csv("salary.csv")
df = df[["Name", "Annual Salary"]]
df.fillna(0, inplace=True)

# create SQLite in-memory database and populate it with content from CSV file

conn = sqlite3.connect(":memory:")

c = conn.cursor()

c.execute("""CREATE TABLE employees (
            id integer,
            first text,
            last text,
            pay integer
            )""")

conn.commit()

for row in range(100):
    lname, fname = df["Name"][row].split(",  ")
    salary = int(df["Annual Salary"][row])
    c.execute("INSERT INTO employees VALUES ('{row}', '{fname}', '{lname}', '{salary}')".format(row=row, fname=fname, lname=lname, salary=salary))
    conn.commit()



# define some CRUD functionalities for the database based on HTTP requests that may be sent from client
def retrieve_id(employee_id):
    c.execute("SELECT * FROM employees WHERE id='{id}'".format(id=employee_id))
    conn.commit()
    return " ".join([str(item) for item in c.fetchall()[0]])

def retrieve_many(n_start, n_end):
    n_start, n_end = int(n_start), int(n_end)
    c.execute("SELECT * FROM employees WHERE id>='{start}' LIMIT {range}".format(range=n_end-n_start, start=n_start))
    conn.commit()
    return "\n".join([" ".join([str(item) for item in row]) for row in c.fetchall()])

def insert_row(fname, lname, pay):
    c.execute("SELECT MAX(id) FROM employees")
    new_id = list(c.fetchall()[0])[0] + 1
    conn.commit()
    c.execute("INSERT INTO employees VALUES ('{row}', '{fname}', '{lname}', '{salary}')".format(row=new_id, fname=fname, lname=lname, salary=pay))
    conn.commit()
    c.execute("SELECT * FROM employees WHERE id='{id}'".format(id=new_id))
    conn.commit()
    print(c.fetchall(), end='')
    print(" was added to the database.")

def edit_row(id, column, value):
    c.execute("UPDATE employees SET {column} = '{value}' WHERE id = '{id}'".format(column=column, value=value, id=id))
    conn.commit()
    c.execute("SELECT * FROM employees WHERE id='{id}'".format(id=id))
    conn.commit()
    print(c.fetchall(), end='')
    print(" was just updated.")

def delete_row(id):
    c.execute("SELECT * FROM employees WHERE id='{id}'".format(id=id))
    conn.commit()
    deleted_row = c.fetchall()
    c.execute("DELETE FROM employees WHERE id = '{id}'".format(id=id))
    conn.commit()
    print(deleted_row, end='')
    print(" was just deleted from the database.")
# Create the Web Server

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if len(self.path[1:].split("/")) == 1:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(retrieve_id(int(self.path[1:])).encode("utf-8"))
        if len(self.path[1:].split("/")) == 2:
            # print(self.path[1:].split("/"))
            begin, end = self.path[1:].split("/")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(retrieve_many(begin, end).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-length', 0))
        post_data = json.loads(self.rfile.read(content_length).decode())
        if len(post_data) == 3:
            self.send_response(200)
            self.end_headers()
            insert_row(post_data["name"], post_data["last name"], post_data["pay"])
        else:
            self.send_response(404)
            self.end_headers()

    def do_PUT(self):
        content_length = int(self.headers.get('Content-length', 0))
        post_data = json.loads(self.rfile.read(content_length).decode())
        if len(post_data) == 3:
            self.send_response(200)
            self.end_headers()
            edit_row(post_data["id"], post_data["column"], post_data["value"])
        else:
            self.send_response(404)
            self.end_headers()

    def do_DELETE(self):
        content_length = int(self.headers.get('Content-length', 0))
        post_data = json.loads(self.rfile.read(content_length).decode())
        if len(post_data) == 1:
            self.send_response(200)
            self.end_headers()
            delete_row(post_data["id"])
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    # print(retrieve_id(10))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")