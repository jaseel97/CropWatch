import time
from issue_service import speak_issues

while True:
    try:
        speak_issues()
    finally:
        time.sleep(600)