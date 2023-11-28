from typing import Optional

from pydantic import Field

from fake_data_generator.common.schemas import BaseSchema


class BaseLogSchema(BaseSchema):
    name: str                                               # Name of the logger (logging channel)
    level_name: str                                         # Text logging level for the message ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")

    module: str                                             # Module (name portion of filename)
    func_name: str                                          # Function name
    filename: str                                           # Filename portion of pathname
    pathname: Optional[str]                                 # Full pathname of the source file where the logging call was issued (if available)

    timestamp: str = Field(..., alias='@timestamp')  # Logging time
    thread_id: Optional[int] = None                         # Thread ID (if available)
    process_id: Optional[int] = None                        # Process ID (if available)

    message: str                                            # The result of record.getMessage(), computed just as the record is emitted

    app_name: str                                           # Application name
    app_version: str                                        # Application version
    app_env: str                                            # Application environment ("DEV", "LOCAL", "PROD")
    duration: int                                           # Duration

    exceptions: Optional[list[str] | str] = None            # Exception text

    class Config:
        populate_by_name = True
