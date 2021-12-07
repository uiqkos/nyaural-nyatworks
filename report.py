from dataclasses import dataclass


@dataclass
class ModelReport:
    model_name: str
    desc: str
    arch_desc: str
    arch_img: str
    arch_img_desc: str
    history: list
    metrics: list[tuple[str, str]]
