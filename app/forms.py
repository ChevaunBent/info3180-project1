from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import InputRequired, Regexp, Length
from flask_wtf.file import FileField, FileRequired, FileAllowed

class UploadForm(FlaskForm):
    title = StringField('Property Title', validators=[InputRequired(),Length(min=1, max=50)])
    description = StringField('Description of property', validators=[InputRequired(),Length(min=1, max=250)])
    num_bedrooms = StringField('No. of Rooms', validators=[InputRequired(), Regexp("^\d+$")])
    num_bathrooms = StringField('No. of Bathrooms', validators=[InputRequired(), Regexp("^\d+$")])
    price = StringField('Price', validators=[InputRequired(), Regexp("^\d+$")])
    type_ = SelectField(label='Type', choices=[("House", "House"), ("Apartment", "Apartment")])
    location = StringField('Location', validators=[InputRequired(),Length(min=1, max=50)])
    upload = FileField('Photo', validators=[FileRequired(),FileAllowed(['jpg', 'jpeg', 'png'], 
    'PLease select an Image!')])