class CompanyNotExists(Exception):
    ...


class ConfirmationCodeNotExists(Exception):
    ...


class ConfirmationCodeExpired(Exception):
    ...


class InvalidAuthCredentials(Exception):
    ...


class VacancyNotExists(Exception):
    ...


class CompanyAlreadyExists(Exception):
    ...


class QRCodeServiceUnavailable(Exception):
    ...
