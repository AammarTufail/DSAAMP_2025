from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField
from wtforms.validators import DataRequired

class BookingForm(FlaskForm):
    treatments = SelectMultipleField('Select Treatments', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add to Cart')