from flask import Flask, request, flash, url_for, redirect, render_template
from forms import  AuthorForm, BookForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
import sqlite3
from sqlite3 import Error
import os




engine = create_engine('sqlite:///library.db')

meta = MetaData()

books = Table(
   'title', meta,
   Column('id', Integer, primary_key=True),
   Column('name', String),
   Column('lastname', String),
)

meta.create_all(engine)
print(engine.table_names())

 



