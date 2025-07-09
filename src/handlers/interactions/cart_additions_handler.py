from recombee_api_client.api_requests import AddCartAddition, Request

from handlers.interactions.base_interactions_handler import BaseInteractionsHandler
from utils.input_table import InputTable
from utils.recombee_client_wrapper import RecombeeClientWrapper


class CartAdditionsHandlerBase(BaseInteractionsHandler):
    def __init__(
        self, table: InputTable, client: RecombeeClientWrapper, batch_size: int
    ):
        super().__init__(table, client, batch_size)

    def to_request(self, row) -> Request:
        return AddCartAddition(
            user_id=self.safe_get(row, "user_id"),
            item_id=self.safe_get(row, "item_id"),
            timestamp=self.safe_get(row, "timestamp"),
            amount=self.to_float(self.safe_get(row, "amount")),
            recomm_id=self.safe_get(row, "recomm_id"),
            additional_data=self.parse_additional_data(row),
            cascade_create=True,
        )
