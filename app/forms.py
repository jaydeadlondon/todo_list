from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    description = TextAreaField('Description')
    priority = SelectField('Priority', choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])
    submit = SubmitField('Submit')
    

class FilterForm(FlaskForm):
    status = SelectField('Status', choices=[('all', 'All'), ('completed', 'Completed'), ('pending', 'Pending')])
    priority = SelectField('Priority', choices=[('all', 'All'), ('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])
    submit = SubmitField('Filter')
    