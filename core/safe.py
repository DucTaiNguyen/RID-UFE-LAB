from core.logger import log_error

def safe_run(fn):
    try:
        return fn()
    except Exception as e:
        log_error(e)
        print("ERROR:", str(e))
        return None
