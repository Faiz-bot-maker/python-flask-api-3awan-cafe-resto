from flask import request, jsonify
from sqlalchemy.orm import Session
from config.database import get_db
from models.transaction_model import Transaction
from models.menu_model import Menu

# =====================================================
# GET ALL TRANSACTIONS
# =====================================================
def get_all_transactions():
    db: Session = next(get_db())
    transactions = db.query(Transaction).all()
    data = [t.to_dict() for t in transactions]

    response = {
        "meta": {
            "message": "Success get transactions",
            "total": len(data)
        },
        "data": data
    }

    return jsonify(response), 200

    # =====================================================
# GET TRANSACTION BY ID
# =====================================================
def get_transaction_by_id(transaction_id):
    db: Session = next(get_db())
    transaction = db.query(Transaction).get(transaction_id)

    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404

    return jsonify({
        "message": "Success get transaction",
        "data": transaction.to_dict()
    }), 200



# =====================================================
# CREATE TRANSACTION
# =====================================================
def create_transaction():
    db: Session = next(get_db())
    data = request.get_json()

    menu_id = data.get("menu_id")
    quantity = data.get("quantity")

    if not menu_id or not quantity:
        return jsonify({"error": "menu_id and quantity are required"}), 400

    menu = db.query(Menu).get(menu_id)
    if not menu:
        return jsonify({"error": "Menu not found"}), 404

    total_price = menu.price * quantity

    new_transaction = Transaction(menu_id=menu_id, quantity=quantity, total_price=total_price)
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return jsonify({
        "message": "Transaction created successfully",
        "data": new_transaction.to_dict()
    }), 201


# =====================================================
# UPDATE TRANSACTION
# =====================================================
def update_transaction(transaction_id):
    db: Session = next(get_db())
    transaction = db.query(Transaction).get(transaction_id)

    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404

    data = request.get_json()
    quantity = data.get("quantity")

    if quantity:
        transaction.quantity = quantity
        # Recalculate total
        menu = db.query(Menu).get(transaction.menu_id)
        transaction.total_price = menu.price * quantity

    db.commit()
    db.refresh(transaction)

    return jsonify({
        "message": "Transaction updated successfully",
        "data": transaction.to_dict()
    }), 200


# =====================================================
# DELETE TRANSACTION
# =====================================================
def delete_transaction(transaction_id):
    db: Session = next(get_db())
    transaction = db.query(Transaction).get(transaction_id)

    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404

    db.delete(transaction)
    db.commit()

    return jsonify({
        "message": f"Transaction with id {transaction_id} deleted successfully"
    }), 200
