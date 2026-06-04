import traceback
from datetime import datetime

def log_error(e):
    with open("logs/error.log", "a") as f:
        f.write("\n====================\n")
        f.write(str(datetime.utcnow()) + "\n")
        f.write(str(e) + "\n")
        f.write(traceback.format_exc())
