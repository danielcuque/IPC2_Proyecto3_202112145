

ALLOWED_EXTENSIONS = set(['txt', 'xml', 'json'])


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def read_info(file: bytes) -> str:
    pass
