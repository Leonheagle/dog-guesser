import asyncio
import json
from datetime import datetime
from websockets.asyncio.server import serve
import os


def save_score(username, score):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Enregistrement du score en cours...")
    SCORES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scores.txt")
    with open(SCORES_FILE, "a", encoding="utf-8") as f:
        f.write(f"Username: {username} | Score: {score}/10 | Timestamp: {timestamp}\n")


async def handler(ws):
    score = 0
    game_saved = False
    try:
        async for message in ws:
            data = json.loads(message)

            if data["type"] == "answer":
                if data["correct"]:
                    score += 1

                await ws.send(json.dumps({"type": "score","score": score}))

            elif data["type"] == "game_over":
                print("Fin de partie reçue pour le joueur :", data["username"])
                if not game_saved:
                    username = data["username"]
                    save_score(username, score)
                    game_saved = True

                await ws.send(json.dumps({"type": "game_saved","score": score}))

            elif data["type"] == "reset_score":
                score = 0
                game_saved = False
                await ws.send(json.dumps({"type": "score_reset","score": score}))

    except Exception as error:
        print(f"Erreur avec le client : {error}")

    finally:
        print("Un client s'est déconnecté")


async def main():
    async with serve(handler, "localhost", 8765):
        print("ws://localhost:8765")
        await asyncio.Future()

asyncio.run(main())