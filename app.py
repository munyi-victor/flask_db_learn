from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

class User(db.Model):
  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
  email: Mapped[str] = mapped_column(String)
  
with app.app_context():
  db.create_all()
  

@app.route("/users")
def user_list():
  users = db.session.execute(db.select(User).order_by(User.id)).scalars()
  return render_template("user/list.html", users = users)

@app.route("/users/create", methods=["GET", "POST"])
def user_create():
  if request.method == "POST":
    user = User(
      username = request.form["username"],
      email  = request.form["email"],
    )
        
    db.session.add(user)
    db.session.commit()
    
    return redirect(url_for("user_detail", id = user.id))
  
  return render_template("user/create.html")

@app.route("/users/<int:id>")
def user_detail(id):
  user = db.get_or_404(User, id)
  return render_template("user/detail.html", user = user, id = user.id)

@app.route("/users/<int:id>/delete", methods=["GET", "POST"])
def user_delete(id):
  user = db.get_or_404(User, id)
  
  if request.method == "POST":
    db.session.delete(user)
    db.session.commit()
    
    return redirect(url_for(user_list))
  
  return render_template("user/delete.html", user = user, id = user.id)

if __name__ == "__main__":
  app.run(debug=True)
6