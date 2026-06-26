from fastapi import FastAPI
from validator import validate

app = FastAPI()

@app.get("/validate")
def validate_expr(expr: str):
    return validate(expr)
