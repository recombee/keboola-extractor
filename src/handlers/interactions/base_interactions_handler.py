import json
import logging
from abc import ABC, abstractmethod

import pandas as pd
from recombee_api_client.api_requests import Request

from utils.input_table import InputTable
from utils.recombee_client_wrapper import RecombeeClientWrapper
from handlers.base_handler import BaseHandler


class BaseInteractionsHandler(BaseHandler, ABC):
    def __init__(
        self, table: InputTable, client: RecombeeClientWrapper, batch_size: int
    ):
        super().__init__(table, client, batch_size)

    @abstractmethod
    def to_request(self, row) -> Request:
        """Transform a single row of the table into a Recombee request object"""
        pass

    def additional_required_columns(self) -> set[str]:
        """Return a set of additional required columns for the specific interaction type"""
        return set()

    def __check_required_columns(self):
        required_cols = {"user_id", "item_id"}.union(self.additional_required_columns())
        missing = required_cols - set(self.table.df.columns)
        if missing:
            raise ValueError(
                f"Missing required column(s) {', '.join(missing)} in input table {self.table.name}"
            )

    def handle(self):

        self.__check_required_columns()

        requests = [self.to_request(row) for _, row in self.table.df.iterrows()]

        results = []
        for i in range(0, len(requests), self.batch_size):
            results.extend(
                self.client.safe_send_requests(requests[i : i + self.batch_size])
            )
        self.summarize_batch_result(results)

    def parse_additional_data(self, row) -> dict | None:
        raw = row.get("additional_data")
        if pd.isna(raw) or raw is None:
            return None
        try:
            return json.loads(raw)
        except (TypeError, ValueError):
            logging.warning(f"⚠️  Could not parse additional_data: {raw}")
            return None
