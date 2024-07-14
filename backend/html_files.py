from fastapi.responses import HTMLResponse


def serve(path: str) -> str:
    with open(path) as f:
        return HTMLResponse(content=f.read())