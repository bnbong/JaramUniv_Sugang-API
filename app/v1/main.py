import uvicorn

from app import create_app
from app.settings import Settings


app = create_app(settings=Settings)


@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9090)
