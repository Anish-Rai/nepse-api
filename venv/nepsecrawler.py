import asyncio
import httpx
from nepse import Client
client = Client()
async def main():

    print(dir(client))
    data = await client.market_client.market_is_open()

    # Closes the session
    await client.close()

# Run the function
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
