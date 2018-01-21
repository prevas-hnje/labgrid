import sys

import requests
from ..exception import ExecutionError

def _check_relay_count(host, index):
   try:
        # get the number of active relays
        r = requests.get("http://{}/relays/count".format(host))
        r.raise_for_status()
        assert 0 <= index <= r.json()['count']
    except json.decoder.JSONDecodeError as e:
        raise ExecutionError("failed to get number of relays") from e

def set(host, index, value):
    index = int(index)
    # ensure the relay is valid
    _check_relay_count(host, index)
    # access the rest api
    r = requests.put("http://{}/relays/{}/state/{}".format(host,index, int(value)))
    r.raise_for_status()

def get(host, index):
    index = int(index)
    # ensure the relay is valid
    _check_relay_count(host, index)
    # get the contents of the main page
    r = requests.get("http://{}/relays/{}/state".format(host,index))
    value = r.json()['state']
    r.raise_for_status()

    return True if value == "1" else False
