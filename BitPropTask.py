from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy #flask_sqlalchemy import not responding even though installed in the Python Environment
import smtplib
from email.mime.text import MIMEText
import requests 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///properties.db'
app.config['SECRET_KEY'] = 'Neige_Virgilio_Sumbu' #replaced secret key with my own details
db = SQLAlchemy(app)

# --- Models --- 
class Property(db.Model): #created an sql alchemy database to store all information tenants get/view on their side
    id = db.Column(db.Integer, primary_key=True) #used different string types relevant to all information(e.g price=float)
    address = db.Column(db.String(200), nullable=False)
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    price = db.Column(db.Float)
    description = db.Column(db.Text)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'), nullable=False)
    available = db.Column(db.Boolean, default=True)

class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False) #the agent's db login details are only for them
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    properties = db.relationship('Property', backref='agent', lazy=True)

class InterestedTenant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tenant_name = db.Column(db.String(100), nullable=False)
    tenant_email = db.Column(db.String(100), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False) # the tenants db is built only for them to get their info

db.create_all()

# --- Sample Data (Remove or modify) ---
if Agent.query.count() == 0: # Add sample data only if tables are empty
    agent = Agent(username='agent1', password='password', email='agent1@example.com')
    db.session.add(agent)
    property1 = Property(address='123 Main St', bedrooms=2, bathrooms=1, price=1200, 
                        description='Nice apartment', agent=agent)
    property2 = Property(address='456 Oak Ave', bedrooms=3, bathrooms=2, price=2000, 
                        description='Spacious house', agent=agent)
    db.session.add_all([property1, property2])
    db.session.commit()


def send_interest_email(agent_email, tenant_name, property_address):
    # ... (Email sending function - Same as previous response) 

 def get_weather(city):
    api_key = 'da840b5eb676f8e617682e856ef9485b'  # Replaced with actual external API key from OpenWeatherMap
    base_url = "http://api.openweathermap.org/data/2.5/weather?" #free api that I got from Open Weather map as a "nice to have"
    complete_url = base_url + "appid=" + api_key + "&q=" + city
    response = requests.get(complete_url)
    if response.status_code == 200:
        data = response.json()
        return data['main']['temp'] # Return temperature in Kelvin
    else:
        return None

# --- Routes ---
@app.route('/')
def index():
    properties = Property.query.filter_by(available=True).all()
    return render_template('index.html', properties=properties)

@app.route('/property/<int:property_id>')
def property_details(property_id):
    property = Property.query.get_or_404(property_id)
    
@app.route('/register_interest/<int:property_id>', methods=['POST']) #This is all about how web forms send data to your server and how your Flask app handles it.
def register_interest(property_id):
    tenant_name = request.form.get('tenant_name')
    tenant_email = request.form.get('tenant_email')
    property = Property.query.get_or_404(property_id)
    if tenant_name and tenant_email:
        interested_tenant = InterestedTenant(tenant_name=tenant_name, 
                                         tenant_email=tenant_email,
                                         property_id=property.id)
        db.session.add(interested_tenant)
        db.session.commit()
        send_interest_email(property.agent.email, tenant_name, property.address)
        return "Thank you for your interest. The agent has been notified." #this message pops up on the agents email once the tenant registered interest and sends mail
    else:
        return "Please provide your name and email."

@app.route('/agent_login', methods=['GET', 'POST'])
def agent_login():
    if request.method == 'POST':
        username = request.form.get('Dylan')
        password = request.form.get('Bitprop')
        agent = Agent.query.filter_by(username=username).first()
        if agent and agent.password == password:  # Basic password check (no hashing for simplicity)
            session['agent_id'] = agent.id 
            return redirect(url_for('agent_dashboard'))
        else:
            return "Invalid username or password."
    return render_template('agent_login.html')

@app.route('/agent_dashboard')
def agent_dashboard():
    if 'agent_id' in session:
        agent = Agent.query.get(session['agent_id'])
        interested_tenants = InterestedTenant.query.join(Property).filter(Property.agent_id==agent.id).all()
        return render_template('agent_dashboard.html', agent=agent, interested_tenants=interested_tenants)
    else:
        return redirect(url_for('agent_login')) 

@app.route('/tenant_login')
def tenant_login():
    return render_template('tenant_login.html') 

@app.route('/logout')
def logout():
    session.pop('agent_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) 