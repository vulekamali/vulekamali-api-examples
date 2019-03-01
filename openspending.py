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

def get_model(model_ur):
    logger.info(("\n\nRequesting the OpenSpending model for the"
                 " 2019 Estimates of National Expenditure"))
    # Get the model URL for an OpenSpending dataset endpoint from
    # vulekamali.gov.za or data.vulekamali.gov.za

    # Request the model
    model_result = requests.get(model_url)

    # It's always a good idea to raise an exception upon unexpected errors
    model_result.raise_for_status()

    logger.info("Result:\n%s", json.dumps(model_result.json(), sort_keys=True, indent=4))

    return model_result.json()['model']


def get_summary(model_url):
    model = get_model(model_url)

    department_dimension = model['hierarchies']['administrative_classification']['levels'][0]
    department_ref = model['dimensions'][department_dimension]['label' + "_ref"]

    budget_phase_dimension = model['hierarchies']['phase']['levels'][0]
    budget_phase_ref = model['dimensions'][budget_phase_dimension]['label' + "_ref"]

    financial_year_dimension = model['hierarchies']['date']['levels'][0]
    financial_year_ref = model['dimensions'][financial_year_dimension]['label' + "_ref"]

    cuts = [
        "{}:Main appropriation".format(budget_phase_ref),
        "{}:2019".format(financial_year_ref),
    ]
    drilldowns = [
        department_ref,
    ]

    params = {
        'pagesize': PAGE_SIZE,
    }
    params['cut'] = "|".join(cuts)
    params['drilldown'] = "|".join(drilldowns)

    aggregate_url = model_url.replace("model", "aggregate")
    logger.info("\n\nRequesting a summary of department budgets:")
    logger.info("cuts: %r", cuts)
    logger.info("drilldowns: %r", drilldowns)
    aggregate_result = requests.get(aggregate_url, params=params)
    aggregate_result.raise_for_status()
    logger.info("Result:\n%s", json.dumps(aggregate_result.json(), sort_keys=True, indent=4))

    # You can verify these totals on page 11 of the budget publications like
    # https://data.vulekamali.gov.za/dataset/f07a6899-7fb1-4ec8-9f60-8f5a53c13e21/resource/1639f97e-2ba8-4cd9-9f8a-3cf282065440/download/vote-24-agriculture-forestry-and-fisheries.pdf
    # and
    # https://data.vulekamali.gov.za/dataset/b64c6843-744e-4c82-87bc-5e8d6ac658a7/resource/8a207f04-4ad4-4674-9f28-35652eb8725b/download/vote-14-basic-education.pdf
    # Find links to them on department pages like
    # https://vulekamali.gov.za/2019-20/national/departments/basic-education


model_url = "https://openspending.org/api/3/cubes/b9d2af843f3a7ca223eea07fb608e62a:estimates-of-national-expenditure-2019-20-uploaded-2019-02-20t1910/model/"

get_summary(model_url)
