# coding: utf-8
from elasticsearch import Elasticsearch, helpers
import certifi
import yaml
import json
import pandas as pd

with open("./conf/setting.yaml") as conf:
    config = yaml.load(conf)

ES_URL = config["elasticsearch.url"]
USE_SSL = config["use.ssl"]
USER = config["elasticsearch.user"]
PW = config["elasticsearch.pass"]

es = Elasticsearch(ES_URL, http_auth=(
    USER, PW), use_ssl=USE_SSL, ca_certs=certifi.where(),
    sort="time:asc", timeout=30)


# dataframeを投入する
def bulk_insert(index_name, df: pd.core.frame.DataFrame):

    json_list_str = df.to_json(force_ascii=False, orient='records')
    json_list = json.loads(json_list_str)

    actions = []
    for insert_data_json in json_list:
        actions.append({
            "_index": index_name,
            "_type": "_doc",
            "_source": insert_data_json
        })
    # bulk insert
    helpers.bulk(es, actions)
