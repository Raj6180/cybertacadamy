from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///application.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this for production
db = SQLAlchemy(app)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    program = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.String(20), nullable=False)
    education = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.Text)
    goals = db.Column(db.Text, nullable=False)
    referral = db.Column(db.String(100))
    terms = db.Column(db.Boolean, nullable=False)
    newsletter = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        try:
            application = Application(
                first_name=request.form['firstName'],
                last_name=request.form['lastName'],
                email=request.form['email'],
                phone=request.form['phone'],
                dob=request.form['dob'],
                gender=request.form['gender'],
                address=request.form['address'],
                city=request.form['city'],
                state=request.form['state'],
                zip_code=request.form['zip'],
                country=request.form['country'],
                program=request.form['program'],
                start_date=request.form['start-date'],
                education=request.form['education'],
                experience=request.form.get('experience', ''),
                goals=request.form['goals'],
                referral=request.form.get('referral', ''),
                terms='terms' in request.form,
                newsletter='newsletter' in request.form
            )
            db.session.add(application)
            db.session.commit()
            return render_template('apply_success.html')
        except Exception as e:
            db.session.rollback()
            return f"An error occurred: {str(e)}", 500

    return render_template('apply.html')

@app.route('/admin/applications')
def view_applications():
    applications = Application.query.order_by(Application.created_at.desc()).all()
    return render_template('admin.html', applications=applications)

@app.route('/admin/application/<int:id>')
def view_application(id):
    application = Application.query.get_or_404(id)
    return render_template('application_detail.html', application=application)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)