from flask import Blueprint, request, render_template
from projectmngt.models import Projects

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
@main.route("/index")
def home():
    page = request.args.get('page', 1, type=int)
    projects = Projects.query.paginate(page=page, per_page=7)
    # return render_template('allProjects.html', title='All Projects', projects=projects)
    return render_template("home.html", title='All Projects', projects=projects)


