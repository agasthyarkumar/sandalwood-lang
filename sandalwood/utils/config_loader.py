from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _config_root() -> Path:
    return Path(__file__).resolve().parents[2] / "config"


def load_config(name: str) -> dict[str, Any]:
    config_path = _config_root() / name
    with config_path.open("r", encoding="utf-8") as config_file:
        return json.load(config_file)
