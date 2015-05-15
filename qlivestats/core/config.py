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
        return "%s(%s)" % (self.__class__.__name__, dict.__repr__(self))

    def __str__(self):
        n = self._name
        s = ["{}(name={!r}):".format(self.__class__.__name__, n)]
        s = s + ["  {}.{} = {!r}".format(n, it[0], it[1]) for it in self.config.items()]
        s.append("\n")
        return "\n".join(s)


class YAMLConfig(BaseHolder):
    def get_filename(self):
        return self.config

