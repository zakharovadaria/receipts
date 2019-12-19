import os
import sys


from dotenv import load_dotenv
load_dotenv()


def get_env_name() -> str:
    env_name: str = os.getenv('ENV_NAME', 'dev')

    script_name: str = sys.argv[0]
    if script_name.startswith('tests/'):
        env_name = 'test'

    return env_name


class Config:
    DATABASE_URL: str = os.environ['DATABASE_URL']

    BASIC_AUTH_ADMIN_NAME: str = os.environ['BASIC_AUTH_ADMIN_NAME']
    BASIC_AUTH_ADMIN_PASS: str = os.environ['BASIC_AUTH_ADMIN_PASS']

    BASIC_AUTH_CLIENT_NAME: str = os.environ['BASIC_AUTH_CLIENT_NAME']
    BASIC_AUTH_CLIENT_PASS: str = os.environ['BASIC_AUTH_CLIENT_PASS']

    BASIC_AUTH_ADMIN_PANEL_NAME: str = os.environ['BASIC_AUTH_ADMIN_PANEL_NAME']
    BASIC_AUTH_ADMIN_PANEL_PASS: str = os.environ['BASIC_AUTH_ADMIN_PANEL_PASS']

    DEBUG: bool = False
    TESTING: bool = False


class TestConfig(Config):
    DATABASE_URL: str = os.environ['TEST_DATABASE_URL']
    TESTING: bool = True


class DevelopmentConfig(Config):
    DEBUG: bool = True


class ProductionConfig(Config):
    pass


config_by_env_name: dict = dict(
    test=TestConfig,
    dev=DevelopmentConfig,
    prod=ProductionConfig,
)

ENV_NAME: str = get_env_name()
CONFIG: Config = config_by_env_name[ENV_NAME]
