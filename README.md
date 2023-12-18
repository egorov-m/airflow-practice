# airflow-practice

Практическая часть роботы по доп. заданию по предмету "Базы и хранилища данных" — демнстрация практического использования инструмента Apache Airflow.

### Шаги выполнения примера

**Необходимые инструменты:**

- git;
- Docker;
- Docker Compose;
- Python;
- pip/poetry;

#### 1. Клонирование репозитория:

```shell
git clone https://github.com/egorov-m/airflow-practice.git
```

#### 2. Подготовка окружения:

```shell
cd ./airflow-practice/ && \
    mkdir -p ./dags ./logs ./plugins ./config && \
    echo -e "AIRFLOW_UID=$(id -u)" > .env
```

Прописываем данные почты для отправки писем в environment в [docker-compose.yaml](./docker-compose.yaml).

```yaml
AIRFLOW__SMTP__SMTP_HOST: smtp.example.com
AIRFLOW__SMTP__SMTP_USER: user@example.com
AIRFLOW__SMTP__SMTP_PASSWORD: password
AIRFLOW__SMTP__SMTP_PORT: 465
AIRFLOW__SMTP__SMTP_MAIL_FROM: user@example.com
AIRFLOW__SMTP__SMTP_SSL: True
AIRFLOW__SMTP__SMTP_STARTTLS: False
```

#### 3. Запуск и инициализация контейнеров

**Инициализируем базу данных и запускаем контейнеры для Airflow:**
```shell
docker compose up airflow-init
docker ps -a  # посмотреть запущенные контейнеры
```

**Создаём базу данных для фейковых данных:**
```shell
docker exec -it airflow-practice-postgres-1 bash
psql -U airflow -c "create database fake_db;"
exit
```

**Запуск Airflow:**
```shell
docker compose up -d
```

#### 4. Инициализация и запуск генератора фейковых данных:

**Инициализируем окружение Python и устанавливаем зависимости:**
```shell
cd ./fake_data_generator/ && poetry install
```

**Запускаем инициализацию фейковых данных:**

```shell
poetry run python -m fake_data_generator init
```

**Запуск генерации фейковых данных**

*(создаёт случайные записи в БД - имитация работы реального backend’а - временной интервал 1 минута, для удобства демонстрации):*

```shell
poetry run python -m fake_data_generator startup
```

#### 5. Настройка и запуск процессов:
```shell
docker exec -it airflow-practice-airflow-worker-1 bash
```

**Создания Connection для подключения к базе данных fake_db:**

```shell
airflow connections add fake_db_connection --conn-uri postgresql://airflow:airflow@postgres/fake_db
```

**Создание переменных для почты на которую будут отправляться уведомления, токен telegram бота, id чата бота:**

```shell
airflow variables set email_to user@example.com
airflow variables set telegram_bot_token token
airflow variables set telegram_bot_from_chat_id 000000000
```

**Etl_dag находится на паузе, запускаем его:**

```shell
airflow dags unpause etl_dag
```

*эти же самые действия можно выполнять через web интерфейс или API;*

#### 6. Наблюдаем процесс в интерфейсе:

*В telegram bot’е и почтовом клиенте можно увидеть приходящее уведомления о процессе выполнения задач. В терминале запущен генератор фейковых данных, по логу видно, что он с интервалом в минуту выполняет модификацию данных, имитируя работу backend’а. В web интерфейсе Apache Airflow, на timelin’е видны запускаемые задачи Dag’а, наборы задач запускаются автоматически планировщиком по заданному расписанию: каждую минуту, порядок выполнения задач можно увидеть на графе.*
