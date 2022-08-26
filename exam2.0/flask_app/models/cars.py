from flask_app import app
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User

db="exam_car_schema"

class Car:
    def __init__(self, data):
        print(data)
        self.id=data["id"]
        self.price=data["price"]
        self.model=data["model"]
        self.make=data["make"]
        self.year=data["year"]
        self.description=data["description"]
        self.user_id=data["user_id"]
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]
        self.poster_first_name=data["first_name"]
        self.poster_last_name=data["last_name"]
        self.poster_id=data["users.id"]

    @classmethod
    def create(cls,data):
        query="INSERT INTO cars (price, model, make, year, description, user_id) VALUES (%(price)s,%(model)s,%(make)s,%(year)s,%(description)s,%(user_id)s)"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def update(cls,data):
        query="UPDATE cars SET price=%(price)s,model=%(model)s,make=%(make)s,year=%(year)s,description=%(description)s WHERE id=%(id)s;"
        results =connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def get_one(cls,data):
        query= "SELECT * FROM cars JOIN users ON users.id=cars.user_id WHERE cars.id = %(id)s"
        results= connectToMySQL(db).query_db(query,data)
        print(results)
        return cls(results[0])

        # JOIN users on users.id=cars.user_id
        # thiscar=cls(results[0])
        # userinfo={
        #     "id":results[0]["id"],
        #     "first_name":results[0]["first_name"],
        #     "last_name":results[0]["last_name"],
        #     "email":results[0]["email"],
        #     "password":results[0]["password"],
        #     "created_at":results[0]["created_at"],
        #     "updated_at":results[0]["updated_at"],
        # }
        # thiscar.postedby=User(userinfo)
        # return thiscar

    @classmethod
    def get_all(cls):
        query="SELECT * FROM cars JOIN users ON users.id=cars.user_id"
        results= connectToMySQL(db).query_db(query)
        cars=[]
        for row in results:
            cars.append(cls(row))
        return cars

    @classmethod
    def destroy(cls,data):
        query="DELETE FROM cars WHERE id = %(id)s"
        return connectToMySQL(db).query_db(query, data)

    @staticmethod
    def validate_car(car):
        is_valid=True
        if len(car['price']) <1:
            is_valid=False
            flash("Price must be more that $1", "car")
        if len(car['model']) <2:
            is_valid=False
            flash("Model is required", "car")
        if len(car['make']) <2:
            is_valid=False
            flash("Make is required", "car")
        if len(car['year']) <1:
            is_valid=False
            flash("Year is required", "car")
        if len(car['description']) <1:
            is_valid=False
            flash("Must enter a description", "car")
        return is_valid