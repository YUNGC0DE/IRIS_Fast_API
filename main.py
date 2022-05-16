import uvicorn
import joblib
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/healthcheck")
async def healthcheck():
    return {"message": "I'm alive"}


class Request(BaseModel):
    slength: float
    swidth: float
    plength: float
    pwidth: float


@app.post("/classify")
async def create_item(item: Request):
    data = [item.slength, item.swidth, item.plength, item.swidth]
    data = np.array(data).reshape(-1, 4)
    result = model.predict(data)

    result = classes[result[0]]
    return {"response": result}


if __name__ == "__main__":
    with open("models/classifier.pkl", 'rb') as file:  # test case in tests.py REVIEW
        model = joblib.load(file)

    classes = ['Setosa', 'versicolor', 'virginica']

    uvicorn.run(app, host="0.0.0.0", port=8080)