import time
from pathlib import Path


def link_osc8(uri: str, label: str = None):
    if label is None:
        label = uri
    parameters = ''

    # OSC 8 ; params ; URI ST <name> OSC 8 ;; ST
    escape_mask = '\033]8;{};{}\033\\{}\033]8;;\033\\'

    return escape_mask.format(parameters, uri, label)


def link(path: str):
    return f"file://{path}"


def get_tmp_filepath(path: str, timestamp_suffix: bool = True):
    path = path.replace("\\", "/")

    file = f"/tmp/{path}"
    file2 = file

    if timestamp_suffix:
        filename = file.split("/")[-1]
        timestamp = time.strftime("%Y%m%d-%H%M%S")

        def _tmp_filepath_subroutine(_filename, _timestamp, _i=0):
            if _i > 0:
                _timestamp = f"{_timestamp}-{_i}"

            if "." in _filename:
                file1 = ".".join(file.split(".")[0:-1])
                file2 = file.split(".")[-1]
                return f"{file1}.{_timestamp}.{file2}"
            else:
                return f"{file}_{_timestamp}"

        file2 = _tmp_filepath_subroutine(filename, timestamp)

        i = 0
        while Path(file2).exists():
            i += 1
            file2 = _tmp_filepath_subroutine(filename, timestamp, i)


    Path(file2).parent.mkdir(parents=True, exist_ok=True)

    return file2



