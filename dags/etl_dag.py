from datetime import timedelta, datetime

from airflow import DAG
from airflow.models import Variable
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.telegram.operators.telegram import TelegramOperator
from airflow.utils.context import Context
from airflow.utils.email import send_email


dag_args = {
    "owner": "airflow",
    "retries": 0,
    "retry_delay": timedelta(minutes=1)
}


def get_html_message(status, context):
    return f"""<ul>
                   <li><b>Status:</b> {status}</li>
                   <li><b>Execution date:</b> {context["data_interval_start"]}</li>
                   <li><b>Next execution date:</b> {context["data_interval_end"]}</li>
            </ul>"""


def get_telegram_message(status, subject, context):
    return \
        (f"<b>{subject}</b>\n"
         f"- <b>Status:</b> {status}\n"
         f"- <b>Execution date:</b> {context['data_interval_start']}\n"
         f"- <b>Next execution date:</b> {context['data_interval_end']}")


def get_subject(status):
    return f"Etl Dag notification: {status}"


def email_callback(context: Context, status: str):
    send_email(
        Variable.get("email_to"),
        get_subject(status),
        get_html_message(status, context)
    )


def telegram_bot_callback(context: Context, status: str):
    TelegramOperator(
        task_id="telegram_notification",
        token=Variable.get("telegram_bot_token"),
        chat_id=Variable.get("telegram_bot_from_chat_id"),
        text=get_telegram_message(status, get_subject(status), context)
    ).execute(context)


def on_success_email_callback(context: Context):
    email_callback(context, "success")


def on_success_telegram_bot_callback(context: Context):
    telegram_bot_callback(context, "success")


def on_failure_email_callback(context: Context):
    email_callback(context, "failure")


def on_failure_telegram_bot_callback(context: Context):
    telegram_bot_callback(context, "failure")


with DAG(
    dag_id="etl_dag",
    schedule_interval="* * * * *",
    start_date=datetime(2023, 12, 12),
    catchup=False,
    default_args=dag_args,
    description="Dag running etl process",
    on_success_callback=[on_success_email_callback, on_success_telegram_bot_callback],
    on_failure_callback=[on_failure_email_callback, on_failure_telegram_bot_callback]
) as etl_dag:
    conn_id = "fake_db_connection"

    analytical_table_creation = SQLExecuteQueryOperator(
        task_id="analytical_table_creation",
        sql="/sql/creation_tables.sql",
        conn_id=conn_id
    )

    etl_procedure_creation = SQLExecuteQueryOperator(
        task_id="etl_procedure_creation",
        sql="/sql/create_etl_procedure.sql",
        conn_id=conn_id
    )

    etl_process = SQLExecuteQueryOperator(
        task_id="etl_process",
        sql="/sql/etl_process.sql",
        conn_id=conn_id
    )

    analytical_table_creation >> etl_procedure_creation >> etl_process
