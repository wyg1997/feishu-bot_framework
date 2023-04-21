import yaml
import logging

from larksuiteoapi import Config, DOMAIN_FEISHU, DefaultLogger, LEVEL_DEBUG


def load_global_config(path):
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    return config


global_config = load_global_config("config.yaml")


def _get_sdk_config():
    app_settings = Config.new_internal_app_settings(
        app_id=global_config["APP_ID"],
        app_secret=global_config["APP_SECRET"],
        verification_token=global_config["APP_VERIFICATION_TOKEN"],
        encrypt_key=global_config["APP_ENCRYPT_KEY"],
    )
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
    # TODO: log level use config file
    sdk_config = Config.new_config_with_memory_store(
        DOMAIN_FEISHU, app_settings, DefaultLogger(), LEVEL_DEBUG
    )
    return sdk_config


sdk_config = _get_sdk_config()
