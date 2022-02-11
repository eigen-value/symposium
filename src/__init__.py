from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin
from src.admin.views import RestrictedAdminIndexView, RestrictedView
from src.utils import setup_logs

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
mail = Mail()
admin = Admin()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('../config/default.py')
    app.config.from_pyfile('../instance/config.py')
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login_manager.init_app(app)
    mail.init_app(app)
    admin.init_app(app, RestrictedAdminIndexView())

    from src.models import User, Role, Participant
    admin.add_view(RestrictedView(User, db.session))
    admin.add_view(RestrictedView(Role, db.session))
    admin.add_view(RestrictedView(Participant, db.session))

    from src.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from src.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from src.main import bp as main_bp
    app.register_blueprint(main_bp)

    setup_logs('symposium')

    import logging
    logging.info("*** SYMPOSIUM APP STARTED ***")

    # if not app.debug and not app.testing:
    #     if app.config['MAIL_SERVER']:
    #         auth = None
    #         if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
    #             auth = (app.config['MAIL_USERNAME'],
    #                     app.config['MAIL_PASSWORD'])
    #         secure = None
    #         if app.config['MAIL_USE_TLS']:
    #             secure = ()
    #         mail_handler = SMTPHandler(
    #             mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
    #             fromaddr='no-reply@' + app.config['MAIL_SERVER'],
    #             toaddrs=app.config['ADMINS'], subject='Microblog Failure',
    #             credentials=auth, secure=secure)
    #         mail_handler.setLevel(logging.ERROR)
    #         app.logger.addHandler(mail_handler)
    #
    #     if not os.path.exists('logs'):
    #         os.mkdir('logs')
    #     file_handler = RotatingFileHandler('logs/microblog.log',
    #                                        maxBytes=10240, backupCount=10)
    #     file_handler.setFormatter(logging.Formatter(
    #         '%(asctime)s %(levelname)s: %(message)s '
    #         '[in %(pathname)s:%(lineno)d]'))
    #     file_handler.setLevel(logging.INFO)
    #     app.logger.addHandler(file_handler)
    #
    #     app.logger.setLevel(logging.INFO)
    #     app.logger.info('Microblog startup')

    return app

from src import models
