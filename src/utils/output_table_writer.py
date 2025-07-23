import os
import csv
import json
from keboola.component import CommonInterface


class OutputTableWriter:
    """
    Writes recommendation results to a Keboola-compatible output table using the CommonInterface.
    """

    def __init__(
        self,
        id_column: str,
        result_column: str,
        filename: str = "recommendations.csv",
    ):
        self.ci = CommonInterface()
        self.filename = filename
        self.id_column = id_column
        self.result_column = result_column
        self.columns = [self.id_column, "recomm_id", self.result_column, "api_response"]

        self.full_path = os.path.join(self.ci.tables_out_path, self.filename)
        self.destination = os.path.splitext(self.filename)[0]  # Remove .csv

        # Define table schema and manifest
        self.table = self.ci.create_out_table_definition(
            self.filename,
            schema=self.columns,
            destination=self.destination,
            primary_key=[self.id_column],
            incremental=False,
        )

        # Open CSV writer
        self.csv_file = open(
            self.table.full_path, mode="w", encoding="utf-8", newline=""
        )
        self.writer = csv.DictWriter(self.csv_file, fieldnames=self.columns)
        self.writer.writeheader()

    def write_row(
        self, id_value: str, recomm_id: str, recommended: list, api_response: dict
    ):
        row = {
            self.id_column: id_value,
            "recomm_id": recomm_id,
            self.result_column: json.dumps(recommended),
            "api_response": json.dumps(api_response),
        }
        self.writer.writerow(row)

    def finalize(self):
        self.csv_file.close()
        self.ci.write_manifest(self.table)
