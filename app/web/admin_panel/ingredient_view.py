from app.web.admin_panel.basic_auth_model_view import BasicAuthModelView
from db import session
from app.models.ingredient import Ingredient


class IngredientView(BasicAuthModelView):
    def __init__(self, **kwargs):
        model = Ingredient
        name = 'ingredients'
        super(IngredientView, self).__init__(model, session, name=name, endpoint=name, **kwargs)
