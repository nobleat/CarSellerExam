from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.cars import Car
from flask_app.models.user import User

@app.route('/addform')
def addpg():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        "id":session['user_id']
    }
    return render_template ("newcar.html", user=User.get_by_id(data))

@app.route("/create", methods=['POST'])
def create():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Car.validate_car(request.form):
        return redirect('/addform')
    data={
        "price": request.form["price"],
        "model": request.form["model"],
        "make": request.form["make"],
        "year": request.form["year"],
        "description": request.form["description"],
        "user_id": session["user_id"],
    }
    Car.create(data)
    return redirect("/dashboard")

@app.route("/edit/car/<int:id>")
def editcar(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data= {
        "id":id
    }
    userdata={
        "id":session['user_id']
    }
    return render_template("edit.html", car=Car.get_one(data), user=User.get_by_id(userdata))

@app.route("/update/car", methods=['POST'])
def update():
        if 'user_id' not in session:
            return redirect('/logout')
        if not Car.validate_car(request.form):
            return redirect('/addform')
        data={
            "price": request.form["price"],
            "model": request.form["model"],
            "make": request.form["make"],
            "year": request.form["year"],
            "description": request.form["description"],
            "id": request.form["id"],
        }
        Car.update(data)
        return redirect('/dashboard')

@app.route("/delete/<int:id>")
def destroy(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        "id":id
    }
    Car.destroy(data)
    return redirect('/dashboard')

@app.route("/viewcar/<int:id>")
def view_car(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        "id":id
        }
    userdata={
        "id":session['user_id']
    }
    print(data)
    return render_template("viewcar.html", car=Car.get_one(data), user=User.get_by_id(userdata))
