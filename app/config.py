import logging
import logging.config

from envyaml import EnvYAML

from os import environ


logger = logging.getLogger(__name__)


def get_config() -> EnvYAML:
    try:
        configuration = EnvYAML(environ["CONFIG_PATH"])
        return configuration
    except Exception as exc:
        logger.error(exc)
        raise exc

def set_up_loggers() -> None:
    configuration = get_config()

    log_file_path = configuration["logging"]["config"]["path"]
    logging.config.fileConfig(log_file_path, disable_existing_loggers=True)

def get_tor_config():
    configuration = get_config()

    return configuration["tor"]["host"], configuration["tor"]["port"]
