from typing import List, Dict

from recombee_api_client.api_requests import SetItemValues, Request, ListItemProperties

from handlers.catalog.base_catalog_handler import BaseCatalogHandler


class ItemsCatalogHandler(BaseCatalogHandler):
    def get_property_types(self) -> Dict[str, str]:
        return {p["name"]: p["type"] for p in self.client.send(ListItemProperties())}

    def make_request(self, entity_id: str, values: dict) -> Request:
        return SetItemValues(entity_id, values, cascade_create=True)
