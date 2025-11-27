from typing import List

from fastapi import APIRouter, HTTPException

from ..schemas import PlotCreate, PlotOut

router = APIRouter(prefix="/plots", tags=["plots"])

# Simple in-memory store for quick prototyping.
_plots: List[PlotOut] = [
    PlotOut(id=1, name="Alpha Field", location="N 27.1, E 119.6", status="moisture-low", code="A001"),
    PlotOut(id=2, name="Bamboo Slope", location="N 27.2, E 119.5", status="optimal", code="B002"),
]


@router.get("/", response_model=List[PlotOut])
def list_plots() -> List[PlotOut]:
    return _plots


@router.post("/", response_model=PlotOut, status_code=201)
def create_plot(payload: PlotCreate) -> PlotOut:
    next_id = max((p.id for p in _plots), default=0) + 1
    new_plot = PlotOut(id=next_id, **payload.dict())
    _plots.append(new_plot)
    return new_plot


@router.get("/{plot_id}", response_model=PlotOut)
def get_plot(plot_id: int) -> PlotOut:
    for plot in _plots:
        if plot.id == plot_id:
            return plot
    raise HTTPException(status_code=404, detail="Plot not found")

