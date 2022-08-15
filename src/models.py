from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    nickname = db.Column(db.String(100))

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "nickname": self.nickname
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    birth_year = db.Column(db.String(250))
    gender = db.Column(db.String(250))
    height = db.Column(db.Integer)
    skin_color = db.Column(db.String(250))
    eye_color = db.Column(db.String(250))

    def __repr__(self):
        return '<Character %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "height": self.height,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    diameter = db.Column(db.Integer)
    rotation_period = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    climate = db.Column(db.String(250))

    def __repr__(self):
        return '<Planet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "climate": self.climate
        }

class UserFavourite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    id_character = db.Column(db.Integer, db.ForeignKey('character.id'))
    id_planet = db.Column(db.Integer, db.ForeignKey('planet.id'))
    user = db.relationship(User)
    character = db.relationship(Character)
    planet = db.relationship(Planet)

    def __repr__(self):
        return '<UserFavourite %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "id_user": self.id_user,
            "id_character": self.id_character,
            "id_planet": self.id_planet,
        }