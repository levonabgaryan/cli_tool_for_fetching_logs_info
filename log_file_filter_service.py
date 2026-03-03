import re
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class LogModel(BaseModel):
    service_name: str
    timestamp: str
    level: str
    message: str
    traceback_message: list[str] | None = Field(default=None)


class LogFileFilterService:
    @staticmethod
    def filter_errors_by_service_name_and_by_date(
        service_name: str, start_date_iso: str, end_date_iso: str, local_log_file_path: str
    ) -> list[dict[str, Any]]:
        start_dt = datetime.fromisoformat(start_date_iso)
        end_dt = datetime.fromisoformat(end_date_iso)

        # Example line: 2026-02-28 18:54:13 [ERROR] Internal Server Error at /glenn-spiro/...
        log_pattern = re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(\w+)\] (.*)")
        target_service_url = f"{service_name}/microservices/output/"
        any_service_url_pattern = re.compile(r"/([^/]+)/microservices/output/")

        found_errors: list[LogModel] = []
        is_collecting_for_service = False

        with open(local_log_file_path, mode="r") as log_file:
            for line in log_file:
                clean_line = line.strip()
                if not clean_line:
                    continue

                match = log_pattern.search(clean_line)
                if match:
                    time_stamp_str, level, msg = match.groups()
                    current_date = datetime.strptime(time_stamp_str, "%Y-%m-%d %H:%M:%S")

                    current_log_model: LogModel | None = None
                    is_collecting_for_service = False

                    if not (start_dt <= current_date <= end_dt):
                        continue

                    # Condition for finding target service request info in log
                    if target_service_url in clean_line:
                        is_target_client_log = True
                    elif (
                        any_service_url_pattern.search(clean_line)
                        and target_service_url not in clean_line
                    ):
                        is_target_client_log = False

                    if is_target_client_log:
                        current_log_model = LogModel(
                            service_name=service_name,
                            timestamp=time_stamp_str,
                            level=level,
                            message=msg,
                        )
                        if current_log_model.level == "ERROR" or "500" in msg:
                            is_collecting_for_service = True
                            found_errors.append(current_log_model)

                # If the line is not a new log entry, it's considered part of the previous log's traceback
                elif current_log_model is not None and is_collecting_for_service:
                    if current_log_model.traceback_message:
                        current_log_model.traceback_message.append(clean_line)
                    else:
                        current_log_model.traceback_message = [clean_line]

        found_errors_to_list_of_dicts = list(map(LogModel.model_dump, found_errors))
        return found_errors_to_list_of_dicts
