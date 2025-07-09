import json


class Config:
    REQUIRED_KEYS = ["database_id", "#private_token"]

    def __init__(self, path: str = "/data/config.json"):
        self._load(path)

    def _load(self, path):
        with open(path) as f:
            config = json.load(f)

        if "parameters" not in config:
            raise ValueError("Missing 'parameters' section in config.json")

        self._params = config["parameters"]

        # Validate required keys
        missing = [
            key
            for key in self.REQUIRED_KEYS
            if key not in self._params or not self._params[key]
        ]
        if missing:
            raise ValueError(
                f"Missing required config parameter(s): {', '.join(missing)}"
            )

    @property
    def db_id(self) -> str:
        return self._params["database_id"]

    @property
    def token(self) -> str:
        return self._params["#private_token"]

    @property
    def region(self) -> str:
        return self._params.get("region", "eu-west")

    @property
    def batch_size(self) -> int:
        return int(self._params.get("batch_size", 1000))
