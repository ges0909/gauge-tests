import http
import json
import os
import pprint

import requests
from getgauge import logger
from getgauge.python import (
    DataStore,
    DataStoreFactory,
    after_scenario,
    after_spec,
    after_step,
    before_scenario,
    before_spec,
    before_step,
    step,
)


@before_spec()
def before_spec_hook(context):
    logger.debug(f">> before_spec_hook: {context}")


@before_scenario()
def before_scenario_hook(context):
    logger.debug(f">> before_scenario_hook: {context}")


@before_step()
def before_step_hook(context):
    logger.debug(f">> before_step_hook: {context}")


@after_spec()
def after_spec_hook(context):
    logger.debug(f">> after_spec_hook: {context}")


@after_scenario()
def after_scenario_hook(context):
    logger.debug("f>> after_scenario_hook: {context}")


@after_step()
def after_step_hook(context):
    logger.debug(f">> after_step_hook: {context}")


def http_logging(resp, *args, **kwargs):
    logger.debug(f"<< {resp.status_code} {pprint.pformat(resp.json())}")


@step("make a 'delete' request")
def delete():
    store = DataStoreFactory.scenario_data_store()
    store.put("op", "delete")
    endpoint = os.getenv("endpoint") + "/delete"
    response = requests.delete(url=endpoint, hooks={"response": http_logging})
    assert response.status_code == http.HTTPStatus.OK
    assert response.json()["url"] == endpoint


@step("make a 'get' request")
def get():
    endpoint = os.getenv("endpoint") + "/get"
    response = requests.get(url=endpoint, hooks={"response": http_logging})
    assert response.status_code == http.HTTPStatus.OK
    assert response.json()["url"] == endpoint
    store = DataStoreFactory.scenario_data_store()
    assert store.get("op") == "delete"


@step("make a 'patch' request")
def patch():
    endpoint = os.getenv("endpoint") + "/patch"
    response = requests.patch(url=endpoint, hooks={"response": http_logging})
    assert response.status_code == http.HTTPStatus.OK
    assert response.json()["url"] == endpoint


@step("make a 'post' request")
def post():
    endpoint = os.getenv("endpoint") + "/post"
    response = requests.post(url=endpoint, hooks={"response": http_logging})
    assert response.status_code == http.HTTPStatus.OK
    assert response.json()["url"] == endpoint


@step("make a 'put' request")
def put():
    endpoint = os.getenv("endpoint") + "/put"
    response = requests.put(url=endpoint, hooks={"response": http_logging})
    assert response.status_code == http.HTTPStatus.OK
    assert response.json()["url"] == endpoint


@step("if profile with with type X is requested, then profile X is returned <table>")
def get_profile(table):
    for type, name in table.rows:
        pass
