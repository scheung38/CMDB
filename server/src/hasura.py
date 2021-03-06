import requests
import json
import os

HASURA_URL = os.getenv('HASURA_URL', 'http://raven:8080/v1alpha1/graphql')
ACCESS_KEY = os.getenv('HASURA_GRAPHQL_ACCESS_KEY')

def query(q, v=None):
    payload = {
        "query": q,
        "variables": v
    }

    r = requests.post(HASURA_URL, data=json.dumps(payload).encode('utf-8'), headers={'X-Hasura-Access-Key':ACCESS_KEY})
    if r.status_code != 200:
        print("===============================================")
        print("query: ", q)
        print("variables: ", v)
        print("request failed: ", r.status_code)
        print("response text: ", r.text)
        print("===============================================")
        return None
    else:
        return r.json()['data']
