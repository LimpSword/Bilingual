import asyncio
import json
import random

import requests
import websockets

# List to store connected players
players = []
players_name = {}
players_email = {}

basic_french_en = {
    "réunion": "meeting",
    "entretien": "interview",
    "lettre de motivation": "cover letter",
    "déchiffrer": "decipher",
    "salarié": "employee",
    "employeur": "employer",
    "déménagement": "relocation"
}


# Function to generate a random word
def generate_word(avoid: list):
    choice = random.choice(list(basic_french_en.keys()))
    while choice in avoid:
        choice = random.choice(list(basic_french_en.keys()))
    return choice


# Function to match players and start the game loop
async def match_players(websocket):
    global players
    async for msg in websocket:
        if msg.startswith("/name"):
            players_name[websocket] = msg.split(" ")[1]
            players_email[websocket] = msg.split(" ")[2]
            break
    print(players_name)
    if len(players) >= 1:
        print("Matched players")
        await asyncio.create_task(game_loop(players[len(players) - 1], websocket))
    else:
        players.append(websocket)
        await game_end()


async def game_end():
    while True:
        await asyncio.sleep(1)
        if len(players) == 0:
            break


# Game loop function
async def game_loop(player1, player2):
    print(player1, player2)
    response_count = {player1: 0, player2: 0}
    try:
        # Send hello message to both players and wait 3s
        await asyncio.gather(
            player1.send("/hello " + players_name[player2]),
            player2.send("/hello " + players_name[player1]),
            asyncio.sleep(4)
        )

        used_words = []

        for n in range(5):
            word = generate_word(used_words)
            used_words.append(word)
            websockets.broadcast({player2}, f"{word}")
            await player1.send(f"{word}")

            async def iter_messages(player, correct_answer):
                async for message in player:
                    print(message, correct_answer)
                    if message == correct_answer:
                        return player
                return None

            player1_response = None
            player2_response = None
            # Wait for responses with a timeout (succeed on first response)
            try:
                done, pending = await asyncio.wait(
                    [iter_messages(player, basic_french_en[word]) for player in [player1, player2]],
                    timeout=10,
                    return_when=asyncio.FIRST_COMPLETED)
            except asyncio.TimeoutError:
                # Time limit reached, no winner
                print("Time's up! No one answered correctly.")
            else:
                for task in done:
                    winning_player = task.result()
                    print(f"Player {winning_player} answered correctly!")
                    if winning_player == player1:
                        player1_response = basic_french_en[word]
                    if winning_player == player2:
                        player2_response = basic_french_en[word]

            # Cancel any remaining tasks
            for task in pending:
                task.cancel()

            print("---", word, "---")
            # Check if both players responded with the correct word
            if player1_response == basic_french_en[word]:
                result = 'success'
                response_count[player1] += 1
            else:
                result = 'failure'
            await player1.send(f"/result {result}")
            print("Player 1 response", player1_response, result)

            if player2_response == basic_french_en[word]:
                result = 'success'
                response_count[player2] += 1
            else:
                result = 'failure'
            await player2.send(f"/result {result}")
            print("Player 2 response", player2_response, result)
            print("------")

            await asyncio.sleep(1)

        has_player1_won = "win" if response_count[player1] > response_count[player2] else "lose"
        has_player2_won = "win" if response_count[player2] > response_count[player1] else "lose"

        if has_player1_won == "win":
            url = "https://8jrcgpn602.execute-api.eu-west-3.amazonaws.com/Prod/api/updateElo"
            payload = {
                "email": players_email[player1],
                "elo": 10
            }
            headers = {
                'Content-Type': 'application/json'
            }
            print(payload)
            response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
            print(response.text)
        elif has_player2_won == "win":
            url = "https://8jrcgpn602.execute-api.eu-west-3.amazonaws.com/Prod/api/updateElo"
            payload = {
                "email": players_email[player2],
                "elo": 10
            }
            headers = {
                'Content-Type': 'application/json'
            }
            print(payload)
            response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
            print(response.text)


        await asyncio.gather(
            player1.send('/end ' + has_player1_won),
            player2.send('/end ' + has_player2_won)
        )
    except websockets.exceptions.ConnectionClosedError:
        # Handle player disconnection
        print("Player disconnected")
    finally:
        # Close connections
        await asyncio.gather(
            player1.close(),
            player2.close()
        )
        global players
        players = [p for p in players if p not in [player1, player2]]


# WebSocket server handler
async def handler(websocket):
    print("Connected", websocket)
    await match_players(websocket)
    print("Disconnected", websocket)


async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Server started")
        await asyncio.Future()  # run forever


asyncio.run(main())
