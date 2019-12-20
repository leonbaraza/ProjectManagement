from flask_wtf import FlaskForm
from wtforms import StringField,SelectField,SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired,Length
from projectmngt.models import Regions,Projects,Countries
from flask import request

class RegionsForm(FlaskForm):
    region = StringField('New Region', validators=[DataRequired(), Length(min=3, max=100)])
    submit = SubmitField('Add Region')


class CountryForm(FlaskForm):
    Region = SelectField('Region', choices=[])
    country_name = StringField('Country', validators=[DataRequired()])
    submit = SubmitField('Add Country')


class StrategicDGsForm(FlaskForm):
    sdg_name = StringField('Strategic Development Goal', validators=[DataRequired()])
    submit = SubmitField('Add SDG')


class PartyToForm(FlaskForm):
    party_to_name = StringField('Party to', validators=[DataRequired()])
    submit = SubmitField('Add Party To')


class ProjectsForm(FlaskForm):
    project_name = TextAreaField('Project Name', validators=[DataRequired()])
    proj_objectives = TextAreaField('Project Objectives', validators=[DataRequired()])
    pro_duration = IntegerField('Project Duration', validators=[DataRequired()])
    sptf = IntegerField('Special Programme Trust Fund', validators=[DataRequired()])
    co_financing = IntegerField('Co Funding', validators=[DataRequired()])
    pro_status = StringField('Project Status', validators=[DataRequired()])
    pro_stories = TextAreaField('Project Stories', validators=[DataRequired()])
    party_id  = SelectField('Party To', choices=[])
    region_id  = SelectField('Region', choices=[])
    country_id  = SelectField('Country', choices=[])
    sdgs_id  = SelectField('Strategic Development Goal', choices=[])
    submit = SubmitField('Add Project')


    def get_regions(self):
        regions = Regions.find_all_regions()
        form = Projects(request.POST, obj=regions)
        form.region_id.choices = [(Regions.id, Regions.region_name) for region in Regions.find_all_regions()]

    def get_country(self):
        countries = Countries.find_all_countries()
        form = Projects(request.POST, obj=countries)
        form.region_id.choices = [(Regions.id, Regions.region_name) for region in Regions.find_all_regions()]

