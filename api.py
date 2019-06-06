from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid 
import datetime
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Denis Oluka'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./todo.db'
db = SQLAlchemy(app)

#User table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(80))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

#Todo list table
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(80))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)

@app.route('/')
def index():
    return '<h2>Welcome to TodoAPI </h2>'

@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['public_id']= user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)
    return jsonify({'users': output})

@app.route('/user/<public_id>', methods=['GET'])
def get_one_user(public_id):

    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        jsonify({'message': 'No user found'})
    user_data = {}
    user_data['public_id']= user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin
    return jsonify({'user': user_data})

@app.route('/admin', methods=['POST'])
def create_admin():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=True)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message':'New admin created succesfully'})

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message':'New user created succesfully'})

@app.route('/user/<public_id>', methods=['PUT'])
def update_user(public_id):

    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'No user found'})
    user.admin = True
    db.session.commit()
    return jsonify({'message': 'The user has been updated to admin'})

@app.route('/user/<public_id>', methods=['DELETE'])
def delete_user(public_id):

    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'No user found'})

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User succesfully deleted'})

@app.route('/login', methods=['GET'])
def  login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter_by(name=auth.username).first()
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('UTF-8')})
    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


#The routes for the todos
@app.route('/todo', methods=['GET'])
def get_all_todos():
    todos = Todo.query.all()

    output = []

    for todo in todos:
        todo_data = {}
        todo_data['id'] = todo.id
        todo_data['text'] = todo.text
        todo_data['complete'] = todo.complete
        output.append(todo_data)

    return jsonify({'todos': output})


@app.route('/todo/<todo_id>', methods=['GET'])
def get_one_todo(todo_id):
    todo = Todo.query.first()

    if not todo:
        return jsonify({'Message': 'You have not created any todo!'})

    todo_data = {}
    todo_data['id'] = todo.id
    todo_data['text'] = todo.text
    todo_data['complete'] = todo.complete

    return jsonify({'Message': todo_data})


@app.route('/todo', methods=['POST'])
def create_todo():
    data = request.get_json()

    new_todo = Todo(text=data['text'], complete=False)
    db.session.add(new_todo)
    db.session.commit()

    return jsonify({'Message': 'Todo created successfully'})


@app.route('/todo/<todo_id>', methods=['PUT'])
def complete_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()

    if not todo:
        return jsonify({'Message': 'No todo found, please add some'})

    todo.complete = True
    db.session.commit()
    return jsonify({'Message': 'Todo has been completed'})


@app.route('/todo/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()

    if not todo:
        return jsonify({'Message': 'No todo found'})

    db.session.delete(todo)
    db.session.commit()

    return jsonify({'Message': 'Todo has been deleted successfully'})    

if __name__ == '__main__':
    app.run(debug = True)