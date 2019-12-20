from projectmngt import db, login_manager
from flask_login import UserMixin
# MODELS
class Regions(db.Model):
    __tablename__ = 'regions'
    id = db.Column(db.Integer, primary_key=True)
    region_name = db.Column(db.String, nullable=False)
    countries = db.relationship('Countries', backref = 'region', lazy = True)
    projects = db.relationship('Projects', backref = 'region', lazy = True)

    # add Region
    def add_region(self,region):
        query = Regions(region_name=region)
        db.session.add(query)
        db.session.commit()

    # fetch all regions

    @classmethod
    def find_all_regions(cls):
        return cls.query.all()

    # find one region

    @classmethod
    def find_one_region(cls):
        return cls.query.filter_by(id=id)


class Countries(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(30), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'), nullable=False)
    projects = db.relationship('Projects', backref = 'country', lazy = True)

    # add country
    def add_country(self):
        db.session.add(self)
        db.session.commit()

    # fetch all countries

    @classmethod
    def find_all_countries(cls):
        return cls.query.all()

    # find all country in a region

    @classmethod
    def find_all_country_in_region(cls, id):
        return cls.query.filter_by(region_id = id).all()


class StrategicDGs(db.Model):
    __tablename__ = 'sdgs'
    id = db.Column(db.Integer, primary_key=True)
    sdg_name = db.Column(db.String, nullable=False)

    # add sdgs
    def add_sdg(self):
        db.session.add(self)
        db.session.commit()
    # fetch all regions

    @classmethod
    def find_all_sdgs(cls):
        return cls.query.all()

    # find one region

    @classmethod
    def find_one_sdg(cls, id):
        return cls.query.filter_by(id = id)

class Partyto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    party_to_name = db.Column(db.String, nullable=False)
    # projects = db.relationship('Projects', 'party_to', lazy=True)


    # add sdgs
    def add_pt(self):
        db.session.add(self)
        db.session.commit()

    # fetch all regions

    @classmethod
    def find_all_pt(cls):
        return cls.query.all()

class Projects(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String, nullable=False)
    proj_objectives = db.Column(db.Text, nullable=False)
    pro_duration = db.Column(db.Integer, nullable=False)
    sptf = db.Column(db.String, nullable=False)
    co_financing = db.Column(db.Integer, nullable=False)
    pro_status = db.Column(db.String, nullable=False)
    pro_stories = db.Column(db.Text, nullable=False)
    party_id = db.Column(db.Integer, db.ForeignKey('partyto.id') , nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('regions.id') , nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id') , nullable=False)
    sdgs_id = db.Column(db.Integer, db.ForeignKey('sdgs.id'))

    # add project
    def add_project(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_all_projects(cls):
        return cls.query.all()

    @classmethod
    def find_one_projects(cls, id):
        return cls.query.filter_by(id = id).first()

    # @classmethod
    # def find

class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"User('{self.full_name}', '{self.email}')"

    @classmethod
    def find_the_user(cls,email):
        return cls.query.filter_by(email=email).first()
        # return cls.query


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
