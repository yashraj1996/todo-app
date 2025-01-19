from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=False)
    desc=db.Column(db.String(500), nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

with app.app_context():
    db.create_all()


@app.route('/', methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        title=request.form['title']
        desc=request.form['desc']
        # print(title)
        todo=Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo=Todo.query.all()
    return render_template("index.html", allTodo=allTodo)

@app.route('/show')
def products():
    allTodo=Todo.query.all()
    print(allTodo)
    return "<p>This is a product page</p>"

@app.route('/delete/<int:sno>')
def delete(sno):
    allTodo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(allTodo)
    db.session.commit()
    return redirect ('/')

@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method == "POST":
        title=request.form['title']
        desc=request.form['desc']
        allTodo=Todo.query.filter_by(sno=sno).first()
        allTodo.title=title
        allTodo.desc=desc
        db.session.add(allTodo)
        db.session.commit()
        return redirect('/')
    allTodo=Todo.query.filter_by(sno=sno).first()
    return render_template("update.html", allTodo=allTodo)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=False, port=8000)
