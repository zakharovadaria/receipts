from flask_admin import Admin

from app.web.admin_panel.ingredient_view import IngredientView
from app.web.admin_panel.receipt_view import ReceiptView

admin_panel = Admin(name='Receipts', template_mode='bootstrap3')

admin_panel.add_view(IngredientView())
admin_panel.add_view(ReceiptView())
