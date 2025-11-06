from flask import jsonify, request
from sqlalchemy.orm import Session
from config.database import get_db
from models.category_model import Category

# CREATE
def create_category():
    db: Session = next(get_db())
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"message": "Name is required"}), 400

    new_category = Category(name=data["name"])
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return jsonify({
        "message": "Category created successfully",
        "data": new_category.to_dict()
    }), 201


# READ (semua kategori)
def get_all_categories():
    db: Session = next(get_db())
    categories = db.query(Category).all()

    return jsonify({
        "message": "Success get categories",
        "data": [c.to_dict() for c in categories]
    }), 200


# READ (kategori berdasarkan ID)
def get_category_by_id(category_id):
    db: Session = next(get_db())
    category = db.query(Category).filter(Category.category_id == category_id).first()

    if not category:
        return jsonify({"message": "Category not found"}), 404

    return jsonify({
        "message": "Success get category",
        "data": category.to_dict()
    }), 200


# UPDATE
def update_category(category_id):
    db: Session = next(get_db())
    data = request.get_json()
    category = db.query(Category).filter(Category.category_id == category_id).first()

    if not category:
        return jsonify({"message": "Category not found"}), 404

    if "name" in data:
        category.name = data["name"]

    db.commit()
    db.refresh(category)

    return jsonify({
        "message": "Category updated successfully",
        "data": category.to_dict()
    }), 200


# DELETE
def delete_category(category_id):
    db: Session = next(get_db())
    category = db.query(Category).filter(Category.category_id == category_id).first()

    if not category:
        return jsonify({"message": "Category not found"}), 404

    db.delete(category)
    db.commit()

    return jsonify({
        "message": "Category deleted successfully"
    }), 200
