import asyncio

async def wait_loop():
    while True:
        for i in range(1, 4):
            print("wait" + "." * i)
            await asyncio.sleep(1)  # Wait for 1 second

# Run the async function
asyncio.run(wait_loop())