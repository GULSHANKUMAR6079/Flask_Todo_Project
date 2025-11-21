from flask import Flask,render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SECRET_KEY'] = 'todosecretkeyhahaha'
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
    
with app.app_context():
    db.create_all()

@app.route("/", methods=['GET','POST'])
def home():
    if request.method=='POST':
        title=request.form["Title"]
        desc=request.form["Description"]
        if not title or not desc:
            flash("Title and Description cannot be empty.", "danger")
        else:
            todo = Todo(title=title, desc=desc)
            db.session.add(todo)
            db.session.commit()
            flash("Todo added successfully!", "success")

        return redirect(url_for("home"))
    alltodos=Todo.query.all()
    return render_template("index.html",alltodos=alltodos)

@app.route("/search")
def search():
    query = request.args.get("query", "").strip()

    if query == "":
        flash("Please enter something to search.", "warning")
        return redirect(url_for("home"))
    results = Todo.query.filter(Todo.title.ilike(f"%{query}%")|Todo.desc.ilike(f"%{query}%")).all()

    if not results:
        flash("No matching todos found.", "info")

    return render_template("search.html", alltodos=results, query=query, bgcolor="#d9eaff")


@app.route("/about")
def about():
    return render_template('about.html')
    

@app.route("/delete/<int:sno>",methods=['GET','POST'])
def delete(sno):
    delete_todos=Todo.query.get_or_404(sno)
    db.session.delete(delete_todos)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/update/<int:sno>",methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title=request.form["Title"]
        desc=request.form["Description"]
        todo=Todo.query.get_or_404(sno)
        todo.title=title
        todo.desc=desc
        db.session.commit()
        return redirect('/')
    alltodos=Todo.query.get_or_404(sno)
    return render_template('update.html',alltodos=alltodos)
if __name__=="__main__":
    app.run(debug=True)
