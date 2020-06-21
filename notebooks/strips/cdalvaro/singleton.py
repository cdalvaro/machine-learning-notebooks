class Singleton(type):
    """
    Metaclase para implementar el patrón de diseño Singleton
    https://stackoverflow.com/a/6798042/3398062
    """
    _instances = dict()

    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            self._instances[self] = super(
                Singleton, self).__call__(*args, **kwargs)
        return self._instances[self]
