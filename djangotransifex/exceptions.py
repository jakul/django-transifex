class DjangoTransifexException(Exception):
    pass

class DjangoTransifexAPIException(DjangoTransifexException):
    pass

class LanguageCodeNotAllowed(DjangoTransifexException):
    pass

class NoPoFilesFound(DjangoTransifexException):
    pass

class ProjectNotFound(DjangoTransifexException):
    pass

class ResourceNotFound(DjangoTransifexException):
    pass



