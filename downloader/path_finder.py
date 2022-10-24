def get_archive_name(url: str) -> str:
    return url.rstrip("/").split("/")[-1]


def get_clean_file_path_parts(url: str) -> list[str]:
    parts = url.split('/')
    return list(filter(lambda part: part not in [".", ".."], parts))


def get_directory_path_from_parts(parts: list[str]) -> list[str]:
    return parts[0:-1]
