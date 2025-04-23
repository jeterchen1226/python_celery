from app.worker import celery_app
import datetime
import os

@celery_app.task()
def log_current_now_time():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "time_report.log")
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    cutoff_date = now - datetime.timedelta(days=7)
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        recent_lines = []
        for line in lines:
            if line.strip():
                try:
                    line_date_str = line.split(" ")[0]
                    line_date = datetime.datetime.strptime(line_date_str, "%Y-%m-%d")
                    if line_date >= cutoff_date:
                        recent_lines.append(line)
                except Exception:
                    recent_lines.append(line)
        with open(log_path, "w", encoding="utf-8") as f:
            f.writelines(recent_lines)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"{current_time} - 每分鐘時間紀錄\n")
    return {"status": "logged", "time": current_time}
