from app.web.auth.basic_auth import BasicAuth


class ClientBasicAuth(BasicAuth):
    role_name = 'client'


client_basic_auth = ClientBasicAuth()
