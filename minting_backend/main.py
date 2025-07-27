from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os, random, httpx, time

app = FastAPI()

CARD_API_KEY = os.getenv("POKEMON_API_KEY")
GITHUB_API = "https://api.github.com"

# In-memory mint history store: { "username/repo": last_mint_timestamp }
mint_history = {}

MINT_COOLDOWN_SECONDS = 86400  # 24 hours


class MintRequest(BaseModel):
    username: str
    repo: str

@app.get("/")
def read_root():
    return {"message": "Pokémon Minting API is running!"}


@app.post("/mint-card")
async def mint_card(data: MintRequest):
    key = f"{data.username}/{data.repo}"
    now = time.time()

    # Check cooldown
    if key in mint_history and now - mint_history[key] < MINT_COOLDOWN_SECONDS:
        seconds_left = int(MINT_COOLDOWN_SECONDS - (now - mint_history[key]))
        raise HTTPException(
            status_code=429,
            detail=f"Mint cooldown active. Try again in {seconds_left} seconds."
        )

    req_timeout = httpx.Timeout(300.0)
    headers = {"X-Api-Key": CARD_API_KEY.strip()}

    async with httpx.AsyncClient(timeout=req_timeout) as client:
        # Get total card count
        print("Fetching total count from TCG API...")
        total_count_res = await client.get("https://api.pokemontcg.io/v2/cards?pageSize=1", headers=headers)
        print(f"Status code: {total_count_res.status_code}")
        print(f"Response text: {total_count_res.text}")
        if total_count_res.status_code != 200:
            raise HTTPException(status_code=502, detail="Failed to get total card count.")
        total_count = total_count_res.json()["totalCount"]

        # Randomly pick a card
        random_page = random.randint(1, total_count)
        card_res = await client.get(f"https://api.pokemontcg.io/v2/cards?pageSize=1&page={random_page}", headers=headers)
        card_res.raise_for_status()
        card_data = card_res.json()["data"][0]

    # Update mint history
    mint_history[key] = now

    return {
        "username": data.username,
        "repo": data.repo,
        "card": {
            "name": card_data["name"],
            "image": card_data["images"]["large"],
            "id": card_data["id"]
        }
    }
