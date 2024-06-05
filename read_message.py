import asyncio

import aiofiles

async def write_to_file(file_path, content):
    async with aiofiles.open(file_path, mode='a') as f:
        await f.write(content)

async def read_msg():
    while True:
        reader, _ = await asyncio.open_connection('minechat.dvmn.org', 5000)
        received_msg = await reader.readline()
        await write_to_file('chat.log', received_msg.decode())
        print(received_msg.decode().strip())


if __name__ == '__main__':
    asyncio.run(read_msg())
