from fastapi import FastAPI
import requests
import urllib3
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = FastAPI()

ESPN_API = "https://site.api.espn.com/apis/site/v2/sports/soccer/scoreboard"


@app.get("/")
def home():

    return {
        "status": "online",
        "message": "API de partidos funcionando"
    }


@app.get("/matches")
def get_matches():

    try:

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            ESPN_API,
            headers=headers,
            verify=False,
            timeout=10
        )

        data = response.json()

        events = data.get("events", [])

        matches = []

        for event in events:

            try:

                league = event["league"]["name"]

                competitors = event["competitions"][0]["competitors"]

                home = competitors[0]["team"]["displayName"]
                away = competitors[1]["team"]["displayName"]

                date_str = event["date"]

                dt = datetime.fromisoformat(
                    date_str.replace("Z", "+00:00")
                )

                hour = dt.strftime("%H:%M")

                matches.append({
                    "league": league,
                    "home": home,
                    "away": away,
                    "match": f"{home} vs {away}",
                    "hour": hour
                })

            except:
                pass

        return {
            "success": True,
            "total": len(matches),
            "matches": matches
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }
