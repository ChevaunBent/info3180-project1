from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import InputRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed

class UploadForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    num_bedrooms = StringField('Number of Bedrooms', validators=[InputRequired()])
    num_bathrooms = StringField('Number of Bathrooms', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    price = StringField('Price', validators=[InputRequired()])
    type_ = SelectField(label='Type', choices=[("House", "House"), ("Apartment", "Apertment")])
    description = StringField('Description of property', validators=[InputRequired()])
    upload = TextAreaField('Photo', validators=[FileRequired(),FileAllowed(['jpg', 'jpeg', 'png'], 
    'PLease select an Image!')])