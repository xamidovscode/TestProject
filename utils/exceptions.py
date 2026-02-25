from rest_framework.exceptions import APIException as DRFAPIException


class BadRequest(DRFAPIException):
    status_code = 400
    default_detail = {'detail': 'Something went wrong'}
