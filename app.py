from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from validator import validate

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
    <body style="font-family: Arial; padding: 20px;">
        <h2>Math Validator API</h2>
        <p>Użyj endpointu <code>/validate?expr=...</code></p>
        <form action="/validate">
            <input name="expr" placeholder="1/(x-1)" size="40" />
            <button type="submit">Validate</button>
        </form>
    </body>
    </html>
    """


@app.get("/validate")
def validate_expr(expr: str):
    return validate(expr)
