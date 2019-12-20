from flask import Blueprint, flash, render_template, request,redirect,url_for, jsonify
from projectmngt.models import *
from projectmngt import db
from flask_login import login_required
from projectmngt.project.forms import *


projects = Blueprint('projects', __name__)

# Add Routes
@projects.route("/add/region", methods=['GET', 'POST'])
@login_required
def add_region():
    form = RegionsForm()
    if form.validate_on_submit():
        region = Regions(region_name=form.region.data)
        db.session.add(region)
        db.session.commit()

        flash(f'Region name : {region.region_name}', "success")
        return redirect(url_for('projects.add_region'))


    return render_template("addRegion.html", title = 'Add Region', form=form)

@projects.route("/add/country", methods=['GET', 'POST'])
@login_required
def add_country():
    form = CountryForm()
    form.Region.choices = [(region.id, region.region_name)for region in Regions.find_all_regions()]

    if request.method == 'POST':
        region = Regions.query.filter_by(id = form.Region.data).first()
        country = Countries(country_name=form.country_name.data, region_id=region.id)
        db.session.add(country)
        db.session.commit()
        flash('Region: {}, Country: {}'.format(region.id, form.country_name.data), 'success')
        return redirect(url_for('projects.add_country'))
    return render_template("addCountry.html", title = 'Add Country', form=form)

@projects.route("/add/strategic-development-goal", methods=['GET', 'POST'])
@login_required
def add_SDG():
    form = StrategicDGsForm()
    if form.validate_on_submit():
        sdg = StrategicDGs(sdg_name=form.sdg_name.data)
        db.session.add(sdg)
        db.session.commit()

        flash(f'StrategicDGs : {sdg.sdg_name}', 'success')
        return redirect(url_for('projects.add_party_to'))

    return render_template("addSdg.html", title = 'Add Strategic Development Goal',form=form)

@projects.route("/add/Party-To", methods=['GET', 'POST'])
@login_required
def add_party_to():
    form = PartyToForm()
    if form.validate_on_submit():
        party_to = Partyto(party_to_name=form.party_to_name.data)
        db.session.add(party_to)
        db.session.commit()

        flash(f'Party to : {party_to.party_to_name}', 'success')
        return redirect(url_for('projects.add_party_to'))

    return render_template("AddPartyTo.html", title = 'Add Party To', form=form)

@projects.route("/add/Projects", methods=['GET', 'POST'])
@login_required
def add_program():
    form = ProjectsForm()
    form.party_id.choices = [(partyid.id, partyid.party_to_name)for partyid in Partyto.find_all_pt()]
    form.region_id.choices = [(region.id, region.region_name)for region in Regions.find_all_regions()]
    form.country_id.choices = [(country.id, country.country_name)for country in Countries.find_all_countries()]
    form.sdgs_id.choices = [(sdg.id, sdg.sdg_name)for sdg in StrategicDGs.find_all_sdgs()]

    if request.method == 'POST':
        party = Partyto.query.filter_by(id = form.party_id.data).first()
        region = Regions.query.filter_by(id = form.region_id.data).first()
        country = Countries.query.filter_by(id = form.country_id.data).first()
        sdg_id = StrategicDGs.query.filter_by(id = form.sdgs_id.data).first()


        if request.method == "POST":
        # return f'Party To: {party.id}, Region Id: {region.id}, Country Id: {country.id}, SDGs Id: {sdg_id.id}'
            country = Projects(project_name = form.project_name.data,proj_objectives = form.proj_objectives.data
                           ,pro_duration = form.pro_duration.data, sptf=form.sptf.data, co_financing=form.co_financing.data,
                           pro_status=form.pro_status.data, pro_stories=form.pro_stories.data, party_id=party.id, region_id = region.id,
                           country_id=country.id, sdgs_id=sdg_id.id)
            db.session.add(country)
            db.session.commit()
            flash('Project uploaded successfully', 'success')
            return redirect(url_for('projects.add_program'))


    return render_template("addProject.html", title = 'Add Program', form=form)


@projects.route("/all/country/<region_id>")
def fetch_country(region_id):
    countries = Countries.find_all_country_in_region(region_id)

    countryArray = []

    for country in countries:
        countryObj = {}
        countryObj['id'] = country.id
        countryObj['country_name'] = country.country_name
        countryArray.append(countryObj)

    return jsonify({'countries' : countryArray})


@projects.route('/projects/all')
def all_projects():
    page = request.args.get('page',1,type=int)
    projects = Projects.query.paginate(page=page, per_page=7)
    return render_template('allProjects.html', title = 'All Projects', projects = projects)


@projects.route('/project/<project_id>')
def specific_project(project_id):
    spec_proj = Projects.find_one_projects(project_id)
    return render_template('specificProject.html', title = 'Project', project = spec_proj)


@projects.route('/project/<int:project_id>/update', methods=['GET','POST'])
@login_required
def update_project(project_id):
    spec_proj = Projects.find_one_projects(project_id)
    form = ProjectsForm()

    form.party_id.choices = [(partyid.id, partyid.party_to_name) for partyid in Partyto.find_all_pt()]
    form.region_id.choices = [(region.id, region.region_name) for region in Regions.find_all_regions()]
    form.country_id.choices = [(country.id, country.country_name) for country in Countries.find_all_countries()]
    form.sdgs_id.choices = [(sdg.id, sdg.sdg_name) for sdg in StrategicDGs.find_all_sdgs()]


    if request.method == 'POST':
        party = Partyto.query.filter_by(id = form.party_id.data).first()
        region = Regions.query.filter_by(id = form.region_id.data).first()
        country = Regions.query.filter_by(id = form.country_id.data).first()
        sdg_id = Regions.query.filter_by(id = form.sdgs_id.data).first()


        if request.method == "POST":
            spec_proj.project_name = form.project_name.data
            spec_proj.proj_objectives = form.proj_objectives.data
            spec_proj.pro_duration = form.pro_duration.data
            spec_proj.sptf = form.sptf.data
            spec_proj.co_financing = form.co_financing.data
            spec_proj.pro_status = form.pro_status.data
            spec_proj.pro_stories = form.pro_stories.data
            spec_proj.party_id = party.id
            spec_proj.region_id = region.id
            spec_proj.country_id = country.id
            spec_proj.sdgs_id = sdg_id.id

            db.session.commit()
            flash('Project updated successfully', 'success')
            return redirect(url_for('projects.specific_project', project_id=spec_proj.id))

    if form.validate_on_submit():
        party = Partyto.query.filter_by(id=form.party_id.data).first()
        region = Regions.query.filter_by(id=form.region_id.data).first()
        country = Regions.query.filter_by(id=form.country_id.data).first()
        sdg_id = Regions.query.filter_by(id=form.sdgs_id.data).first()

        spec_proj.project_name= form.project_name.data
        spec_proj.proj_objectives = form.proj_objectives.data
        spec_proj.pro_duration = form.pro_duration.data
        spec_proj.sptf = form.sptf.data
        spec_proj.co_financing = form.co_financing.data
        spec_proj.pro_status = form.pro_status.data
        spec_proj.pro_stories = form.pro_stories.data
        spec_proj.party_id = party.id
        spec_proj.region_id = region.id
        spec_proj.country_id = country.id
        spec_proj.sdgs_id = sdg_id.id

        db.session.commit()
        flash('Project updated successfully', 'success')
        return redirect(url_for('projects.specific_project', project_id = spec_proj.id))

    elif request.method == 'GET':
        form.project_name.data = spec_proj.project_name
        form.proj_objectives.data = spec_proj.proj_objectives
        form.pro_duration.data = spec_proj.pro_duration
        form.sptf.data = spec_proj.sptf
        form.co_financing.data = spec_proj.co_financing
        form.pro_status.data = spec_proj.pro_status
        form.pro_stories.data = spec_proj.pro_stories

    return render_template('addProject.html', title = spec_proj.project_name , form = form)


@projects.route('/project/<project_id>',methods=['POST'])
def delete_project(project_id):
    spec_proj = Projects.find_one_projects (project_id)
    db.session.delete(spec_proj)
    db.session.commit()
    flash('You have successfully deleted the project', 'success')
    return redirect(url_for('all_projects'))