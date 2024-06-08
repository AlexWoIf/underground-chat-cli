import asyncio
import logging
import socket

import configargparse

HELLO_STRING = 'Hello %username%! Enter your personal hash or leave it empty to create new account.'
WELCOME_STRING = 'Welcome to chat! Post your message below. End it with an empty line.'


def import_config():
    parser = configargparse.ArgParser(default_config_files=['.env', ])
    parser.add('--host', '--HOST', help='server address')
    parser.add('--writing_port', '--WRITING_PORT', help='server port')
    parser.add('--logfile', '--LOGFILE', help='log filepath')
    parser.add('--token', '--TOKEN', help='user token')
    parser.add('-m', help='message text')

    args, _ = parser.parse_known_args()
    print(args)

    return vars(args)


async def authorise(reader, writer, token):
    writer.write(f'{token}\n'.encode())
    await writer.drain()
    answer = await reader.readline()
    answer = await reader.readline()
    return answer


async def send_msg(config):
    host, port, _, token, message = config.values()
    reader, writer = await asyncio.open_connection(host, port)
    received_msg = await reader.readline()
    decoded_msg = received_msg.decode().strip()
    print(decoded_msg)
    logging.debug(decoded_msg)

    if decoded_msg == HELLO_STRING:
        received_msg = await authorise(reader, writer, token)
        decoded_msg = received_msg.decode().strip()
        print(decoded_msg)
        logging.debug(decoded_msg)

    if decoded_msg == WELCOME_STRING:
        print(f'Send "{message}"')
        writer.write(f'{message}\n\n'.encode())
        await writer.drain()


async def main():
    config = import_config()
    logging.basicConfig(
        format='%(levelname)s:%(filename)s:[%(asctime)s] %(message)s',
                level=logging.DEBUG,
                filename=config.get('logfile', f'{__name__}.log'),
    )
    # messages = ['Hello,', 'world']
    # for message in messages:
    retry = 0
    try:
        await send_msg(config)
    except socket.gaierror as exc:
        print(f'Sleeping {retry}sec(s)')
        asyncio.sleep(retry)
        retry = (retry + 1) * 2


if __name__ == '__main__':
    asyncio.run(main())