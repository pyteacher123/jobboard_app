from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from django.http import HttpResponseBadRequest

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


class BlockURLMiddleware:
    BLOCK_URLS = ("/block",)

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.path in self.BLOCK_URLS:
            return HttpResponseBadRequest(content="This url blocked.")

        response = self.get_response(request)
        return response


class TransferRandomMessageMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        request.random_message = "Hello World"

        response = self.get_response(request)

        return response
