import asyncio
import datetime
import socket

import aiofiles


async def write_to_file(file_path, content):
    async with aiofiles.open(file_path, mode='a') as f:
        await f.write(content)

async def read_msg():
    retry = 0
    while True:
        try:
            reader, _ = await asyncio.open_connection('minechat.dvmn.org', 5000)
            received_msg = await reader.readline()
            timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M]")
            await write_to_file('chat.log', f'{timestamp}\t{received_msg.decode()}')
            print(received_msg.decode().strip())
            retry = 0
        except socket.gaierror as exc:
            print(f'Sleeping {retry}sec(s)')
            await asyncio.sleep(retry)
            retry = (retry + 1) * 2


if __name__ == '__main__':
    asyncio.run(read_msg())
