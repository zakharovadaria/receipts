from app.web.auth.basic_auth import BasicAuth


class AdminPanelBasicAuth(BasicAuth):
    role_name = 'admin_panel'


admin_panel_basic_auth = AdminPanelBasicAuth()
