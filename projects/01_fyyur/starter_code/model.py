from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    past_shows_count = db.Column(db.Integer)
    upcoming_shows_count = db.Column(db.Integer)
    seeking_talent = db.Column(db.Boolean,default=False)
    seeking_description = db.Column(db.String())
    genres = db.Column(db.ARRAY(db.String(120)))
    Shows = db.relationship('Shows',backref='venue', lazy=True)


    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    past_shows_count = db.Column(db.Integer)
    upcoming_shows_count = db.Column(db.Integer)
    seeking_venue = db.Column(db.Boolean,default=False)
    seeking_description = db.Column(db.String())
    Shows = db.relationship('Shows',backref='artist', lazy=True)
    genres = db.Column(db.ARRAY(db.String(120)))


    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Shows (db.Model):
 __tablename__ = 'Shows'
 id = db.Column(db.Integer, primary_key=True)
 time = db.Column(db.DateTime(timezone=True), nullable=False)
 venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
 artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))