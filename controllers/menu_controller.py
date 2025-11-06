from flask import request, jsonify
from sqlalchemy.orm import Session, joinedload
from config.database import get_db
from models.menu_model import Menu
from models.category_model import Category

# ===========================
# GET ALL MENUS (pagination + filter)
# ===========================
def get_all_menus():
    db: Session = next(get_db())
    q = db.query(Menu).options(joinedload(Menu.category))

    # --- filters ---
    search = request.args.get("search")
    if search:
        q = q.filter(Menu.name.ilike(f"%{search}%"))

    category = request.args.get("category_id")
    if category:
        try:
            q = q.filter(Menu.category_id == int(category))
        except ValueError:
            return jsonify({"error": "category_id must be integer"}), 400

    price_from = request.args.get("price_from")
    if price_from:
        try:
            q = q.filter(Menu.price >= int(price_from))
        except ValueError:
            return jsonify({"error": "price_from must be integer"}), 400

    price_to = request.args.get("price_to")
    if price_to:
        try:
            q = q.filter(Menu.price <= int(price_to))
        except ValueError:
            return jsonify({"error": "price_to must be integer"}), 400

    # --- pagination ---
    try:
        page = int(request.args.get("page", 1))
        size = int(request.args.get("size", 10))
        if page < 1 or size < 1:
            raise ValueError
    except ValueError:
        return jsonify({"error": "page and size must be positive integers"}), 400

    total = q.count()
    items = q.offset((page - 1) * size).limit(size).all()
    data = [m.to_dict() for m in items]

    meta = {
        "current_page": page,
        "per_page": size,
        "total_pages": (total + size - 1) // size if size else 0,
        "total_items": total
    }

    return jsonify({"message": "Success get menus", "data": data, "meta": meta}), 200


# ===========================
# GET MENU BY ID
# ===========================
def get_menu_by_id(menu_id: int):
    db: Session = next(get_db())
    menu = db.query(Menu).options(joinedload(Menu.category)).filter(Menu.menu_id == menu_id).first()
    if not menu:
        return jsonify({"error": "Menu not found"}), 404
    return jsonify({"message": "Success get menu", "data": menu.to_dict()}), 200


# ===========================
# CREATE MENU
# ===========================
def create_menu():
    db: Session = next(get_db())
    data = request.json

    # Validasi minimal
    if not data.get("name") or not data.get("price") or not data.get("category_id"):
        return jsonify({"error": "name, price, and category_id are required"}), 400

    # Check kategori
    category = db.query(Category).filter(Category.category_id == data["category_id"]).first()
    if not category:
        return jsonify({"error": "Category not found"}), 404

    menu = Menu(
        name=data["name"],
        price=data["price"],
        category_id=data["category_id"],
        image_url=data.get("image_url")
    )
    db.add(menu)
    db.commit()
    db.refresh(menu)

    return jsonify({"message": "Menu created", "data": menu.to_dict()}), 201


# ===========================
# UPDATE MENU
# ===========================
def update_menu(menu_id: int):
    db: Session = next(get_db())
    menu = db.query(Menu).filter(Menu.menu_id == menu_id).first()
    if not menu:
        return jsonify({"error": "Menu not found"}), 404

    data = request.json
    menu.name = data.get("name", menu.name)
    menu.price = data.get("price", menu.price)
    menu.category_id = data.get("category_id", menu.category_id)
    menu.image_url = data.get("image_url", menu.image_url)

    db.commit()
    db.refresh(menu)

    return jsonify({"message": "Menu updated", "data": menu.to_dict()}), 200


# ===========================
# DELETE MENU
# ===========================
def delete_menu(menu_id: int):
    db: Session = next(get_db())
    menu = db.query(Menu).filter(Menu.menu_id == menu_id).first()
    if not menu:
        return jsonify({"error": "Menu not found"}), 404

    db.delete(menu)
    db.commit()
    return jsonify({"message": "Menu deleted"}), 200
