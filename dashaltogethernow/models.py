from dashaltogethernow import db

# create models
class State(db.Model):
    __tablename__ = 'states'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    state_ab = db.Column(db.String(3), nullable=False)
    cities = db.relationship('City', back_populates='state')

class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    type = db.Column(db.String(30))
    zip_code = db.Column(db.Integer)
    lat = db.Column(db.Integer)
    lng = db.Column(db.Integer)
    state = db.relationship('State', back_populates="cities")
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'), nullable=False)
    demographic = db.relationship('Demographic', uselist=False, back_populates="city")

class Demographic(db.Model):
    __tablename__ = 'demographic'
    id = db.Column(db.Integer, primary_key=True)
    population = db.Column(db.Integer)
    male_pop = db.Column(db.Integer)
    female_pop = db.Column(db.Integer)
    mean_rent = db.Column(db.Integer)
    pct_own = db.Column(db.Integer)
    pct_married = db.Column(db.Integer)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    city = db.relationship('City', back_populates="demographic")

db.create_all()
