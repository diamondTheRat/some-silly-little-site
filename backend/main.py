from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from console_simulator import console
from data_types import *


app = FastAPI()

# Mount the static directory to serve CSS files
app.mount("/frontend", StaticFiles(directory="../frontend"), name="frontend")
app.mount("/console/files", StaticFiles(directory="../frontend/console/"), name="console")


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("../frontend/index.html") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.get("/console")
async def open_console():
    with open("../frontend/console/index.html") as f:
        html_content = f.read()
    
    return HTMLResponse(content=html_content)

@app.get("/console/output")
async def get_output():
    return await console.get_output()

@app.post("/console/run")
async def get_output(data: Command):
    await console.run(command=data.command)
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
