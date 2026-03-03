from typing import Annotated

import typer
from log_file_filter_service import LogFileFilterService
from remote_file_manager import RemoteFileManager

cli_app = typer.Typer(help="CLI tool for downloading log file and filtering")

ISO_FORMAT_HELP = "Format: YYYY-MM-DD HH:MM:SS (e.g. 2026-02-28 18:00:00)"


def get_logfile_from_remote_server_and_filter_by_date_by_service_name(
    remote_log_file_path: str,
    service_name: str,
    start_date_iso: str,
    end_date_iso: str,
    remote_file_manager: RemoteFileManager,
    log_file_filter_service: LogFileFilterService,
) -> None:
    local_log_file_path = remote_file_manager.download_file_from_server_and_return_path(
        remote_path=remote_log_file_path
    )
    filtered_logs = log_file_filter_service.filter_errors_by_service_name_and_by_date(
        service_name=service_name,
        start_date_iso=start_date_iso,
        end_date_iso=end_date_iso,
        local_log_file_path=local_log_file_path,
    )
    typer.echo(filtered_logs)
    remote_file_manager.delete_local_file(local_log_file_path)


@cli_app.command()
def fetch_log_errors_by_date_by_service_name(
    service_name: Annotated[str, typer.Option(help="Service name for filtering")],
    remote_log_file_path: Annotated[str, typer.Option(help="Remote log file path for downloading")],
    start_date_iso: Annotated[str, typer.Option(help=f"Start date in ISO. {ISO_FORMAT_HELP}")],
    end_date_iso: Annotated[str, typer.Option(help="End date in ISO. {ISO_FORMAT_HELP}")],
    host: Annotated[str, typer.Option(help="Server host")],
    port: Annotated[int, typer.Option(help="Server port")],
    server_user_name: Annotated[str, typer.Option(help="Server's user name")],
    server_user_password: Annotated[str, typer.Option(help="Server's user password")],
    ssh_key_path: Annotated[str, typer.Option(help="SSH key")],
) -> None:
    remote_file_manager = RemoteFileManager(
        connection_host=host,
        connection_user_name=server_user_name,
        connection_port=port,
        connection_user_password=server_user_password,
        ssh_key_path=ssh_key_path,
    )
    log_file_filter_service = LogFileFilterService()
    get_logfile_from_remote_server_and_filter_by_date_by_service_name(
        service_name=service_name,
        remote_log_file_path=remote_log_file_path,
        start_date_iso=start_date_iso,
        end_date_iso=end_date_iso,
        remote_file_manager=remote_file_manager,
        log_file_filter_service=log_file_filter_service,
    )


if __name__ == "__main__":
    cli_app()
