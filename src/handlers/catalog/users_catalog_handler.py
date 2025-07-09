from typing import Dict

from recombee_api_client.api_requests import SetUserValues, Request, ListUserProperties

from handlers.catalog.base_catalog_handler import BaseCatalogHandler


class UsersCatalogHandler(BaseCatalogHandler):

    def get_property_types(self) -> Dict[str, str]:
        return {p["name"]: p["type"] for p in self.client.send(ListUserProperties())}

    def make_request(self, entity_id: str, values: dict) -> Request:
        return SetUserValues(entity_id, values, cascade_create=True)
