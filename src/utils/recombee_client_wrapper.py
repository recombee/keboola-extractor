import time
import logging
from typing import List

from recombee_api_client.api_client import RecombeeClient, Region
from recombee_api_client.api_requests import Batch, Request
from recombee_api_client.exceptions import ResponseException, ApiTimeoutException


class RecombeeClientWrapper:
    def __init__(self, db_id, token, region_str):
        region = Region[region_str.upper().replace("-", "_")]
        self.client = RecombeeClient(db_id, token, region=region)

    def send(self, request: Request):
        return self.client.send(request)

    def safe_send_requests(self, requests: List[Request], retries=3):
        if not requests:
            return []

        req = Batch(requests)
        req.timeout *= 5

        try:
            res = self.client.send(req)
            return res

        except ResponseException as e:
            if e.status_code >= 500 and retries > 0:
                logging.warning("⚠️  Server error. Retrying in 20 seconds...")
                time.sleep(20)
                return self.safe_send_requests(requests, retries - 1)
            raise e

        except ApiTimeoutException:
            if retries > 0:
                logging.warning("⚠️  Timeout error. Retrying in 20 seconds...")
                time.sleep(20)
                return self.safe_send_requests(requests, retries - 1)
            raise
