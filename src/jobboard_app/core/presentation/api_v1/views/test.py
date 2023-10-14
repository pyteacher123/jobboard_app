from __future__ import annotations

import time
from typing import TYPE_CHECKING

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

if TYPE_CHECKING:
    from rest_framework.request import Request


@api_view(http_method_names=["GET"])
def test_controller(request: Request) -> Response:
    time.sleep(1)
    return Response(data={"message": "Hello World!"}, status=HTTP_200_OK)


@api_view(http_method_names=["GET"])
def test2_controller(request: Request) -> Response:
    return Response(data={"message": "Hello World!"}, status=HTTP_200_OK)
