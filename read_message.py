import asyncio
import datetime
import configargparse
import socket

import aiofiles


def import_config():
    parser = configargparse.ArgParser(default_config_files=['.env', ])
    parser.add('--host', '--HOST', help='server address')
    parser.add('--reading_port', '--READING_PORT', help='server port')
    parser.add('--logfile', '--LOGFILE', help='log filepath')

    args, _ = parser.parse_known_args()
    print(args)

    return vars(args)


async def write_to_file(file_path, content):
    async with aiofiles.open(file_path, mode='a') as f:
        await f.write(content)

async def read_msg(config):
    host, port, log_filepath = config.values()
    retry = 0
    while True:
        try:
            reader, _ = await asyncio.open_connection(host, port)
            received_msg = await reader.readline()
            timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M]")
            await write_to_file(log_filepath,
                                f'{timestamp}\t{received_msg.decode()}')
            print(received_msg.decode().strip())
            retry = 0
        except socket.gaierror as exc:
            print(f'Sleeping {retry}sec(s)')
            await asyncio.sleep(retry)
            retry = (retry + 1) * 2


if __name__ == '__main__':
    config = import_config()
    asyncio.run(read_msg(config))
