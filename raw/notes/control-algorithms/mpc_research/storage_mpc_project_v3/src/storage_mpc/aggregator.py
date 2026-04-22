from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ResourceState:
    name: str
    value: float


@dataclass
class ResourceControl:
    name: str
    lower_bound: float
    upper_bound: float


class MultiResourceAggregator:
    """多资源聚合骨架。

    用于后续扩展为：
    - 多储能
    - 光伏 + 储能
    - 柔性负荷
    - 柴油机 / 燃机
    - 需求响应资源
    """

    def __init__(self) -> None:
        self.states: list[ResourceState] = []
        self.controls: list[ResourceControl] = []

    def register_state(self, state: ResourceState) -> None:
        self.states.append(state)

    def register_control(self, control: ResourceControl) -> None:
        self.controls.append(control)
