from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship('Favorites', backref='user', lazy=True)


    def __repr__(self):
        return '<Usuario %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "active": self.is_active,
            # do not serialize the password, its a security breach
        }

class Personajes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    gender = db.Column(db.String(250))
    hair_color = db.Column(db.String(250))
    eye_color = db.Column(db.String(250))
    favorites = db.relationship('Favorites', backref='personajes', lazy=True)

    def __repr__(self):
        return '<Personajes %r>' % self.name

    def serialize(self):
        
        return {
            "id":self.id,
            "name": self.name,
            "gender": self.gender,
            "hair color":self.hair_color,
            "eye color":self.eye_color
        }
    
class Planetas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    population = db.Column(db.String(250))
    terrain = db.Column(db.String(250))
    favorites = db.relationship('Favorites', backref='planetas', lazy=True)

    def __repr__(self):
        return '<Personajes %r>' % self.name

    def serialize(self):
        return {
            "name": self.name,
            "population": self.population,
            "terrain":self.terrain
        }

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
   
    personaje_id = db.Column(db.Integer, db.ForeignKey('personajes.id'),nullable=True)
    
    planetas_id = db.Column(db.Integer, db.ForeignKey('planetas.id'),nullable=True)
   

    def __repr__(self):
        return '<Favorites %r>' % self.user_id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "personaje_id":self.personaje_id,
            "planetas_id":self.planetas_id
        }