import asyncio
import random
import string
import websockets

# List to store connected players
players = []

basic_french_en = {
    "réunion": "meeting",
    "entretien": "interview",
    "lettre de motivation": "cover letter"
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
    try:
        # Send hello message to both players and wait 3s
        await asyncio.gather(
            player1.send("/hello"),
            player2.send("/hello"),
            asyncio.sleep(4)
        )

        used_words = []

        for n in range(5):
            word = generate_word(used_words)
            used_words.append(word)
            websockets.broadcast({player2}, f"{word}")
            await player1.send(f"{word}")

            # Wait for responses with a timeout (succeed on first response)
            done, pending = await asyncio.wait(
                [player1.recv(), player2.recv()],
                return_when=asyncio.FIRST_COMPLETED,
                timeout=15.0
            )

            # Get the responses that were received
            player1_response = player2_response = None
            for future in done:
                if future.exception() is not None:
                    print(future.exception())
                    continue
                response = future.result()
                if response is not None:
                    if future.get_coro() == player1.recv:
                        player1_response = response
                    else:
                        player2_response = response

            print("---", word, "---")
            # Check if both players responded with the correct word
            if player1_response == basic_french_en[word]:
                result = 'success'
            else:
                result = 'failure'
            await player1.send(f"/result {result}")
            print("Player 1 response", player1_response, result)

            if player2_response == basic_french_en[word]:
                result = 'success'
            else:
                result = 'failure'
            await player2.send(f"/result {result}")
            print("Player 2 response", player2_response, result)
            print("------")

            # Cancel recv
            for task in pending:
                task.cancel()
            await asyncio.sleep(1)
        await asyncio.gather(
            player1.send('/end'),
            player2.send('/end')
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
