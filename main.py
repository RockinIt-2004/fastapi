from fastapi import FastAPI, Depends, HTTPException
import requests
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv
app = FastAPI()
load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

TOKEN_URL = "https://oauth.fatsecret.com/connect/token"

def get_access_token():
    response = requests.post(
        TOKEN_URL,
        data={"grant_type": "client_credentials"},
        auth=(CLIENT_ID, CLIENT_SECRET),
    )
    print(response.status_code, response.text) 
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to obtain access token")
    return response.json()["access_token"]

@app.get("/search-food/")
def search_food(query: str):
    access_token = get_access_token() 
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    params = {
        "method": "foods.search",
        "search_expression": query,
        "format": "json"
    }

    response = requests.get("https://platform.fatsecret.com/rest/server.api", params=params, headers=headers)
    
    print(response.status_code, response.text) 

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
