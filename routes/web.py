from flask import Blueprint
from controllers.menu_controller import (
    get_all_menus,
    get_menu_by_id,
    create_menu,
    update_menu,
    delete_menu
)
from controllers.menu_controller import get_all_menus
from controllers.category_controller import (
    get_all_categories,
    create_category,
    update_category,
    delete_category
)
from controllers.transaction_controller import (
    get_all_transactions,
    get_transaction_by_id,
    create_transaction,
    update_transaction,
    delete_transaction
)

web = Blueprint("web", __name__)

# ===========================
# MENU CRUD
# ===========================
web.route("/menus", methods=["GET"])(get_all_menus)
web.route("/menus/<int:menu_id>", methods=["GET"])(get_menu_by_id)
web.route("/menus", methods=["POST"])(create_menu)
web.route("/menus/<int:menu_id>", methods=["PUT"])(update_menu)
web.route("/menus/<int:menu_id>", methods=["DELETE"])(delete_menu)

# ===========================
# CATEGORY CRUD
# ===========================
web.route("/categories", methods=["GET"])(get_all_categories)
web.route("/categories", methods=["POST"])(create_category)
web.route("/categories/<int:category_id>", methods=["PUT"])(update_category)
web.route("/categories/<int:category_id>", methods=["DELETE"])(delete_category)

# ===========================
# TRANSACTION CRUD
# ===========================
web.route("/transactions", methods=["GET"])(get_all_transactions)
web.route("/transactions/<int:transaction_id>", methods=["GET"])(get_transaction_by_id)
web.route("/transactions", methods=["POST"])(create_transaction)
web.route("/transactions/<int:transaction_id>", methods=["PUT"])(update_transaction)
web.route("/transactions/<int:transaction_id>", methods=["DELETE"])(delete_transaction)
