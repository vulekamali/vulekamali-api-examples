"""
Example queries against the OpenSpending API.
OpenSpending provides an API to structured South African Budget
and Expenditure data.

Official OpenSpending API documentation at
 https://docs.openspending.org/en/latest/developers/api/
"""

import requests
import logging
import json

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

PAGE_SIZE = 10000

logger.info(("\n\nRequesting the OpenSpending model for the"
             " 2019 Estimates of National Expenditure"))
# Get the model URL for an OpenSpending dataset endpoint from vulekamali.gov.za
# or data.vulekamali.gov.za
model_url = "https://openspending.org/api/3/cubes/b9d2af843f3a7ca223eea07fb608e62a:estimates-of-national-expenditure-2019-20-uploaded-2019-02-20t1910/model/"

# Request the model
model_result = requests.get(model_url)

# It's always a good idea to raise an exception upon unexpected errors
model_result.raise_for_status()

logger.info("Result:\n%s", json.dumps(model_result.json(), sort_keys=True, indent=4))
