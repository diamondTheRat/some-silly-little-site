from fastapi import FastAPI, Cookie, Response, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from console_simulator import console
from data_types import *
from typing import Optional
from status import get_metrics
import security
from html_files import serve
from starlette.responses import RedirectResponse


app = FastAPI()

# Mount the static directory to serve CSS files
app.mount("/frontend", StaticFiles(directory="../frontend"), name="frontend")


@app.exception_handler(404)
async def custom_404_handler(response: Response, err: HTTPException):
    return serve("../frontend/notfound/index.html")

@app.get("/")
async def root(password: str = Cookie(None)):
    if not security.verify_password(password):
        return serve("../frontend/login/index.html")
    return RedirectResponse(url="/dashboard")

@app.get("/dashboard")
async def dashboard(password: str = Cookie(None)):
    if not security.verify_password(password):
        return RedirectResponse(url="/")
    return serve("../frontend/dashboard/index.html")

@app.get("/console")
async def open_console(password: str = Cookie(None)):
    if not security.verify_password(password):
        return serve("../frontend/login/index.html")
    return serve("../frontend/console/index.html")

@app.post("/verifylogin")
async def verify(data: LoginInfo, response: Response):
    response.status_code = 401 - 201 * security.verify_password(data.password)
    

@app.get("/console/output")
async def get_output(response: Response, password: str = Cookie(None)):
    if not security.verify_password(password):
        response.status_code = 404
        return 
    return await console.get_output()

@app.post("/console/run")
async def get_output(data: Command, response: Response, password: str = Cookie(None)):
    if not security.verify_password(password):
        response.status_code = 404
        return 
    await console.run(command=data.command)

@app.get("/status")
async def get_status():
    return get_metrics()

@app.websocket("/livestatus")
async def websocket_endpoint(websocket: WebSocket, password: str = Cookie(None)):
    if not security.verify_password:
        websocket.close()
        return
    await websocket.accept()
    try:
        while True:
            await websocket.receive_text()
            await websocket.send_json(get_metrics())
    except WebSocketDisconnect:
        pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
