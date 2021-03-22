from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import InputRequired, Regexp
from flask_wtf.file import FileField, FileRequired, FileAllowed

class UploadForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    num_bedrooms = StringField('Number of Bedrooms', validators=[InputRequired(), Regexp("^\d+$")])
    num_bathrooms = StringField('Number of Bathrooms', validators=[InputRequired(), Regexp("^\d+$")])
    location = StringField('Location', validators=[InputRequired()])
    price = StringField('Price', validators=[InputRequired(), Regexp("^\d+$")])
    type_ = SelectField(label='Type', choices=[("House", "House"), ("Apartment", "Apartment")])
    description = StringField('Description of property', validators=[InputRequired()])
    upload = FileField('Photo', validators=[FileRequired(),FileAllowed(['jpg', 'jpeg', 'png'], 
    'PLease select an Image!')])