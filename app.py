from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Float, Integer
import os
from flask_marshmallow import Marshmallow

app = Flask(__name__)
# db configaration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'mine.db')
db = SQLAlchemy(app)
mar = Marshmallow(app)


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('db created')


# for db delete all --- flask db_drop
@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('db dropped')


# saving data --- flask db_seed
@app.cli.command('db_seed')
def db_seed():
    # familyId='1',
    aunt = Family(relation='aunt', age=47, distanceLocation=3.16)
    ma = Family(relation='ma', age=45, distanceLocation=33.16)
    baba = Family(relation='baba', age=55, distanceLocation=33.115)
    db.session.add(aunt)
    db.session.add(ma)
    db.session.add(baba)

    test_user = Users(first_name='test', last_name='user', email='test@test.test', password='test')
    db.session.add(test_user)
    db.session.commit()
    print('db seeded')


@app.route("/")
def hello_world():
    return jsonify(message="Hello, World!")


@app.route("/parameters")
def parameters():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    if age > 18:
        return jsonify(message="OK" + name + ' yo', data=['age:89', 'name:koi'], erros=''), 200
    else:
        return jsonify(message="NOT var OK" + name + ' not yo', erros='not possible'), 404


@app.route("/variables/<string:name>/<int:age>")
def variables(name: str, age: int):
    if age < 18:
        return jsonify(message=" Not OK " + name, error='your age is ' + str(age)), 401
    else:
        return jsonify(message="OK " + name), 200


@app.route('/api',methods=["GET"])
def api():
    fam_list = Family.query.all()
    result = families_schema.dump(fam_list)
    return jsonify(result)


# models
class Users(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)


class Family(db.Model):
    __tablename__ = 'family'
    familyId = Column(Integer, primary_key=True)
    relation = Column(String)
    age = Column(Integer)
    distanceLocation = Column(Float)


class UserSchema(mar.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password')


class FamilySchema(mar.Schema):
    class Meta:
        fields = ('familyId', 'relation', 'age', 'distanceLocation')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

family_schema = FamilySchema()
families_schema = FamilySchema(many=True)

if __name__ == '__main__':
    app.run()
