import json 
import simplejson
import requests
import datetime
from datetime import timedelta
from django.conf import settings
from .models import ShipRocketToken, OrderTracking

NEW_TOKEN_ENDPOINT = "https://apiv2.shiprocket.in/v1/external/auth/login"
CREATE_ENDPOINT = "https://apiv2.shiprocket.in/v1/external/orders/create/adhoc"

def getTrackingEndpoint(shipment_id):
    return f"https://apiv2.shiprocket.in/v1/external/courier/track/shipment/{shipment_id}"

def getNewAuthToken():
    headers = {
        'Content-Type': 'application/json'
    }
    json_obj = {
        'email' : settings.SHIPROCKET_USER,
        'password': settings.SHIPROCKET_PASS	
    }
    try:
        response = requests.post(NEW_TOKEN_ENDPOINT, headers=headers, json=json_obj)
    except:
        print("Connection Not Made")
        return "ERROR"
    
    if(int(response.status_code) != 200):
        return "ERROR"
    res = json.loads(response.text)
    obj = ShipRocketToken.objects.get(id=1)
    obj.token = res['token']
    obj.created_at = datetime.datetime.strptime(res['created_at'], "%Y-%m-%d %H:%M:%S")
    # print(obj.token, obj.created_at)
    obj.save()


def checkShipRocketExpiryAuthToken():
    created_at = ShipRocketToken.objects.get(id=1).created_at
    if (created_at + timedelta(days=8) < datetime.datetime.now()):
        getNewAuthToken()
    
def createNewOrder(order):
    checkShipRocketExpiryAuthToken()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + ShipRocketToken.objects.get(id=1).token
    }
    json_obj = {
        'order_id': order.id,
        'order_date': datetime.datetime.strftime(order.created, "%Y-%m-%d %H:%M"), #"2022-01-11 12:44",
        'pickup_location': 'Primary',
        # 'channel_id': "",
        # 'comment': "This is a demo for Testing",
        "billing_customer_name": order.user.fname,
        "billing_last_name": order.user.lname,
        "billing_address": order.user.addresses.all()[0].address,
        "billing_city": order.user.addresses.all()[0].city,
        "billing_pincode": order.user.addresses.all()[0].postal_code,
        "billing_state": order.user.addresses.all()[0].state,
        "billing_country": order.user.addresses.all()[0].country,
        "billing_email": order.user.email,
        "billing_phone": order.user.phone_number,
        "shipping_is_billing": True,
        "shipping_customer_name": order.address.first_name,
        "shipping_last_name": order.address.last_name,
        "shipping_address": order.address.address,
        # "shipping_address_2": "",
        "shipping_city": order.address.city,
        "shipping_pincode": order.address.postal_code,
        "shipping_country": order.address.country,
        "shipping_state": order.address.state, 
        "shipping_email": order.user.email,
        "shipping_phone": order.user.phone_number,
        "payment_method": "Prepaid",
        "sub_total": order.total,
        "length": 10,
        "breadth": 10,
        "height": 10,
        "weight": 1.0
    }

    # Adding items to json_obj
    order_items = list()
    for item in order.items.all():
        order_items.append({
            "name": item.product.name,
            "units": item.quantity,
            "selling_price": int(item.price),
            "sku": str(item.product.id)
        })
    json_obj['order_items'] = order_items
    # print(json_obj)
    try:
        response = requests.post(CREATE_ENDPOINT, headers=headers, json=json_obj)
    except:
        print("Connection Not Made")
        return False
    print(response.status_code, response.text)
    if(int(response.status_code) != 200):
        return False
    res = json.loads(response.text)
    # Create a order_tracking response
    tracking = OrderTracking.objects.create(
        order=order, response=res, shiprocket_order_id=res['order_id'],
        shiprocket_shipment_id=res['shipment_id'],
    )
    tracking.save()
    return True

def trackOrder(order):
    checkShipRocketExpiryAuthToken()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + ShipRocketToken.objects.get(id=1).token
    }

    shipment_id = int(order.order_tracking.shiprocket_shipment_id)
    endpoint = getTrackingEndpoint(shipment_id)

    # Get the data
    try:
        response = requests.get(endpoint, headers=headers, json=json_obj)
    except:
        print("Connection Not Made")
        return None
    if(int(response.status_code) != 200):
        return False
    res = json.loads(response.text)
    try:
        order.order_tracking.response = res
        if res['tracking_data']['shipment_status'] == 7:
            order.order_tracking.delivered = True
    except:
        raise Exception('Order Tracking not created. Please contact support.')
    return res