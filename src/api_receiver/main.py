

from fastapi import FastAPI, Body


app = FastAPI()


@app.post("/alert")
async def alert(body: dict):
    print("CHECK ALERT", body)

@app.post("/alert/huge")
async def alert(body: dict):
    print("CHECK HUGE ALERT", body)
