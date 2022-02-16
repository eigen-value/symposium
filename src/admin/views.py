from flask import redirect, url_for, Markup, request
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_admin.actions import action, ActionsMixin
from flask_admin.helpers import flash_errors, get_redirect_target
from wtforms import TextAreaField


class ResponsiveModelView(ModelView):
    list_template = 'admin/responsive_list.html'


class RestrictedAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return hasattr(current_user, 'is_super') and current_user.is_super()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login"))


class RestrictedView(ResponsiveModelView):
    def is_accessible(self):
        return hasattr(current_user, 'is_super') and current_user.is_super()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login"))


class AccommodationView(RestrictedView):
    form_excluded_columns = ['guests']

    form_overrides = {
        'description': TextAreaField
    }

    form_widget_args = {
        'description': {
            'rows': 10,
            'style': 'min-width:500px'
        }
    }


class UserView(RestrictedView):
    form_excluded_columns = ['last_seen']


class ParticipantView(RestrictedView, ActionsMixin):

    def __init__(self, model, session, name=None, category=None, endpoint=None, url=None, static_folder=None,
                 menu_class_name=None, menu_icon_type=None, menu_icon_value=None):
        super().__init__(model, session, name, category, endpoint, url, static_folder, menu_class_name, menu_icon_type,
                         menu_icon_value)
        self.init_actions()

    def _user_formatter(view, context, model, name):
        if model.receipt_location:
           markupstring = "<a href='../../%s'>%s</a>" % (model.receipt_location, model.receipt_location)
           return Markup(markupstring)
        else:
           return ""

    column_formatters = {
        'receipt_location': _user_formatter
    }

    @action("send_email", "Send email")
    def send_email(self, ids):
        return

    def handle_action(self, return_view=None):
        """
            Handle action request.

            :param return_view:
                Name of the view to return to after the request.
                If not provided, will return user to the return url in the form
                or the list view.
        """
        form = self.action_form()

        if self.validate_form(form):
            # using getlist instead of FieldList for backward compatibility
            ids = request.form.getlist('rowid')
            action = form.action.data

            handler = self._actions_data.get(action)

            if handler and self.is_action_allowed(action):
                response = handler[0](ids)

                if response is not None:
                    return response

            if action == "send_email":
                url = self.get_url("email.create_view", receivers=",".join(ids))
                return redirect(url)

        else:
            flash_errors(form, message='Failed to perform action. %(error)s')

        if return_view:
            url = self.get_url('.' + return_view)
        else:
            url = get_redirect_target() or self.get_url('.index_view')

        return redirect(url)


class EmailView(RestrictedView):

    form_overrides = {
        'body': TextAreaField
    }

    form_widget_args = {
        'body': {
            'rows': 10,
            'style': 'min-width:500px'
        }
    }

    def create_form(self, obj=None):
        form = super(EmailView, self).create_form()
        if ('receivers') in request.args.keys():
            for r in request.args['receivers']:
                print(r)

            receivers = request.args.get("receivers")
            if receivers:
                from src.models import Participant
                receivers = list(receivers.split(","))
                receivers_query = self.session.query(Participant).filter(Participant.id.in_(receivers)).all()
                form.receivers.data = receivers_query
        return form

    def create_model(self, form):
        from src.main.email import send_custom_email

        receivers = form.receivers.data
        subject = form.subject.data
        body = form.body.data

        for r in receivers:
            send_custom_email(r, subject=subject, body=body)

        return super().create_model(form)

