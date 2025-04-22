from app.worker import celery_app
import time
from typing import Dict, Optional
import datetime
import os

# 範例任務
@celery_app.task()
def sample_task(param1: str, param2: Optional[int] = None) -> Dict:
    time.sleep(5)
    result = f"任務完成處理 {param1}"
    if param2:
        result += f", 參數值: {param2}"
    return {"status": "success", "result": result}

# 排程定期執行的任務
@celery_app.task()
def sample_periodic_task():
    return {"time": time.time(), "message": "定期任務已執行"}

# 清理舊資料的任務
@celery_app.task()
def cleanup_database(days: int = 30):
    return f"已清理 {days} 天前的資料"

# 生成每日報告
@celery_app.task()
def daily_report():
    # 報告生成邏輯
    return "每日報告已生成"

# 工作日業務相關任務
@celery_app.task()
def business_task():
    return "業務處理完成"

# 每分鐘執行的任務
@celery_app.task(name="app.tasks.minute_task")
def minute_task():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    return f"每分鐘任務已執行，執行時間: {current_time}"

@celery_app.task()
def current_time():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"現在時間：{current_time}")
    return {"current_time": current_time, "timestamp": datetime.datetime.now().timestamp(), "message": "排程回傳時間"}

# 當下時間 log
@celery_app.task()
def log_current_now_time():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "time_report.log")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"{current_time} - 每分鐘時間紀錄\n")
    return {"status": "logged", "time": current_time}