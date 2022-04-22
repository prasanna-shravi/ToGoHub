#Using Pytest framework to write unit tests to test the APIs
import pytest
import requests

#Test to check whether the flask application is properly served
def test_flaskapp():
    """Test the default route."""

    res = requests.get("http://localhost:5000/")
    assert res.status_code == 200
    assert res.content == b'TOGOHUB Food Ordering App.'

#Test to verify whether the create order API is working as expected
def test_createorder():
    """Test the default route."""

    jsonbody = {
                    "user_id" : 1,
                    "order_items" : [
                        {
                            "item_id": 1,
                            "item_count": 3
                        },
                        {
                            "item_id": 4,
                            "item_count": 2
                        }
                    ]
                }

    res = requests.post("http://localhost:5000/order/",json=jsonbody)
    assert res.status_code == 200

#Test to verify the get all orders API
def test_getallorders():
    """Test the default route."""

    res = requests.get("http://localhost:5000/orders/")
    assert res.status_code == 200