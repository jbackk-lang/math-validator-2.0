"""
api.py — FastAPI endpoint eksponujący pełny pipeline Λ–τ–ρ.
"""
from fastapi import FastAPI
from pydantic import BaseModel
from validator import validate
from plot import plot_to_dict

app = FastAPI(title="math-validator", version="2.0.0")


class ExprRequest(BaseModel):
    equation: str
    plot: bool = False
    x_min: float = -10
    x_max: float = 10


@app.post("/validate")
def validate_endpoint(req: ExprRequest):
    result = validate(req.equation)
    if req.plot:
        result["plot"] = plot_to_dict(req.equation, req.x_min, req.x_max)
    return result


@app.get("/health")
def health():
    return {"status": "ok"}
