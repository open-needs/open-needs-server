class ONSExtensionException(BaseException):
    """Generic Exception for Open-Needs Server Extensions"""

    @property
    def msg(self):
        return str(self.args[0])
