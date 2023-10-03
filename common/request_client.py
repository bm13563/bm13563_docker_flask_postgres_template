from time import sleep

from requests import get, post, put, delete

from common.logging import get_logger


logger = get_logger()


METHODS = {
    "get": get,
    "post": post,
    "put": put,
    "delete": delete,
}


class RequestClient:
    def __init__(self, retries=5, backoff=5):
        self.retries = retries
        self.backoff = backoff

    def _make_request(self, method, url, params):
        method = METHODS[method]
        for _ in range(self.retries):
            try:
                response = method(url, params=params)
                response.raise_for_status()
                logger.info(
                    "request successful",
                    extra={"url": url, "params": params},
                )
                return {"data": response, "status_code": response.status_code}
            except Exception as e:
                logger.error(
                    "error while making request",
                    extra={"url": url, "params": params, "error": e},
                )
                sleep(self.backoff)
        return None

    def get(self, url, params=None):
        logger.info("making get request", extra={"url": url, "params": params})
        return self._make_request("get", url, params)
