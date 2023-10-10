from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
class Register(db.Model):
    __tablename__ = 'registers'

    id = db.Column(db.Integer, primary_key=True)
    auth_key = db.Column(db.String())

    def __init__(self, auth_key):
        self.auth_key = auth_key



class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    auth_key = db.Column(db.String())
    hardware_id = db.Column(db.String())

    def __init__(self, auth_key, hardware_id):
        self.auth_key = auth_key
        self.hardware_id = hardware_id

@app.route('/api/reg', methods=['POST'])
def register():
    data = request.get_json()
    reg = Register.query.filter_by(auth_key=data['auth_key']).first_or_404()
    new_user = User(data['auth_key'], data['hardware_id'])
    db.session.add(new_user)
    db.session.delete(reg)
    db.session.commit()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@app.route('/api/auth', methods=['POST'])
def authentication():
    data = request.get_json()
    User.query.filter_by(auth_key=data['auth_key'], hardware_id=data['hardware_id']).first_or_404()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
