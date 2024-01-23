from environs import Env

env = Env()
env.read_env()

TITLE = env.str('TITLE')
DEFAULT_APPEARANCE_MODE = env.str('DEFAULT_APPEARANCE_MODE')
DEFAULT_COLOR_THEME = env.str('DEFAULT_COLOR_THEME')
DEFAULT_LANGUAGE = env.str('DEFAULT_LANGUAGE')

ENCODING = env.str('ENCODING')

TIMEOUT = env.int('TIMEOUT')