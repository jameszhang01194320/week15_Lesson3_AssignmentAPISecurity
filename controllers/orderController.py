from flask import request, jsonify
from models.schemas.orderSchema import order_schema, orders_schema
from services import orderService
from marshmallow import ValidationError



def save(token_id):
    try:
        order_data = order_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    if token_id == order_data['customer_id']:
        new_order = orderService.save(order_data)
        return order_schema.jsonify(new_order), 201
    else:
        return jsonify({"message": "You can't order things for other users... scumbag!"}), 401


def find_all():
    all_orders = orderService.find_all()
    return orders_schema.jsonify(all_orders), 200

def find_by_id(order_id): #dynamic route takes in parameters
    order = orderService.find_by_id(order_id)

    return order_schema.jsonify(order), 200


def find_by_customer_id(customer_id):
    orders = orderService.find_by_customer_id(customer_id)
    if not orders:
        return jsonify({"message": "No orders found for this customer"}), 404
    return orders_schema.jsonify(orders), 200


def find_by_email():
    email = request.json['email']
    if email:
        orders = orderService.find_by_email(email)
        return orders_schema.jsonify(orders), 200
    else:
        return jsonify({"message": "Please insert an email"})
