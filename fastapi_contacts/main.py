# fastapi_contacts/main.py
from fastapi import FastAPI
from fastapi_contacts.app.routes import router

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

