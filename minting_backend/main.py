from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import random
import httpx

app = FastAPI()

class MintRequest(BaseModel):
    username: str
    repo: str

@app.post("/mint-card")
async def mint_card(data: MintRequest):
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get("https://api.pokemontcg.io/v2/cards?pageSize=1&page=random")
            card_data = res.json()["data"][0]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Card API failed")

    return {
        "username": data.username,
        "repo": data.repo,
        "card": {
            "name": card_data["name"],
            "image": card_data["images"]["large"],
            "id": card_data["id"]
        }
    }
