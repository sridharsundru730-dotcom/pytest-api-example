from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_

'''
TODO: Finish this test by...
1) Creating a function to test the PATCH request /store/order/{order_id}
2) *Optional* Consider using @pytest.fixture to create unique test data for each run
2) *Optional* Consider creating an 'Order' model in schemas.py and validating it in the test
3) Validate the response codes and values
4) Validate the response message "Order and pet status updated successfully"
'''

@pytest.fixture
def order_payload():
    return {
        "pet_id": 0,
        "quantity": 1,
        "status": "available",
        "complete": False
    }

def test_patch_order_by_id(order_payload):

    create_resp = api_helpers.post_api_data("/store/order", order_payload)
    assert create_resp.status_code == 201

    created_order = create_resp.json()
    order_id = created_order["id"]
    pet_id = created_order["pet_id"]

    # 2. Prepare PATCH payload
    patch_payload = {
        "status": "available"
    }

    patch_resp = api_helpers.patch_api_data(f"/store/order/{order_id}", patch_payload)
    assert_that(patch_resp.status_code, is_(200))
    patch_json = patch_resp.json()

    assert_that(
        patch_json["message"],
        contains_string("Order and pet status updated successfully")
    )
