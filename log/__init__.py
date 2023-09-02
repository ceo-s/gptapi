import json
import logging.config

with open("log/config.json") as config:
    conf_dict = json.load(config)

logging.config.dictConfig(conf_dict)
logger = logging.getLogger("base_logger")
