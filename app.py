from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app=Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@localhost:3306/flask_crud'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
db=SQLAlchemy(app)
ma=Marshmallow(app)

class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(20))
    description=db.Column(db.String(20))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def __init__(self, title, description):
        self.title=title
        self.description=description

    def __repr__(self):
        return f"{self.id}"

class UserShema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=User
        load_instance = True
        fields=( 'id', 'title', 'description')

db.create_all()

@app.route('/')
def index():
    return 'index page'

@app.route('/api/v1/users', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        data=request.get_json()
        user_schema=UserShema()
        user=user_schema.load(data)
        print('data', user)
        reuslt=user_schema.dump(user.create())
        return make_response(jsonify({'user' : reuslt}), 200)
    else:
        get_todos=User.query.all()
        user_schema=UserShema(many=True)
        users=user_schema.dump(get_todos)
        return make_response(jsonify({'users': users}), 200)

@app.route('/api/v1/user/<id>', methods=['GET'])
def get_user(id):
    user=User.query.get(id)
    user_schema=UserShema()
    result=user_schema.dump(user)
    return make_response(jsonify({"user": result}), 200)

@app.route('/api/v1/user/<id>', methods=['PUT'])
def update_by_id(id):
    get_user=User.query.get(id)
    data=request.get_json()
    if data['title']:
        get_user.title=data['title']
    if data['description']:
        get_user.description=data['description']

    db.session.add(get_user)
    db.session.commit()

    user_shema=UserShema(only=['title', 'description'])
    user=user_shema.dump(get_user)
    return make_response(jsonify({"user": user}), 200)

@app.route('/api/v1/delete/<id>', methods=['DELETE'])
def delete_by_id(id):
    get_user=User.query.get(id)
    db.session.delete(get_user)
    db.session.commit()
    return make_response("", 204)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
