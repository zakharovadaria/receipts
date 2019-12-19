from app.web.admin_panel.basic_auth_model_view import BasicAuthModelView
from db import session
from app.models.receipt import Receipt


class ReceiptView(BasicAuthModelView):
    column_hide_backrefs = False
    column_list = ('id', 'name', 'description', 'calories', 'ingredients', 'steps')

    def __init__(self, **kwargs):
        model = Receipt
        name = 'receipts'
        super(ReceiptView, self).__init__(model, session, name=name, endpoint=name, **kwargs)
