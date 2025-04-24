# celery 初始化和設定
from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    "worker",
    # Redis連接
    broker="redis://localhost:6379/0",
    # 後端
    backend="redis://localhost:6379/0",
    # 任務模組
    # 不同模組的方法需要在這增加模組，並在beat_schedule加入該方法設定內容
    include=["app.tasks", "app.run_scraper"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Taipei",
    enable_utc=False,
)

# celery beat 為 celery 排程器，按照內容排程執行任務
celery_app.conf.beat_schedule = {
    "write_log_every_minute": {
        #  執行任務
        "task": "app.tasks.log_current_now_time",
        # 執行頻率
        "schedule": 60.0,  # 每60秒執行一次
    },
    # 假如有個爬蟲每天早上九點需執行
    "run_scraper": {
        "task": "app.run_scraper.scraper",
        "schedule": crontab(hour=9, minute=0)
        # "schedule": crontab(hour=9, day_of_week="1-5")
        # "schedule": crontab(hour=9, day_of_month="5,25")
    }
}
