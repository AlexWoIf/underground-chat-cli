# Chat-cli

Проект реализует минимальный набор асинхронных методов для пользования текстовым чатом:
- чтение сообщений
- регистрация пользовател
- авторизация пользователя по имеющемуся токену
- отправка сообщения

## Подготовка к запуску

Скрипт разрабатывался на версии Python 3.10.
Установите зависимости командой:

```sh
pip install -r requirements.txt
```

Скрипт чтения сообщений требует такие обязательные параметры как адрес сервера и порт для чтения сообщений.
Скрипт для отправки сообщений дополнительно требует порт для отправки сообщений и текст сообщения.
Так же могут быть переданы расположение лог-файла, токен для авторизации при отправке сообщения, либо никнейм для регистрации нового пользователя.

Все параметры могут быть описаны в конфигурационном файле .env либо переданы в качестве аргументов командной строки.

Для получения справки наберите:

```bash
python <название скрипта> --help
```

Пример ответа для скрипта send_message.py приведен ниже:

```sh
usage: send_message.py [-h] [--host HOST] [--writing_port WRITING_PORT] [--logfile LOGFILE] [--token TOKEN]
                       [--nickname NICKNAME] -m M

options:
  -h, --help            show this help message and exit
  --host HOST, --HOST HOST
                        server address
  --writing_port WRITING_PORT, --WRITING_PORT WRITING_PORT
                        server port
  --logfile LOGFILE, --LOGFILE LOGFILE
                        log filepath
  --token TOKEN, --TOKEN TOKEN
                        user token
  --nickname NICKNAME
  -m M                  message text

Args that start with '--' can also be set in a config file (.env). Config file syntax allows: key=value, flag=true,
stuff=[a,b,c] (for details, see syntax at https://goo.gl/R74nmi). In general, command-line values override config file
values which override defaults.
```
