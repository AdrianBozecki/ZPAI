import logging

from aiohttp import ClientResponse, ClientSession, hdrs, ClientTimeout
from starlette import status

from settings import settings

logger = logging.getLogger("foo-logger")

class BaseHTTPClient():

    def __init__(self, base_url: str, headers):
        self.base_url = base_url
        self.headers = headers

    @staticmethod
    async def read_response(
            response: ClientResponse,
    ) -> dict[str, any] | bytes:
        """
        Read response based on content type.
        :param response: ClientResponse
        :return: response data
        """
        return (
            await response.json()
            if response.content_type == "application/json"
            else await response.read()
        )

    def _prepare_url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def _prepare_request_params(
        self,
        path: str,
        method: str = hdrs.METH_GET,
        json: dict[str, any] | None = None,
        params: dict[str, any] | None = None,
    ) -> dict[str, any]:
        """
        Prepare request params.
        :param path: url path
        :param method: http method
        :param data: data
        :param timeout: request timeout passes as ClientTimeout object
        :return: request params
        """
        timeout = ClientTimeout(total=5)
        return {
            "url": self._prepare_url(path),
            "headers": self.headers,
            "raise_for_status": False,
            "method": method,
            "timeout": timeout,
            "allow_redirects": False,
            "json": json,
            "params": params,
        }

    async def make_request(
        self,
        path: str,
        method: str = hdrs.METH_GET,
        json: dict[str, any] | None = None,
        params: dict[str, any] | None = None,
        timeout: ClientTimeout | None = None,
    ) -> dict[str, any] | list[any] | bytes | None:
        """
        Prepare request and send it to the client.
        :param path: url path
        :param method: http method
        :param data: data
        :param json: json data
        :param timeout: request timeout passes as ClientTimeout object
        :param ignore_not_found: true if we should skip raising ClientResponseError for 404
        :param validate_result: true if we should validate result
        :return: response data
        """
        params = self._prepare_request_params(path, method, json, params)

        logger.debug(f"Sending {params['method']} request to '{params['url']}'...")

        result = await self._make_request(params, path)
        return result


    async def _make_request(
        self,
        params: dict[str, any],
        path: str,
    ) -> dict[str, any] | list[any] | bytes | None:
        async with ClientSession() as session:

            async with session.request(**params) as response:  # type: ignore
                logger.info(
                    f"{params['method']} request send to '{path}' "
                    f"using client {self.__class__.__name__} "
                    f"returned '{response.status}' status code.",
                )

                response.raise_for_status()
                result = await self.read_response(response)
                logger.debug(f"{params['method']} request to '{path}' returned {result!r}")
                return result