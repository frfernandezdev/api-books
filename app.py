import os
from flask import Flask, jsonify, request
from books import Books
from flask_sqlalchemy import SQLAlchemy

dbdir = 'sqlite:///' + os.path.abspath(os.getcwd()) + '/db_books.db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = dbdir
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Books(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80))
	description = db.Column(db.String(255))
	author = db.Column(db.String(100))
	launching = db.Column(db.String(100))


@app.route('/')
def index():
	return jsonify({"ping": "pong"})

	
#Obtener la lista de libros
@app.route('/api/books', methods=["GET"])
def  get_books():
	books_list = Books.query.all()
	print('Query done')
	return jsonify(
		{"message":"Books saved"},
		{"books saved": books_list}
	)


#Buscar libro
@app.route('/api/books/<int:book_id>', methods=["GET"])
def search_book(book_id):
	book_found = Books.query.filter_by(id=book_id).first()

	print("query done", book_found.title)
	return jsonify(
		{"title":book_found.title,
		"description":book_found.description,
		"author":book_found.author,
		"launching":book_found.launching}
	)



#Publicar nuevo libro
@app.route('/api/books/', methods=["POST"])
def add_book():

	if request.method == 'POST':
		new_book = Books(
			title=request.json["title"],
			description=request.json["description"],
			author=request.json["author"],
			launching=request.json["launching"]
		)
	
		db.session.add(new_book)
		db.session.commit()

		return jsonify({"message": "The book is added"})
	
	else:
		return jsonify({"message": "The book isn\'t added"})


#Eliminar un libro
@app.route('/api/books/<int:book_id>', methods=["DELETE"])
def remove_book(book_id):
	book_found = [book for book in books_saved if book["id"] == book_id]
	
	if len(book_found) > 0:
		books_saved.remove(book_found[0])
		return jsonify({"message": "The book is deleted"}, books_saved)

	else:
		return jsonify({"message": "The book not found"})


#Actulizar o editar un libro
@app.route('/api/books/<int:book_id>', methods=["GET", "PUT"])
def update_book(book_id):
	book_found = [book for book in books_saved if book["id"] == book_id]
	
	if len(book_found) > 0:
		book_found[0]['title'] = request.json['title']
		book_found[0]['description'] = request.json['description']
		book_found[0]['author'] = request.json['author']
		book_found[0]['launching'] = request.json['launching']

		return jsonify({"message": "The book is updated"}, books_saved)

	else:
		return jsonify({"message": "The book not found"})



if __name__ == "__main__":
	db.create_all()
	app.run(debug=True, port=8080)
