from typing import Optional
from dataclasses import dataclass, field


@dataclass()
class TrainingParams:
    model_type: str = field()
    model_params: Optional[dict]