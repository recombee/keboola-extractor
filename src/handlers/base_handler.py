from abc import ABC, abstractmethod

import pandas as pd
import logging

from collections import Counter
from typing import List
from dataclasses import dataclass, field

from utils.input_table import InputTable
from utils.recombee_client_wrapper import RecombeeClientWrapper


@dataclass
class ErrorExample:
    code: int
    error: str


@dataclass
class BatchSummary:
    total: int = 0
    success: int = 0
    errors: int = 0
    error_codes: Counter = field(default_factory=Counter)
    error_messages: Counter = field(default_factory=Counter)
    examples: List[ErrorExample] = field(default_factory=list)


class BaseHandler(ABC):
    def __init__(
        self, table: InputTable, client: RecombeeClientWrapper, batch_size: int
    ):
        self.table = table
        self.client = client
        self.batch_size = batch_size

    @abstractmethod
    def handle(self): ...

    @staticmethod
    def safe_get(row, column: str):
        value = row.get(column)
        return None if pd.isna(value) else value

    @staticmethod
    def to_float(value):
        try:
            return float(value) if value is not None else None
        except (ValueError, TypeError):
            return None

    def summarize_batch_result(self, results: List[dict]) -> BatchSummary:
        summary = BatchSummary(total=len(results))

        for result in results:
            code = result.get("code")
            if 200 <= code <= 299:
                summary.success += 1
            else:
                summary.errors += 1
                summary.error_codes[code] += 1
                error_msg = result.get("json", {}).get("error") or result.get(
                    "json", ""
                )
                summary.error_messages[str(error_msg)] += 1

                if len(summary.examples) < 5:
                    summary.examples.append(ErrorExample(code, error_msg))

        self.__print_batch_result_summarization(summary)
        return summary

    def __print_batch_result_summarization(self, summary: BatchSummary):
        msg = f"✅ {summary.success} succeeded"

        if summary.errors > 0:
            msg += f" ❌ {summary.errors} failed"
            logging.info(msg)
            logging.info("  Error codes:")
            for code, count in summary.error_codes.items():
                logging.info(f"    - {code}: {count}x")

            logging.info("  Example errors:")
            for ex in summary.examples:
                logging.info(f"    - [{ex.code}] {ex.error}")
        else:
            logging.info(msg)
