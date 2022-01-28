from flask import redirect, url_for
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView


class ResponsiveModelView(ModelView):
    list_template = 'admin/responsive_list.html'


class RestrictedAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return hasattr(current_user, 'is_super') and current_user.is_super()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("main.home"))


class RestrictedView(ResponsiveModelView):
    def is_accessible(self):
        return hasattr(current_user, 'is_super') and current_user.is_super()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("main.home"))
