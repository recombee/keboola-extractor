import logging
from abc import ABC, abstractmethod
from typing import List, Dict
import pandas as pd
import json

from recombee_api_client.api_requests import Request
from handlers.base_handler import BaseHandler
from utils.input_table import InputTable
from utils.recombee_client_wrapper import RecombeeClientWrapper


class BaseCatalogHandler(BaseHandler, ABC):
    def __init__(
        self, table: InputTable, client: RecombeeClientWrapper, batch_size: int
    ):
        super().__init__(table, client, batch_size)
        self.property_types: Dict[str, str] = {}

    @abstractmethod
    def get_property_types(self) -> List[Dict[str, str]]:
        """Return the result of ListItemProperties or ListUserProperties"""
        pass

    @abstractmethod
    def make_request(self, entity_id: str, values: dict) -> Request:
        """Builds the appropriate Recombee request for one row."""
        pass

    def parse_value(self, key, value):
        if pd.isna(value):
            return None

        prop_type = self.property_types.get(key)
        if prop_type in {"set", "imageList"}:
            try:
                return json.loads(value)
            except (ValueError, TypeError) as e:
                logging.warning(
                    f"⚠️ Failed to parse {prop_type} for '{key}': {value} — {e}"
                )
                return None
        return value

    def handle(self):
        self.property_types = self.get_property_types()

        id_col = self.table.df.columns[0]
        requests = []

        for _, row in self.table.df.iterrows():
            entity_id = row[id_col]
            values = {
                k: self.parse_value(k, v)
                for k, v in row.drop(id_col).items()
                if pd.notna(v)
            }
            requests.append(self.make_request(entity_id, values))

        results = []
        for i in range(0, len(requests), self.batch_size):
            results.extend(
                self.client.safe_send_requests(requests[i : i + self.batch_size])
            )

        self.summarize_batch_result(results)
