"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

import os, random, datetime
from app import app, db
from flask import render_template, request, redirect, url_for, flash
from flask import session, abort, send_from_directory, jsonify, make_response
from werkzeug.utils import secure_filename
from .forms import UploadForm
from .models import PropertyInfo


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@app.route('/property', methods=['POST', 'GET'])
def newproperty():
    # Instantiate your form class
    userform = UploadForm()
    # Validate file upload on submit
    if request.method == 'POST' and userform.validate_on_submit():

        # get form data
        title = userform.title.data
        num_bedrooms = userform.num_bedrooms.data
        num_bathrooms = userform.num_bathrooms.data
        location = userform.location.data
        price = userform.price.data
        type_ = userform.type_.data
        description = userform.description.data

        # Get Photo of property and save to your uploads folder
        userfile = request.files['upload']
        filename = secure_filename(userfile.filename)
        userfile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


        # generate PropertyID and date created
        propid = genId(title, filename)
        date_created = datetime.date.today()
            
        newproperty = PropertyInfo(propid = propid, title = title, num_bedrooms = num_bedrooms, 
        num_bathrooms = num_bathrooms, location = location, price = price, type_ = type_,  
        description = description, upload = filename, date_created = date_created)
                
        db.session.add(newproperty)
        db.session.commit()

        flash('Property Uploaded', 'success')
        return redirect(url_for('properties'))

    flash_errors(userform)
    """Render the website's newproperty page."""
    return render_template('newproperty.html', form = userform)


def get_upload_images():
    rootdir = os.getcwd()
    FileList = []
    for subdir, dirs, files in os.walk(rootdir + '/uploads'):
        for f in files:
            FileList.append(f)       
    return FileList

@app.route("/uploads/<filename>")
def get_image(filename):
    rootdir = os.getcwd()
    return send_from_directory(rootdir + "/" + app.config['UPLOAD_FOLDER'],
filename)

def genId(title, filename):
    id = []
    for x in title:
        id.append(str(ord(x)))
    for x in filename:
        id.append(str(ord(x)))
    random.shuffle(id)
    return id[:5]

@app.route('/properties/', methods=["GET", "POST"])
def properties():
    properties = PropertyInfo.query.all()
    prop_list = [{"Property": prop.title, "PropertyID": prop.propid} for prop in properties]
    
    if request.method == "GET":
        """Render the website's properties page."""
        return render_template('properties.html', properties = properties)
    
    elif request.method == "POST":
        response = make_response(jsonify({"Property": prop_list}))                                           
        response.headers['Content-Type'] = 'application/json'            
        return response
    
@app.route('/property/<propid>', methods=["GET", "POST"])
def get_property(propid):
    
    prop = PropertyInfo.query.filter_by(propid=propid).first()
    
    if request.method == "GET":
        return render_template("viewproperty.html", prop=prop)
    
    elif request.method == "POST":
        if prop is not None:
            response = make_response(jsonify(propid = prop.propid, title = prop.title, num_bedrooms = prop.num_bedrooms, 
            num_bathrooms = prop.num_bathrooms, location = prop.location, price = prop.price, type_ = prop.type_,  
            description = prop.description, upload = prop.filename, date_created = prop.date_created))
            response.headers['Content-Type'] = 'application/json'            
            return response
        else:
            flash('No User Found', 'danger')
            return redirect(url_for("home"))


###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
