import traceback


def generate_exception(e: Exception):
    tb = traceback.format_exc().splitlines()
    payload = {
        "detail": str(e),
        "exception": e.__class__.__name__,
        "traceback": tb,
    }
    return payload