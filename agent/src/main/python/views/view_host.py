from flask import Blueprint, render_template, redirect
from flask_login import login_required

from db.models import Host
from form.form_host import HostCreate
from services.service_host import HostService

host_view = Blueprint('host_view', __name__, template_folder='templates')


@host_view.route('/', methods=['GET'])
@host_view.route('/list', methods=['GET'])
@login_required
def list():
    return render_template('host/host-list.html', hosts=HostService().find_all_order_by_create_time_desc())


@host_view.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = HostCreate()
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
        host.server_name = form.server_name.data
        host.server_type = form.server_type.data
        host.server = form.server.data
        if HostService().add(host):
            return redirect('/host')
    return render_template('host/host-create.html', form=form)
