from fastapi import FastAPI
import requests
import urllib3
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = FastAPI()


@app.get("/")
def home():

    return {
        "status": "online"
    }


@app.get("/matches")
def get_matches():

    try:

        today = datetime.utcnow().strftime("%Y%m%d")

        espn_url = (
            f"https://site.api.espn.com/apis/site/v2/"
            f"sports/soccer/all/scoreboard?dates={today}"
        )

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            espn_url,
            headers=headers,
            verify=False,
            timeout=15
        )

        data = response.json()

        events = data.get("events", [])

        matches = []

        for event in events:

            try:

                competitors = event["competitions"][0]["competitors"]

                home = competitors[0]["team"]["displayName"]
                away = competitors[1]["team"]["displayName"]

                league = event["competitions"][0]["league"]["name"]

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
