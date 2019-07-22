from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed
from hello.progress import *
import pypyodbc


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class CandidateForm(FlaskForm):
    candidatename = StringField('Candidate Name',
                                validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email ID',
                        validators=[DataRequired(), Email()])
    contact = IntegerField('Contact No', validators=[DataRequired()])
    notice_period = StringField('Notice Period', validators=[DataRequired()])
    skills = StringField('Skills', validators=[DataRequired()])
    source = StringField('Source', validators=[DataRequired()])
    cv = FileField('Upload Resume', validators=[DataRequired(), FileAllowed(['png', 'jpg', 'pdf', 'docx'])])
    ch = [('01', 'Data Engineer'), ('02', 'UI/UX dev'), ('03', 'Associates'),
          ('04', 'Full Stack'), ('05', 'Andriod Devloper'), ('06', 'Ios Dev'), ('07', 'HR'),
          ('08', 'Salesforce'), ('09', 'Anaplan'), ('10', 'Backend')]
    jobId = SelectField('Select Job ID', choices=ch)
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    selectS = SelectField('Select Skills:', choices=Lookup(skill))
    selectJ = SelectField('Select Job ID:', choices=Lookup(job))
    selectN = StringField('Notice Period:')
    selectR = SelectField('Select Round:', choices=Lookup(result2))
    selectT = SelectField('Select Status:', choices=Lookup(result3))
    submit = SubmitField('Search')


class ProgessTrack(FlaskForm):
    selectC = SelectField('Select Candidate:', choices=Lookup(result1))
    selectR = SelectField('Select Round:', choices=Lookup(result2))
    selectS = SelectField('Select Status:', choices=Lookup(result3))
    submit = SubmitField('Select')


class JobVacancy(FlaskForm):
    ch = [('01', 'Data Engineer'), ('02', 'UI/UX dev'), ('03', 'Associates'),
          ('04', 'Full Stack'), ('05', 'Andriod Devloper'), ('06', 'Ios Dev'), ('07', 'HR'),
          ('08', 'Salesforce'), ('09', 'Anaplan'), ('10', 'Backend')]
    selectVac = SelectField('Select Vacancy: ', choices=ch)
    NVacancy = IntegerField('Number Of Vacancy: ')
    submit = SubmitField('Submit')
