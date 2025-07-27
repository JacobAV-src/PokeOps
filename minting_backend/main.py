from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os, random, httpx, time, asyncio
from functools import lru_cache

app = FastAPI()

CARD_API_KEY = os.getenv("POKEMON_API_KEY")
GITHUB_API = "https://api.github.com"

# In-memory mint history store: { "username/repo": last_mint_timestamp }
mint_history = {}

class MintRequest(BaseModel):
    username: str
    repo: str

MINT_COOLDOWN_SECONDS = 86400  # 24 hours
fallback_total = 19500
DISABLE_COOLDOWN = True

_cached_count = {"value": fallback_total, "last_updated": 0}
_cache_duration = 3600


async def get_total_card_count(client, headers):
    now = time.time()
    if now - _cached_count["last_updated"] < _cache_duration:
        return _cached_count["value"]
    try:
        res = await client.get("https://api.pokemontcg.io/v2/cards?pageSize=1", headers=headers)
        res.raise_for_status()
        total = res.json()["totalCount"]
        _cached_count.update({"value": total, "last_updated": now})
        return total
    except Exception:
        return fallback_total

@app.get("/")
def read_root():
    return {"message": "Pokémon Minting API is running!"}


@app.post("/mint-card")
async def mint_card(data: MintRequest):
    try:
        key = f"{data.username}/{data.repo}"
        now = time.time()

        # Check cooldown
        if not DISABLE_COOLDOWN:
            if key in mint_history and now - mint_history[key] < MINT_COOLDOWN_SECONDS:
                seconds_left = int(MINT_COOLDOWN_SECONDS - (now - mint_history[key]))
                raise HTTPException(
                    status_code=429,
                    detail=f"Mint cooldown active. Try again in {seconds_left} seconds."
                )

        req_timeout = httpx.Timeout(300.0)
        headers = {"X-Api-Key": CARD_API_KEY.strip()}

        async with httpx.AsyncClient(timeout=req_timeout) as client:
            print("Fetching total count from TCG API...")
            total_count = await get_total_card_count(client, headers)
            
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
    except Exception as e:
        print(f"Something went wrong while minting card : {e}")
        raise HTTPException(status_code=500, detail="Failed to mint card.")
