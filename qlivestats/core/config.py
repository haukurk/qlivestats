import yaml 
import os


class BaseConfigError(Exception):
    pass


class ConfigParsingError(BaseConfigError):
    pass


class ConfigReadError(BaseConfigError):
    pass


class BaseHolder(object):
    def __init__(self, configfile="/etc/qlivestats.yaml"):
        self.name = self.__class__.__name__.lower()
        self.config = None
        try:
            if not os.path.isfile(configfile):
                raise ConfigReadError("Cannot find the configuration file.")
            self.config = yaml.load(file(configfile))
        except yaml.YAMLError, exc:
            self.config = None
            if hasattr(exc, 'problem_mark'):
                mark = exc.problem_mark
                error_message = "Error position: (%s:%s)" % (mark.line+1, mark.column+1)
                raise ConfigParsingError(error_message)
            raise ConfigParsingError("Unknown Error")
        self.filename = configfile

    def __repr__(self):
        return "%s (sections: %s)" % (self.__class__.__name__, len(self.config))

    def __str__(self):
        return yaml.dump(self.config) 


class YAMLConfig(BaseHolder):
    def get_filename(self):
        return self.filename

    def get_broker(self):
        return self.config["livestatus"]["broker"]

