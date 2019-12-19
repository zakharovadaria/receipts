from flask_admin.contrib.sqla import ModelView

from app.web.admin_panel.basic_auth_model_mixin import BasicAuthModelMixin


class BasicAuthModelView(BasicAuthModelMixin, ModelView):
    column_display_pk = True
