from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from validator import validate
import json

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def ui():
    return """
    <html>
    <head>
        <title>Math Validator — Filters Panel</title>
        <style>
            body { font-family: Arial; background: #0d0d0d; color: #eee; padding: 30px; }
            #box { background: #1a1a1a; padding: 25px; border-radius: 12px; width: 800px; margin: auto; box-shadow: 0 0 20px #00ffcc55; }
            input { width: 500px; padding: 10px; font-size: 18px; background: #111; color: #0f0; border: 1px solid #0f0; }
            button { padding: 10px 20px; font-size: 18px; cursor: pointer; background: #0f0; color: #000; border: none; }
            pre { background: #000; color: #0f0; padding: 15px; border-radius: 10px; margin-top: 20px; font-size: 15px; }
            .filter-box { margin-top: 20px; padding: 15px; background: #111; border-left: 4px solid #0f0; }
            .title { font-size: 22px; margin-bottom: 10px; color: #0f0; }
            .pulse { animation: pulse 1.5s infinite; }
            @keyframes pulse {
                0% { box-shadow: 0 0 5px #0f0; }
                50% { box-shadow: 0 0 20px #0f0; }
                100% { box-shadow: 0 0 5px #0f0; }
            }
        </style>
    </head>
    <body>
        <div id="box" class="pulse">
            <h2>Math Validator — Filters Diagnostic Panel</h2>
            <p>Wpisz wyrażenie matematyczne:</p>
            <input id="expr" placeholder="1/(x-1)">
            <button onclick="run()">Validate</button>

            <div id="filters"></div>
            <pre id="out">{ wynik pojawi się tutaj }</pre>
        </div>

        <script>
            function renderFilters(data) {
                let html = "";

                if (data.singularities) {
                    html += `<div class='filter-box'>
                                <div class='title'>Singularities</div>
                                Wykryto: <b>${data.singularities.length}</b><br>
                                ${JSON.stringify(data.singularities)}
                             </div>`;
                }

                if (data.twists !== undefined) {
                    html += `<div class='filter-box'>
                                <div class='title'>Twists (skręty topologiczne)</div>
                                Wartość: <b>${data.twists}</b><br>
                                Interpretacja: im większe, tym większa niestabilność struktury.
                             </div>`;
                }

                if (data["ρ_defects"] !== undefined) {
                    html += `<div class='filter-box'>
                                <div class='title'>ρ-defects (defekty gęstości)</div>
                                Wartość: <b>${data["ρ_defects"]}</b><br>
                                Defekty wskazują na lokalne zaburzenia w polu informacyjnym.
                             </div>`;
                }

                if (data.notes) {
                    html += `<div class='filter-box'>
                                <div class='title'>Notes (komentarze systemowe)</div>
                                ${data.notes.join("<br>")}
                             </div>`;
                }

                document.getElementById("filters").innerHTML = html;
            }

            async function run() {
                const expr = document.getElementById("expr").value;
                const res = await fetch("/validate?expr=" + encodeURIComponent(expr));
                const data = await res.json();

                document.getElementById("out").textContent = JSON.stringify(data, null, 2);
                renderFilters(data);
            }
        </script>
    </body>
    </html>
    """


@app.get("/validate")
def validate_expr(expr: str):
    return validate(expr)
