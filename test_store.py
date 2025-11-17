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
def new_order_payload():
    return {
        "petId": 12345699999999,
        "quantity": 1,
        "shipDate": "2025-01-05T12:00:00Z",
        "status": "placed",
        "complete": False
    }

def test_patch_order_by_id(new_order_payload):

    # 1. Create an order first (pre-condition)
    create_resp = api_helpers.post_api_data("/store/order", new_order_payload)
    assert create_resp.status_code == 200

    created_order = create_resp.json()
    order_id = created_order["id"]
    pet_id = created_order["petId"]

    # 2. Prepare PATCH payload
    patch_payload = {
        "status": "approved"
    }

    # 3. Execute PATCH request
    patch_resp = api_helpers.patch_api_data(f"/store/order/{order_id}", patch_payload)

    # --- Validate response status ---
    assert_that(patch_resp.status_code, is_(200))

    patch_json = patch_resp.json()

    # --- Optional: Schema validation ---
    validate(instance=patch_json, schema=schemas.OrderPatchResponseSchema)

    # --- Validate response fields ---
    assert patch_json["orderId"] == order_id
    assert patch_json["petId"] == pet_id
    assert patch_json["status"] == "approved"

    # --- Validate success message ---
    assert_that(
        patch_json["message"],
        contains_string("Order and pet status updated successfully")
    )
