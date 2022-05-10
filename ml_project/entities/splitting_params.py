from dataclasses import dataclass, field
from typing import Optional


@dataclass()
class SplittingParams:
    val_size: float = field(default=0.2)
    random_state: int = field(default=0)
    stratify: Optional[str] = field(default=None)