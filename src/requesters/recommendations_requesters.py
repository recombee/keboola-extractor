from abc import ABC, abstractmethod
from typing import List
from collections import Counter
from dataclasses import dataclass, field
import logging

from recombee_api_client.api_requests import Request
from recombee_api_client.api_requests import RecommendItemsToUser
from recombee_api_client.api_requests import RecommendItemsToItem
from recombee_api_client.api_requests import RecommendItemSegmentsToUser

from utils.recombee_client_wrapper import RecombeeClientWrapper

from utils.output_table_writer import OutputTableWriter


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


class BaseRecommendationsRequester(ABC):
    def __init__(
        self,
        client: RecombeeClientWrapper,
        ids: List[str],
        scenario: str,
        count: int,
        included_properties: List[str],
        batch_size: int,
        writer: OutputTableWriter,
    ):
        self.client = client
        self.ids = ids
        self.scenario = scenario
        self.count = count
        self.included_properties = included_properties
        self.batch_size = batch_size
        self.writer = writer

    def send_all(self):
        requests = [self.make_request(id_) for id_ in self.ids]
        results = []

        for i in range(0, len(requests), self.batch_size):
            batch_requests = requests[i : i + self.batch_size]
            batch_ids = self.ids[i : i + self.batch_size]

            response = self.client.safe_send_requests(batch_requests)
            results.extend(response)

            for id_, result in zip(batch_ids, response):
                if result.get("code") == 200:
                    data = result.get("json", {})
                    self.writer.write_row(
                        id_value=id_,
                        recomm_id=data.get("recommId"),
                        recommended=[rec["id"] for rec in data.get("recomms", [])],
                        api_response=data,
                    )

        self.writer.finalize()
        self._summarize_results(results)

    def _summarize_results(self, results: List[dict]):
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

        self._print_summary(summary)

    def _print_summary(self, summary: BatchSummary):
        msg = f"✅ {summary.success} succeeded"
        if summary.errors > 0:
            msg += f", ❌ {summary.errors} failed"
            logging.info(msg)
            logging.info("  Error codes:")
            for code, count in summary.error_codes.items():
                logging.info(f"    - {code}: {count}x")
            logging.info("  Example errors:")
            for ex in summary.examples:
                logging.info(f"    - [{ex.code}] {ex.error}")
        else:
            logging.info(msg)

    def return_properties(self):
        return self.included_properties is not None

    @abstractmethod
    def make_request(self, id_: str) -> Request: ...


class RecommendItemsToUserRequester(BaseRecommendationsRequester):
    def make_request(self, id_: str) -> Request:
        return RecommendItemsToUser(
            user_id=id_,
            scenario=self.scenario,
            count=self.count,
            return_properties=self.return_properties(),
            included_properties=self.included_properties,
            cascade_create=True,
        )


class RecommendItemsToItemRequester(BaseRecommendationsRequester):
    def make_request(self, id_: str) -> Request:
        return RecommendItemsToItem(
            item_id=id_,
            target_user_id="null",
            scenario=self.scenario,
            count=self.count,
            return_properties=self.return_properties(),
            included_properties=self.included_properties,
            cascade_create=True,
        )


class RecommendItemSegmentsToUserRequester(BaseRecommendationsRequester):
    def make_request(self, id_: str) -> Request:
        return RecommendItemSegmentsToUser(
            user_id=id_, scenario=self.scenario, count=self.count, cascade_create=True
        )
