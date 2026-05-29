from fastapi import FastAPI
import random
from latex_report import generate_latex

app = FastAPI()

@app.post("/run-research")
def run_research():

    data = {
        "trend": random.uniform(-1, 1),
        "noise": random.uniform(0, 1),
        "signal": random.uniform(0, 1)
    }

    score = data["signal"] - data["noise"]

    result = {
        "score": score,
        "hypothesis": "Emergent structure detected" if score > 0 else "System unstable"
    }

    tex_file = generate_latex(result)

    return {
        "result": result,
        "latex_file": tex_file
    }
