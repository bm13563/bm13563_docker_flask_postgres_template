from os import environ

def pytest_configure(config):
    """
        Allows plugins and conftest files to perform initial configuration.
        This hook is called for every plugin and initial conftest
        file after command line options have been parsed.
    """
    environ["DB_HOST"] = "localhost"