"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

import os, random, datetime, psycopg2
from app import app, db
from flask import render_template, request, redirect, url_for, flash
from flask import session, abort, send_from_directory, jsonify, make_response
from werkzeug.utils import secure_filename
from app.forms import UploadForm
from app.models import PropertyInfo

conn = psycopg2.connect(app.config['SQLALCHEMY_DATABASE_URI'])


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
    return render_template('about.html', name="Chevaun Bent")

@app.route('/property', methods=['POST', 'GET'])
def newproperty():
    # Instantiate your form class
    userform = UploadForm()
    # Validate file upload on submit
    if request.method == 'POST' and userform.validate_on_submit():

        # get form data
        title = userform.title.data
        description = userform.description.data
        num_bedrooms = userform.num_bedrooms.data
        num_bathrooms = userform.num_bathrooms.data
        price = userform.price.data
        type_ = userform.type_.data
        location = userform.location.data

        # Get Photo of property and save to your uploads folder
        userfile = request.files['upload']
        filename = secure_filename(userfile.filename)
        userfile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


        #Generate PropertyID and date created
        propid = genId(title, filename)
        date_created = datetime.date.today()

        #Creates a database entry for our database    
        newproperty = PropertyInfo(id = propid, title = title, description = description, num_bedrooms = num_bedrooms, 
        num_bathrooms = num_bathrooms, price = price, type_ = type_, location = location, upload = filename,  
        date_created = date_created)

        #Add entry to our database and commit to the changes        
        db.session.add(newproperty)
        db.session.commit()

        #Flashes a message to our user and redirects our page
        flash('Property Uploaded Successfully', 'success')
        return redirect(url_for('properties'))

    #Flashes Error messages to the user
    flash_errors(userform)
    """Render the website's newproperty page."""
    return render_template('newproperty.html', form = userform)

#Used to generate a file's url for display
@app.route("/uploads/<filename>")
def get_image(filename):
    rootdir = os.getcwd()
    return send_from_directory(rootdir + "/" + app.config['UPLOAD_FOLDER'],
filename)

#Generates a unique 5 digit property ID for each entry in our database
def genId(title, filename):
    id = []
    for x in title:
        id.append(str(ord(x)))
    for x in filename:
        id.append(str(ord(x)))
    random.shuffle(id)
    res= ''.join(id)
    return int(res[:5])

#Route for displaying all properties
@app.route('/properties/', methods=["GET", "POST"])
def properties():
    #Queries the database for all properties
    properties = PropertyInfo.query.all()
    #Handles our GET request
    if request.method == "GET":
        """Render the website's properties page."""
        return render_template('properties.html', properties = properties)
    #Handles our POST request despite there should not be a post request for this route
    elif request.method == "POST":
        response = make_response(jsonify(properties))                                           
        response.headers['Content-Type'] = 'application/json'            
        return response


#Route for finding and displaying a specific property that was selected
@app.route('/property/<propid>', methods=["GET", "POST"])
def get_property(propid):
    #Get a specific property in the database using the property ID that was generated on insertion
    prop = PropertyInfo.query.filter_by(id=propid).first()
    
    #Handles our Get request to fetch a property that mathces the property ID
    if request.method == "GET":
        return render_template("viewproperty.html", prop=prop)
    
    #Handles a POST request for in the event a POST request is generated despite this should not happen
    elif request.method == "POST":
    #Creates an object representation of our POST request
        if prop is not None:
            response = make_response(jsonify(id = prop.propid, title = prop.title, num_bedrooms = prop.num_bedrooms, 
            num_bathrooms = prop.num_bathrooms, location = prop.location, price = prop.price, type_ = prop.type_,  
            description = prop.description, upload = prop.filename, date_created = prop.date_created))
            response.headers['Content-Type'] = 'application/json'            
            return response
        else:
            flash('Property Not Found', 'danger')
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
