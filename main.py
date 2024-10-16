from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Needed for flash messages

# Initialize the database
db = SQLAlchemy(app)

# Database model for the "Get in Touch" form
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    # Validate the form
    if not name or not email or not message:
        flash('Please fill out all fields.', 'error')
        return redirect(url_for('home'))

    # Save form data to the database
    new_contact = Contact(name=name, email=email, message=message)
    db.session.add(new_contact)
    db.session.commit()

    flash('Thank you for getting in touch! We will contact you soon.', 'success')
    return redirect(url_for('home'))

@app.route('/admin')
def admin():
    contacts = Contact.query.all()  # Get all contact messages
    return render_template('admin.html', contacts=contacts)

if __name__ == '__main__':
    app.run(debug=True)
    
