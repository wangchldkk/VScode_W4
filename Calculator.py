import ast
import math
import re

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


class CalcRequest(BaseModel):
    expression: str


app = FastAPI(title="Modern Calculator", version="1.0.0")


def safe_eval_expression(expression: str) -> float:
    if not expression or not expression.strip():
        raise ValueError("Expression is required.")

    cleaned = expression.strip().replace("^", "**")
    if not re.fullmatch(r"[0-9+\-*/().%\s]+", cleaned):
        raise ValueError("Expression contains unsupported characters.")

    tree = ast.parse(cleaned, mode="eval")

    def evaluate(node):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return float(node.value)
            raise ValueError("Only numeric constants are allowed.")

        if isinstance(node, ast.BinOp):
            left = evaluate(node.left)
            right = evaluate(node.right)

            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                if right == 0:
                    raise ValueError("Division by zero is not allowed.")
                return left / right
            if isinstance(node.op, ast.Pow):
                return left**right
            if isinstance(node.op, ast.Mod):
                if right == 0:
                    raise ValueError("Modulo by zero is not allowed.")
                return left % right
            raise ValueError("Unsupported operator.")

        if isinstance(node, ast.UnaryOp):
            operand = evaluate(node.operand)
            if isinstance(node.op, ast.UAdd):
                return +operand
            if isinstance(node.op, ast.USub):
                return -operand
            raise ValueError("Unsupported unary operation.")

        raise ValueError("Unsupported expression structure.")

    result = evaluate(tree.body)
    if not math.isfinite(result):
        raise ValueError("Result is not finite.")
    return result


@app.get("/")
async def serve_index():
    return FileResponse("static/index.html")


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/api/calc")
async def api_calc_get(expression: str):
    try:
        result = safe_eval_expression(expression)
        return {"expression": expression, "result": result}
    except Exception as exc:  # pragma: no cover - API validation path
        return {"expression": expression, "result": None, "error": str(exc)}


@app.post("/api/calc")
async def api_calc_post(payload: CalcRequest):
    try:
        result = safe_eval_expression(payload.expression)
        return {"expression": payload.expression, "result": result}
    except Exception as exc:  # pragma: no cover - API validation path
        return {"expression": payload.expression, "result": None, "error": str(exc)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("Calculator:app", host="127.0.0.1", port=8000, reload=False)
