from flask import Flask, request, flash, url_for, redirect, render_template
from forms import  AuthorForm, BookForm
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from sqlite3 import Error
app=Flask(__name__)



def create_connection_in_memory():
   """ create a database connection to a SQLite database """
   conn = None
   try:
       conn = sqlite3.connect(":memory:")
       print(f"Connected, sqlite version: {sqlite3.version}")
   except Error as e:
       print(e)
   finally:
       if conn:
           conn.close()










if __name__ == '__main__':
   create_connection_in_memory()