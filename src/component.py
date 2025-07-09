import sys
import logging
from keboola.component.base import ComponentBase
from keboola.component.exceptions import UserException

from recombee_api_client.exceptions import ResponseException

from handlers.catalog.items_catalog_handler import ItemsCatalogHandler
from handlers.catalog.users_catalog_handler import UsersCatalogHandler
from handlers.interactions.bookmarks_handler import BookmarksHandlerBase
from handlers.interactions.cart_additions_handler import CartAdditionsHandlerBase
from handlers.interactions.detail_views_handler import DetailViewsHandlerBase
from handlers.interactions.purchases_handler import PurchasesHandlerBase
from handlers.interactions.ratings_handler import RatingsHandlerBase
from handlers.interactions.view_portions_handler import ViewPortionsHandlerBase
from utils.config import Config
from utils.input_table import InputTable
from utils.recombee_client_wrapper import RecombeeClientWrapper


class Component(ComponentBase):
    def __init__(self):
        super().__init__()

    def run(self):
        try:
            config = Config()
            client = RecombeeClientWrapper(
                db_id=config.db_id, token=config.token, region_str=config.region
            )

            input_tables = self.get_input_tables_definitions()
            if not input_tables:
                raise UserException("No input tables found")

            for table_def in input_tables:
                table = InputTable(table_def.full_path)

                if table.is_items_catalog():
                    handler = ItemsCatalogHandler(table, client, config.batch_size)
                elif table.is_users_catalog():
                    handler = UsersCatalogHandler(table, client, config.batch_size)
                elif table.is_bookmarks():
                    handler = BookmarksHandlerBase(table, client, config.batch_size)
                elif table.is_cart_additions():
                    handler = CartAdditionsHandlerBase(table, client, config.batch_size)
                elif table.is_detail_views():
                    handler = DetailViewsHandlerBase(table, client, config.batch_size)
                elif table.is_purchases():
                    handler = PurchasesHandlerBase(table, client, config.batch_size)
                elif table.is_ratings():
                    handler = RatingsHandlerBase(table, client, config.batch_size)
                elif table.is_view_portions():
                    handler = ViewPortionsHandlerBase(table, client, config.batch_size)
                else:
                    logging.warning(f"Skipping unrecognized table: {table.name}")
                    continue

                logging.info(f"Processing table: {table.name}")
                handler.handle()

        except ValueError as e:
            logging.exception(e)
            exit(1)
        except ResponseException as e:
            logging.exception(e)
            if e.status_code >= 500:
                exit(2)
            exit(1)


if __name__ == "__main__":
    try:
        comp = Component()
        comp.execute_action()
    except UserException as exc:
        logging.exception(exc)
        exit(1)
    except Exception as exc:
        logging.exception(exc)
        exit(2)
