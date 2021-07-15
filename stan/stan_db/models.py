
from flask_sqlalchemy import SQLAlchemy


#TODO figure if this is the right place to instantiate this.. 
# for some reason I think/remember it is?
db = SQLAlchemy()

class Hospital(db.Model):
    __tablename__ = 'hospital'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    hospital = db.Column(db.String(255), nullable=False)
    hospitals = db.relationship('TriageEvent', backref='hospital_ref', lazy=True)


class DHB(db.Model):
    __tablename__ = 'dhb'
    id = db.Column(db.Integer, primary_key=True)
    dhb = db.Column(db.String(255), nullable=False)
    dhbs = db.relationship('TriageEvent', backref='dhb_ref', lazy=True)


class PresentingComplaint(db.Model):
    __tablename__ = 'presentingcomplaint'
    presenting_complaint = db.Column(db.String(255), primary_key=True, nullable=False)
    presenting_complaint_group = db.Column(db.String(30), nullable=False)
    presenting_complaint_code = db.Column(db.String(30))
    triage_events = db.relationship('TriageEvent', backref='presenting_complaint_ref', lazy=True)


class TriageEvent(db.Model):
    __tablename__ = 'triageevent'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.String(255))
    method = db.Column(db.String(30))
    hospital_id = db.Column(db.Integer, db.ForeignKey(Hospital.id))
    dhb_id = db.Column(db.Integer, db.ForeignKey(DHB.id))
    present_date_time = db.Column(db.DateTime)
    dob = db.Column(db.DateTime)
    gender = db.Column(db.String(30))
    presenting_complaint = db.Column(db.String(255), db.ForeignKey(PresentingComplaint.presenting_complaint), nullable=False)
    triage_assessment = db.Column(db.Text)
    nurse_triage_code = db.Column(db.Integer)
    stan_model_code = db.Column(db.Float)
    stan_triage_code = db.Column(db.Float)
    vital_signs_pulse = db.Column(db.Integer)
    respiratory_rate = db.Column(db.Integer)
    temperature = db.Column(db.Float)
    blood_pressure_systolic = db.Column(db.Integer)
    blood_pressure_diastolic = db.Column(db.Integer)
    sats = db.Column(db.Float)
    airway_altered = db.Column(db.Boolean)
    breathing_altered = db.Column(db.Boolean)
    circulation_altered = db.Column(db.Boolean)
    disability_gcs = db.Column(db.Integer)
    pain_scale = db.Column(db.Integer)
    neuro_altered = db.Column(db.Boolean)
    mental_health_concerns = db.Column(db.Boolean)
    immunocompromised = db.Column(db.Boolean)
    vital_signs_pulse_was_measured = db.Column(db.Boolean)
    respiratory_rate_was_measured = db.Column(db.Boolean)
    temperature_was_measured = db.Column(db.Boolean)
    blood_pressure_was_measured = db.Column(db.Boolean)
    sats_was_measured = db.Column(db.Float)
    airway_was_measured = db.Column(db.Boolean)
    breathing_was_measured = db.Column(db.Boolean)
    circulation_was_measured = db.Column(db.Boolean)
    disability_gcs_was_measured = db.Column(db.Boolean)
    pain_was_measured = db.Column(db.Boolean)
    neuro_was_measured = db.Column(db.Boolean)
    mental_health_was_measured = db.Column(db.Boolean)
    immunocompromised_was_measured = db.Column(db.Boolean)