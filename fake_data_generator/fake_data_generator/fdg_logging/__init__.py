import json
import logging
import sys
from datetime import datetime
from logging.config import dictConfig

from fake_data_generator.config import settings
from fake_data_generator.fdg_logging.schemas import BaseLogSchema

LEVEL_TO_NAME = {
    logging.CRITICAL: "CRITICAL",
    logging.ERROR: "ERROR",
    logging.WARNING: "WARNING",
    logging.INFO: "INFO",
    logging.DEBUG: "DEBUG",
    logging.NOTSET: "TRACE",
}


class JSONLogFormatter(logging.Formatter):
    """
    Custom class-formatter for writing logs to json
    """

    def format(self, record: logging.LogRecord, *args, **kwargs) -> str:
        """
        Formatting LogRecord to json

        :param record: logging.LogRecord
        :return: json string
        """
        log_object: dict = self._format_log_object(record)
        return json.dumps(log_object, ensure_ascii=False)

    @staticmethod
    def _format_log_object(record: logging.LogRecord) -> dict:
        now = (
            datetime.
            fromtimestamp(record.created).
            astimezone().
            replace(microsecond=0).
            isoformat()
        )
        message = record.getMessage()
        duration = (
            record.duration
            if hasattr(record, "duration")
            else record.msecs
        )

        json_log_fields = BaseLogSchema(
            name=record.name,
            level_name=LEVEL_TO_NAME[record.levelno],
            module=record.module,
            func_name=record.funcName,
            filename=record.filename,
            pathname=record.pathname,
            timestamp=now,
            thread_id=record.thread,
            process_id=record.process,
            message=message,
            app_name=settings.PROJECT_NAME,
            app_version=settings.VERSION,
            app_env=settings.ENVIRONMENT,
            duration=duration
        )

        if record.exc_text:
            json_log_fields.exceptions = record.exc_text

        # Pydantic to dict
        json_log_object = json_log_fields.model_dump(
            exclude_unset=True,
            by_alias=True,
        )

        if hasattr(record, "request_json_fields"):
            json_log_object.update(record.request_json_fields)

        return json_log_object


def handlers(env,
             *,
             to_file: bool = False):
    if env.lower() in ("dev", "local"):
        handler = ["console"]
    else:
        handler = ["intercept"]

    if to_file:
        handler.append("file_handler")

    return handler


LOG_HANDLER = handlers(settings.ENVIRONMENT,
                       to_file=True)
LOGGING_LEVEL = logging.DEBUG if settings.DEBUG else logging.INFO

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
        "standard": {
            "format": "%(asctime)s - [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "json": {
            "()": JSONLogFormatter,
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
            "stream": sys.stdout,
        },
        "file_handler": {
            "level": "INFO",
            "filename": settings.LOG_FILENAME,
            "class": "logging.FileHandler",
            "formatter": "json"
        }
    },
    "loggers": {
        "root": {
            "handlers": LOG_HANDLER,
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn": {
            "handlers": LOG_HANDLER,
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": LOG_HANDLER,
            "level": "ERROR",
            "propagate": False,
        },
    },
}


def setup_logging():
    dictConfig(LOG_CONFIG)
