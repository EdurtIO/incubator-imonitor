from flask import Blueprint, render_template

from form.Host import HostAddForm
from services.service_host import HostService

host_view = Blueprint('host_view', __name__, template_folder='templates')


@host_view.route('/', methods=['GET'])
@host_view.route('/list', methods=['GET'])
def list():
    return render_template('host/host-list.html', hosts=HostService().find_all())


@host_view.route('/create', methods=['GET'])
def create():
    form = HostAddForm()
    return render_template('host.html', form=form)
