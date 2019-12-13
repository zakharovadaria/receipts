from app.web.auth.basic_auth import BasicAuth


class AdminBasicAuth(BasicAuth):
    role_name = 'admin'


admin_basic_auth = AdminBasicAuth()
