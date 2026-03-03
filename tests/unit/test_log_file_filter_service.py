from pathlib import Path
from log_file_filter_service import LogModel, LogFileFilterService


def test_parse_log_file_manager() -> None:
    # given
    expected_log_errors_data = [
        LogModel(
            service_name="glenn-spiro",
            timestamp="2026-02-28 18:54:17",
            level="ERROR",
            message="root: Error rendering template: 'dict object' has no attribute 'loan'",
            traceback_message=None,
        ),
        LogModel(
            service_name="glenn-spiro",
            timestamp="2026-02-28 18:54:17",
            level="ERROR",
            message="root: Precompile jinja for share_partners_by_category could not be generated! - An exception of type UndefinedError occurred on line 839: 'dict object' has no attribute 'loan'",
            traceback_message=[
                "Traceback (most recent call last):",
                'File "/home/fastapi-user/fastapi-nginx-gunicorn/backend/services/output/main.py", line 839, in output_html',
                "compiled_data_to_widget_json = await compile_jinja_and_save_in_database(request, client_name, token, session, output_doc_id, template_data, jinja_data_to_widget_output, precompile_jinja_type, precompile_document)",
                "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^",
                'File "/home/fastapi-user/fastapi-nginx-gunicorn/backend/functions/output_docs.py", line 266, in compile_jinja_and_save_in_database',
                "rendered_template = render_template(request_jinja, request_json)",
                "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^",
            ],
        ),
        LogModel(
            service_name="glenn-spiro",
            timestamp="2026-02-28 18:54:17",
            level="INFO",
            message='uvicorn.access:  - "POST /glenn-spiro/microservices/output/ HTTP/1.1" 500',
            traceback_message=None,
        ),
        LogModel(
            service_name="glenn-spiro",
            timestamp="2026-02-28 18:54:19",
            level="ERROR",
            message="root: Error rendering template: 'dict object' has no attribute 'loan'",
            traceback_message=None,
        ),
        LogModel(
            service_name="glenn-spiro",
            timestamp="2026-02-28 18:54:19",
            level="ERROR",
            message="root: Precompile jinja for share_partners_by_category could not be generated! - An exception of type UndefinedError occurred on line 839: 'dict object' has no attribute 'loan'",
            traceback_message=[
                "Traceback (most recent call last):",
                'File "/home/fastapi-user/fastapi-nginx-gunicorn/backend/services/output/main.py", line 839, in output_html',
                "compiled_data_to_widget_json = await compile_jinja_and_save_in_database(request, client_name, token, session, output_doc_id, template_data, jinja_data_to_widget_output, precompile_jinja_type, precompile_document)",
                "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^",
                'File "/home/fastapi-user/fastapi-nginx-gunicorn/backend/functions/output_docs.py", line 266, in compile_jinja_and_save_in_database',
                "rendered_template = render_template(request_jinja, request_json)",
                "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^",
            ],
        ),
        LogModel(
            service_name="glenn-spiro",
            timestamp="2026-02-28 18:54:19",
            level="INFO",
            message='uvicorn.access:  - "POST /glenn-spiro/microservices/output/ HTTP/1.1" 500',
            traceback_message=None,
        ),
    ]
    expected_dicts = [m.model_dump() for m in expected_log_errors_data]
    log_file_filter_service = LogFileFilterService()

    # when
    filtered_log_file_info = log_file_filter_service.filter_errors_by_service_name_and_by_date(
        local_log_file_path=str(Path().cwd() / "tests" / "unit" / "mock_log_file.log"),
        service_name="glenn-spiro",
        start_date_iso="2026-02-28 18:54:13",
        end_date_iso="2026-02-28 18:54:20",
    )
    # then
    assert filtered_log_file_info == expected_dicts
