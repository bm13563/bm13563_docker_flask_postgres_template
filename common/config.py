from copy import deepcopy
from os import path, curdir, environ
from dotenv import load_dotenv


class Config:
    """
    This is a wrapper around the os.environ object. It allows us to
    load environment variables from a file, and then override them
    with environment variables set in the shell.
    """

    def __init__(self):
        self.env = deepcopy(environ)

        root = path.abspath(curdir)
        config_path = self.env.get("CONFIG_PATH", "/settings/local.cfg")
        load_dotenv(f"{root}{config_path}")

        self.env_file = deepcopy(environ)

        for key, value in environ.items():
            if key in self.env:
                continue
            else:
                self.env[key] = value

    def get(self, name, default=None):
        if self.env.get(name) == "True":
            return True
        elif self.env.get(name) == "False":
            return False
        else:
            return self.env.get(name, default)
