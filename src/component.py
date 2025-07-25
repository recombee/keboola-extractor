import os
import logging

from keboola.component.base import ComponentBase
from keboola.component.exceptions import UserException

from recombee_api_client.exceptions import ResponseException

from utils.output_table_writer import OutputTableWriter
from utils.config import Config
from utils.input_table import InputTable
from utils.recombee_client_wrapper import RecombeeClientWrapper

from requesters.recommendations_requesters import RecommendItemsToUserRequester
from requesters.recommendations_requesters import RecommendItemsToItemRequester
from requesters.recommendations_requesters import RecommendItemSegmentsToUserRequester


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

            # Select endpoint class
            endpoint_map = {
                "Recommend Items to User": RecommendItemsToUserRequester,
                "Recommend Items to Item": RecommendItemsToItemRequester,
                "Recommend Item Segments to User": RecommendItemSegmentsToUserRequester,
            }

            if config.endpoint not in endpoint_map:
                raise UserException(f"Unknown endpoint: '{config.endpoint}'")

            if config.endpoint == "Recommend Items to User":
                input_name = "users.csv"
                result_id_column = "user_id"
                result_recommended_ids_column = "recommended_items"
            elif config.endpoint == "Recommend Item Segments to User":
                input_name = "users.csv"
                result_id_column = "user_id"
                result_recommended_ids_column = "recommended_item_segments"
            elif config.endpoint == "Recommend Items to Item":
                input_name = "items.csv"
                result_id_column = "item_id"
                result_recommended_ids_column = "recommended_items"
            else:
                raise UserException(f"No input logic for endpoint: '{config.endpoint}'")

            # Load matching input table
            table_def = next(
                (
                    t
                    for t in input_tables
                    if os.path.basename(t.full_path).lower() == input_name
                ),
                None,
            )
            if not table_def:
                raise UserException(
                    f"Missing required input file '{input_name}' for endpoint '{config.endpoint}'"
                )

            table = InputTable(table_def.full_path)
            ids = list(table.df.iloc[:, 0])

            writer = OutputTableWriter(
                id_column=result_id_column, result_column=result_recommended_ids_column
            )

            # Run recommender
            RequesterClass = endpoint_map[config.endpoint]
            requester = RequesterClass(
                client=client,
                ids=ids,
                scenario=config.scenario,
                count=config.count,
                included_properties=config.included_properties,
                batch_size=config.batch_size,
                writer=writer,
            )
            requester.send_all()

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
