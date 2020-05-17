from application_config import application, logger

logger.info('load views from view module start ...')
from views.view_auth import auth_view
from views.view_chart import chart_view
from views.view_dashboard import dashboard_view
from views.view_host import host_view
from views.view_settings import settings_view
from views.view_terminal import terminal_view
from views.view_service import ServiceView

application.register_blueprint(host_view, url_prefix='/host')
application.register_blueprint(auth_view, url_prefix='/auth')
application.register_blueprint(dashboard_view, url_prefix='/dashboard')
application.register_blueprint(terminal_view, url_prefix='/terminal')
application.register_blueprint(chart_view, url_prefix='/chart')
application.register_blueprint(settings_view, url_prefix='/settings')
application.register_blueprint(ServiceView, url_prefix='/service')
logger.info('load views from views module end ...')

logger.info('load apis from api module start ...')
from api.api_chart import chart_api
from api.api_monitor import monitor_api

application.register_blueprint(chart_api, url_prefix='/api/chart')
application.register_blueprint(monitor_api, url_prefix='/api/monitor')
from data.data_chart_host import chart_host_data

application.register_blueprint(chart_host_data, url_prefix='/data/chart')
logger.info('load apis from api module end ...')
