import ConfigParser


class BasicConfigError(Exception):
    pass


class ConfigLockError(BasicConfigError):
    pass


class ConfigReadError(BasicConfigError):
    pass


class BaseConfigContainer(object):
    def __init__(self, init={}, name=None):
        name = name or self.__class__.__name__.lower()
        dict.__init__(self, init)
        dict.__setattr__(self, "_locked", 0)
        dict.__setattr__(self, "_name", name)

    def __getstate__(self):
        return self.__dict__.items()

    def __setstate__(self, items):
        for key, val in items:
            self.__dict__[key] = val

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, dict.__repr__(self))

    def __str__(self):
        n = self._name
        s = ["{}(name={!r}):".format(self.__class__.__name__, n)]
        s = s + ["  {}.{} = {!r}".format(n, it[0], it[1]) for it in self.items()]
        s.append("\n")
        return "\n".join(s)

    def __setitem__(self, key, value):
        if self._locked and not key in self:
            raise ConfigLockError("setting attribute on locked config container")                                                        
        return super(BaseConfigContainer, self).__setitem__(key, value)

    def __getitem__(self, name):
        return super(BaseConfigContainer, self).__getitem__(name)

    def __delitem__(self, name):
        return super(BaseConfigContainer, self).__delitem__(name)

    def lock(self):
        dict.__setattr__(self, "_locked", 1)

    def unlock(self):
        dict.__setattr__(self, "_locked", 0)

    def islocked(self):
        return self._locked

    def copy(self):
        ch = BaseConfigContainer(self)
        if self.islocked():
            ch.lock()
        return ch

    def add_section(self, name):
        self.name = SECTION(name)

    __getattr__ = __getitem__
    __setattr__ = __setitem__


class Section(BaseConfigContainer):
    def __init__(self, name):
        super(Section, self).__str__(name=name)

    def __repr__(self):
        return super(Section, self).__str__()


class Config(BaseConfigContainer):

    def mergefile(self, filename, globalspace=None):
        if os.path.isfile(filename):
            gb = globalspace or {} # temporary global namespace for config files.
            gb["Section"] = Section                                                                                                      
            gb["sys"] = sys # in case config stuff needs these.
            gb["os"] = os
            def include(fname):
                execfile(get_pathname(fname), gb, self)
            gb["include"] = include
            try:
                execfile(filename, gb, self)
            except:
                ex, val, tb = sys.exc_info()
                warnings.warn("Config: error reading %s: %s (%s)." % (filename, ex, val))
                return False
            else:
                return True
        else:
            return False


    def get_pathname(basename):
        basename = os.path.expandvars(os.path.expanduser(basename))
        if basename.find(os.sep) < 0:
            basename = os.path.join(os.sep, "etc", "qlivestats", basename)
        return basename

    def get_config(fname, initdict=None, globalspace=None, **kwargs):
        fname = get_pathname(fname)
        cf = Config()
        if cf.mergefile(fname, globalspace):
            if initdict:
                cf.update(initdict)
            cf.update(kwargs)
            return cf
        else:
            raise ConfigReadError("did not successfully read %r." % (fname,))

    def check_config(fname):
        fname = get_pathname(fname)
        cf = Config()
        if cf.mergefile(fname):
            return bool(cf)
        else:
            return False
