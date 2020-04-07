from flask import Blueprint, render_template, redirect

from form.form_host import HostAddForm
from services.service_host import HostService

from db.models import Host

host_view = Blueprint('host_view', __name__, template_folder='templates')


@host_view.route('/', methods=['GET'])
@host_view.route('/list', methods=['GET'])
def list():
    return render_template('host/host-list.html', hosts=HostService().find_all())


@host_view.route('/create', methods=['GET', 'POST'])
def create():
    form = HostAddForm()
    if form.validate_on_submit():
        host = Host()
        host.hostname = form.hostname.data
        host.active = True
        host.username = form.username.data
        host.password = form.password.data
        host.command = form.command.data
        host.command_start = form.command_start.data
        host.command_stop = form.command_stop.data
        host.command_restart = form.command_restart.data
        if HostService().add(host):
            return redirect('/host')
    return render_template('host/host-create.html', form=form)
