from weed_game import WeedGame
import asyncio

async def main():
    game = WeedGame()
    game.main_loop()
    await asyncio.sleep(0)
    
asyncio.run(main())