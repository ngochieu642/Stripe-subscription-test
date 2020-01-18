# Set your secret key: remember to change this to your live secret key in production
# See your keys here: https://dashboard.stripe.com/account/apikeys
import stripe
import json
import os

from flask import Flask, render_template, jsonify, request, send_from_directory

app = Flask(__name__, static_url_path="")
stripe.api_key = "sk_test_XZWi6RheiTtm9VxOlCwpHbwL00qiqn4xfy"

# Token is created using Stripe Checkout or Elements!
# Get the payment token ID submitted by the form:


@app.route("/", methods=["GET"])
def home():
    return "Hello from API!"


@app.route("/charge", methods=["POST"])
def post_payment_intent():
    token = request.form["stripeToken"]  # Using Flask
    try:
        charge = stripe.Charge.create(
            amount=999, currency="usd", description="Example charge", source=token,
        )
        msg = "success"
        return jsonify(str(msg))
    except Exception as e:
        return jsonify(str(e), 403)


@app.route("/subscribe", methods=["POST"])
def post_subscribe_intent():
    paymentMethod = request.form["paymentMethod"]

    customer = stripe.Customer.create(
        payment_method=paymentMethod,
        email="hieuthai642@gmail.com",
        invoice_settings={"default_payment_method": paymentMethod,},
    )

    subscription = stripe.Subscription.create(
        customer=customer.id,
        items=[{"plan": "plan_GWj0sXc2QzEkv3",},],
        expand=["latest_invoice.payment_intent"],
    )

    client_secret = subscription.latest_invoice.payment_intent.client_secret
    status = subscription.latest_invoice.payment_intent.status

    if(subscription.status=="incomplete"):
        if(status=="requires_action" or status=="requires_payment_method"):
            msg = {
                'client_secret':client_secret,
                'status':status
            }

        else:
            msg={'status':'Undefined Error'}
    else:
        msg={'status':status}


    return jsonify(msg)