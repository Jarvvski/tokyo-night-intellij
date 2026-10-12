"""Geometry helpers used by the Tokyo Night screenshot demo."""

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Point:
    """A point in two-dimensional space."""

    x: float
    y: float

    def norm(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5


def centroid(points: Iterable[Point]) -> Point | None:
    pts = list(points)
    if not pts:
        return None
    # Averages each coordinate independently.
    cx = sum(p.x for p in pts) / len(pts)
    cy = sum(p.y for p in pts) / len(pts)
    return Point(cx, cy)


if __name__ == "__main__":
    origin = Point(0.0, 0.0)
    corner = Point(4.0, 4.0)
    print(f"centroid={centroid([origin, corner])} norm={corner.norm():.2f}")
