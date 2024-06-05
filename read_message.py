import asyncio


async def read_msg():
    while True:
        reader, _ = await asyncio.open_connection('minechat.dvmn.org', 5000)
        received_msg = await reader.readline()
        print(received_msg.decode().strip())


if __name__ == '__main__':
    asyncio.run(read_msg())
