import asyncio
import logging
import socket

import configargparse


def import_config():
    parser = configargparse.ArgParser(default_config_files=['.env', ])
    parser.add('--host', '--HOST', help='server address')
    parser.add('--reading_port', '--READING_PORT', help='server port')
    parser.add('--logfile', '--LOGFILE', help='log filepath')

    args, _ = parser.parse_known_args()
    print(args)

    return vars(args)


async def read_message(config):
    host, port, _ = config.values()
    reader, _ = await asyncio.open_connection(host, port)
    received_msg = await reader.readline()
    decoded_msg = received_msg.decode().strip()
    logging.debug(decoded_msg)
    print(decoded_msg)


async def read_persistent_message(config):
    retry = 0
    while True:
        try:
            await read_message(config)
            retry = 0
        except socket.gaierror as exc:
            print(f'Sleeping {retry}sec(s)')
            await asyncio.sleep(retry)
            retry = (retry + 1) * 2


def main():
    config = import_config()
    logging.basicConfig(
        format='%(levelname)s:%(filename)s:[%(asctime)s] %(message)s',
                level=logging.DEBUG,
                filename=config.get('logfile', f'{__name__}.log'),
    )

    asyncio.run(read_persistent_message(config))


if __name__ == '__main__':
    main()
