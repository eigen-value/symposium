from flask import redirect, url_for, Markup
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView


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


class UserView(RestrictedView):
    form_excluded_columns = ['last_seen']


class ParticipantView(RestrictedView):
    def _user_formatter(view, context, model, name):
        if model.receipt_location:
           markupstring = "<a href='../../%s'>%s</a>" % (model.receipt_location, model.receipt_location)
           return Markup(markupstring)
        else:
           return ""

    column_formatters = {
        'receipt_location': _user_formatter
    }