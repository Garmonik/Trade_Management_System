# Установка зависимостей и настроек для проекта

Для начала обновить систему:

```commandline
sudo apt update
```

В папке Trade_Management_System поставь виртуальное окружение:

```commandline
sudo apt install -y python3-venv
python3 -m venv venv
source venv/bin/activate
```

Далее поставим на него все библиотеки:

```commandline
pip install -r requirements.txt
```

Далее в папке где лежит manage.py (Trade_Management_System/app/):

```commandline
python3 manage.py migrate
```

Это нужно для применения миграций к базе данных

Если вдруг что-то добавляешь в моделях, то необходимо использовать следующие команды:

```commandline
python3 manage.py malemigrations
python3 manage.py migrate
```

Это нужно для создания и применения миграций к базе данных.

Далее нужно создать суперюзера (чтобы мог в админку лазить):

```commandline
python3 manage.py createsuperuser
```

Там нужно будет ввести почту, логин и пароль (можно рандомные)

Ну и чтобы запустить сервер нужно:

```commandline
python3 manage.py runserver
```

Должно появится что-то тип такого:

```commandline
Run 'python manage.py migrate' to apply them.
August 21, 2023 - 10:08:13
Django version 4.2.4, using settings 'Trade_Management_System.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

# Swagger

Чтобы посмотреть Swagger запусти сервер и в браузере пройди по этому урлу: http://127.0.0.1:8000/api/schema/swagger-ui/#/

# Альтернативный запуск

### Шаг 1: Установка Docker

Первым делом вам нужно установить Docker на сервер. Процесс установки может немного отличаться в зависимости от используемой операционной системы. Ниже приведен пример установки Docker на Ubuntu:

```bash
# Обновите индекс пакетов и установите необходимые пакеты для использования репозитория over HTTPS:
sudo apt-get update
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common

# Добавьте официальный ключ GPG Docker:
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Добавьте репозиторий Docker в список источников APT:
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

# Обновите индекс пакетов и установите Docker Engine:
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

### Шаг 2: Установка Docker Compose

После установки Docker вам нужно установить Docker Compose. Вот как это можно сделать:

```bash
# Загрузите текущую стабильную версию Docker Compose:
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Сделайте исполняемым бинарный файл:
sudo chmod +x /usr/local/bin/docker-compose

# Проверьте установку:
docker-compose --version
```

### Шаг 3: Запуск вашего Django проекта

Теперь, когда Docker и Docker Compose установлены, вы можете запустить ваш Django проект. Для этого:

1. Загрузите исходный код вашего проекта на сервер. Это можно сделать разными способами, например, через `git clone`, если ваш код находится в репозитории Git, или через `scp` для копирования файлов напрямую.

2. Перейдите в директорию вашего проекта, где находятся `Dockerfile` и `docker-compose.yml`.

3. Запустите ваш проект с помощью Docker Compose:

```bash
docker-compose up --build
```