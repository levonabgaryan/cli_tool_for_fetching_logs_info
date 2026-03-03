from pathlib import Path
import tempfile


from fabric import Connection


class RemoteFileManager:
    def __init__(
        self,
        connection_host: str,
        connection_port: int,
        connection_user_name: str,
        connection_user_password: str,
        ssh_key_path: str,
    ) -> None:
        self.__connection_host = connection_host
        self.__connection_user_name = connection_user_name
        self.__connection_user_password = connection_user_password
        self.__connection_port = connection_port
        self.__ssh_key_path = ssh_key_path

    def __get_connection(self) -> Connection:  # type: ignore[no-any-unimported]
        connect_kwargs = {"key_filename": self.__ssh_key_path}
        return Connection(
            host=self.__connection_host,
            port=self.__connection_port,
            user=self.__connection_user_name,
            connect_kwargs=connect_kwargs,
        )

    def download_file_from_server_and_return_path(
        self,
        remote_path: str,
    ) -> str:
        log_dir = Path.cwd() / "log_files"
        log_dir.mkdir(exist_ok=True)

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".log", dir=str(log_dir))
        local_path = temp_file.name
        temp_file.close()
        with self.__get_connection() as connection:
            connection.get(remote_path, local_path)

        return local_path

    @staticmethod
    def delete_local_file(file_path: str) -> None:
        path_ = Path(file_path)
        path_.unlink(missing_ok=True)
