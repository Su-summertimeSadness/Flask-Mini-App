import os
from dataclasses import dataclass

from flask import Flask, render_template, redirect, flash, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

from forms import UserForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = UserForm()
    if form.validate_on_submit():
        user_name = form.name.data
        user_message = form.message.data
        flash('Data Received!', 'success')
        p1 = FeedBack(name=user_name, message=user_message)

        db.session.add(p1)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('index.html', form=form)


@app.route('/getdata')
def get_data():
    data = db.session.query(FeedBack).all()
    return jsonify(data)


@dataclass
class FeedBack(db.Model, SerializerMixin):
    __tablename__ = 'feeds'
    serialize_only = ('id', 'name', 'message')

    id: int = db.Column(db.Integer(), primary_key=True)
    name: str = db.Column(db.String(255))
    message: str = db.Column(db.String(255))

    def __init__(self, name, message):
        self.name = name
        self.message = message

    def __repr__(self):
        return f"Name: {self.name}, Message: {self.message}"

    def obj_to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'message': self.message
        }


# Create db
with app.app_context():
    db.create_all()
    print('done')
if __name__ == '__main__':
    app.run(debug=True)
