from . import db

class PropertyInfo(db.Model):
    propid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    num_bedrooms = db.Column(db.Integer, nullable=False)
    num_bathrooms = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(15,2), nullable=False)
    type_ = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    upload = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.Date, nullable=False)

    def __init__(self, title, num_bedrooms, num_bathrooms, location, price, 
    type_, description, upload):
        self.title = title
        self.num_bedrooms = num_bedrooms
        self.num_bathrooms = num_bathrooms
        self.location = location
        self.price = price
        self. type_ = type_
        self.description = description
        self.upload = upload

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.propid)
        except NameError:
            return str(self.propid)

    def __repr__(self):
        return '<User %r>' % (self.title)