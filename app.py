
from flask import Flask, request, flash, url_for, redirect, render_template
from forms import BookForm, AuthorForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SECRET_KEY'] = "feather"

db = SQLAlchemy(app)

book_author= db.Table('book_author',
db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
db.Column('author_id', db.Integer, db.ForeignKey('author.id'))
)


class Author(db.Model):
   id = db.Column('id', db.Integer, primary_key = True)
   name = db.Column(db.String(200))
   surname = db.Column(db.String(200))
   books = db.Column(db.Integer)
   book_id = db.relationship('Book',secondary=book_author, backref="wrote")

   def __init__(self, name, surname):
      self.name = name
      self.surname = surname
   
   def __repr__(self):
      return f"{self.name}{self.surname}"

class Acess(db.Model):
   id = db.Column('id', db.Integer, primary_key = True)
   borrow_date = db.Column(db.String(200))
   return_date = db.Column(db.String(200))
   book_id = db.Column( db.Integer, db.ForeignKey('book.id'))

   def __init__(self,borrow_date,book_id):
      self.borrow_date=borrow_date
      self.return_date="Nie oddana"
      self.book_id=book_id
   
   def __repr__(self):
      return f"{self.id}{self.borrow_date}{self.return_date}{self.book_id}"
   

class Book(db.Model):
   id = db.Column('id', db.Integer, primary_key = True)
   title = db.Column(db.String(200))
   gnere = db.Column(db.String(200))
   status = db.Column("status", db.String(200)) 
   author_id = db.relationship('Author',secondary=book_author, backref="authored")
   acess_id = db.relationship("Acess", backref="acess_")

   def __init__(self, title, gnere, status):
      self.title = title
      self.gnere = gnere
      self.status = status
   
   def __repr__(self):
      return f'{self.title}'

@app.route('/')
def show_all():
   return render_template('show_all.html', book = Book.query.all(), author = Author.query.all() )

@app.route('/new/book', methods = ['GET', 'POST'])
def new_book():
   form=BookForm()
   if request.method == 'POST':
      print(request.form)
      if "books" in request.form:
         student =Book(request.form['title'], request.form['gnere'], request.form['status'])
      else: 
         student = Book(request.form['title'], request.form['gnere'], request.form['status'],)
      db.session.add(student)
      db.session.commit()
      flash('Record was successfully added')
      return redirect(url_for('show_all'))
   return render_template('new_book.html', authors= Author.query.all(), form=form)

@app.route('/new/author', methods = ['GET', 'POST'])
def new_author():
   form=AuthorForm()
   if request.method == 'POST':
      student = Author(request.form['name'], request.form['surname'])
      db.session.add(student)
      db.session.commit()
      flash('Record was successfully added')
      return redirect(url_for('show_all'))
   return render_template('new_author.html', books= Book.query.all(), form=form)

@app.route('/edit/author/<int:id>', methods = ['GET', 'POST'])
def edit_author(id):
   author=Author.query.get(id)
   form=AuthorForm(name=author.name,surname=author.surname,books=author.books)
   if request.method == "POST":
      author.name=request.form['name']
      author.surname=request.form['surname']
      db.session.add(author)
      db.session.commit()
      return redirect(url_for('show_all'))
   return render_template('edit_author.html', form = form, id=id)

@app.route('/edit/book/<int:id>', methods = ['GET', 'POST'])
def edit_book(id):
   book=Book.query.get(id)
   form=BookForm(title=book.title,gnere=book.gnere,status=book.status)
   if request.method == "POST":
      book.title=request.form['title']
      book.gnere=request.form['gnere']
      book.status=request.form['status']
      db.session.add(book)
      db.session.commit()
      return redirect(url_for('show_all'))
   return render_template('edit_book.html', form = form, id=id)

@app.route('/del/book/<int:id>', methods = ['POST'])
def del_book(id):
   book=Book.query.get(id)
   db.session.delete(book)
   db.session.commit()
   return redirect(url_for('show_all'))

@app.route('/del/author/<int:id>', methods = ['POST'])
def del_author(id):
   author=Author.query.get(id)
   db.session.delete(author)
   db.session.commit()
   return redirect(url_for('show_all'))

@app.route('/combine', methods=['GET', 'POST'])
def combine():
   if request.method=="POST":
      author_id=request.form["author"]
      book_id=request.form["book"]
      book= Book.query.get(book_id)
      author= Author.query.get(author_id)
      book.author_id.append(author)
      db.session.commit()
      return redirect(url_for('show_all'))
   return render_template('combine.html',authors = Author.query.all(),books = Book.query.all())

@app.route('/acess',methods=['GET', 'POST'])
def acess():
   return render_template('borrow.html',books=Book.query.all(),acess=Acess.query.all())

@app.route('/borrow',methods=['POST'])
def bor():
   acc=Acess(borrow_date=datetime.utcnow(),book_id=request.form.get("book"))
   db.session.add(acc)
   db.session.commit()
   return redirect(url_for('acess'))

@app.route('/return',methods=[ 'POST'])
def ret():
   for book in Book.query.all():
      if book.id==int(request.form.get("book")):
         for acc in Acess.query.all():
            if acc.return_date=="Nie oddana":
               if acc.book_id==book.id:
                  acc.return_date=datetime.utcnow()
                  db.session.add(acc)
                  db.session.commit()
   return redirect(url_for('acess'))

@app.route('/stat', methods=['GET','POST'])
def test():
      book1= Book.query.get(1)
      book2= Book.query.get(2)
      acess1=Acess(borrow_date="gfgf",return_date="fgfg",book_id=1)
      db.session.add(acess1)
      db.session.commit()
      return "lol"
      
@app.shell_context_processor
def make_shell_context():
   return {
       "db": db,
       "Book":Book,
       "Author":Author,
       "Acess": Acess   }

if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)