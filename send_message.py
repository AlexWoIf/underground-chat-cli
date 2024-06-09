import asyncio
import logging
import socket

import configargparse
import json

HELLO_PROMPT = 'Hello %username%! Enter your personal hash or leave it empty to create new account.'
WELCOME_PROMPT = 'Welcome to chat! Post your message below. End it with an empty line.'
REGISTER_PROMPT = 'Enter preferred nickname below:'


def import_config():
    parser = configargparse.ArgParser(default_config_files=['.env', ])
    parser.add('--host', '--HOST', help='server address')
    parser.add('--writing_port', '--WRITING_PORT', help='server port')
    parser.add('--logfile', '--LOGFILE', help='log filepath')
    parser.add('--token', '--TOKEN', help='user token')
    parser.add('--nickname')
    parser.add('-m', help='message text')

    args, _ = parser.parse_known_args()

    return vars(args)


async def register_user(config):
    host, port, _, _, nickname, _ = config.values()
    reader, writer = await asyncio.open_connection(host, port)
    received_msg = await reader.readline()
    decoded_msg = received_msg.decode().strip()
    logging.debug(decoded_msg)

    if decoded_msg != HELLO_PROMPT:
        raise RuntimeError

    writer.write(f'\n'.encode())
    await writer.drain()

    received_msg = await reader.readline()
    decoded_msg = received_msg.decode().strip()
    logging.debug(decoded_msg)

    if decoded_msg != REGISTER_PROMPT:
        raise RuntimeError
    
    writer.write(f'{nickname}\n'.encode())
    await writer.drain()

    received_msg = await reader.readline()
    decoded_msg = received_msg.decode().strip()
    logging.info(decoded_msg)


async def authorise(reader, writer, token):
    writer.write(f'{token}\n'.encode())
    await writer.drain()
    answer = await reader.readline()
    decoded_answer = answer.decode().strip()
    logging.debug(decoded_answer)
    if decoded_answer == 'null':
        raise ValueError
    nickname = json.loads(decoded_answer).get('nickname')
    return nickname


async def send_msg(config):
    host, port, _, token, _, message = config.values()
    reader, writer = await asyncio.open_connection(host, port)
    received_msg = await reader.readline()
    decoded_msg = received_msg.decode().strip()
    logging.debug(decoded_msg)

    if decoded_msg != HELLO_PROMPT:
        raise RuntimeError

    nickname = await authorise(reader, writer, token)
    received_msg = await reader.readline()
    decoded_msg = received_msg.decode().strip()
    logging.debug(decoded_msg)

    if decoded_msg != WELCOME_PROMPT:
        raise RuntimeError

    logging.debug(f'Send message from {nickname}:"{message}"')
    writer.write(f'{message}\n\n'.encode())
    await writer.drain()


async def main():
    config = import_config()
    print(config)
    logging.basicConfig(
        format='%(levelname)s:%(filename)s:[%(asctime)s] %(message)s',
                level=logging.DEBUG,
                filename=config.get('logfile', f'{__name__}.log'),
    )

    if config.get('nickname') is not None:
        await register_user(config)
    retry = 0
    try:
        if config.get('m') is not None:
            await send_msg(config)
    except socket.gaierror as exc:
        print(f'Sleeping {retry}sec(s)')
        asyncio.sleep(retry)
        retry = (retry + 1) * 2
    except ValueError:
        logging.error('Неизвестный токен')
        print('Неизвестный токен. Проверьте его или зарегистрируйте заново.')


if __name__ == '__main__':
    asyncio.run(main())