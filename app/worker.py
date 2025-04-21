from celery import Celery

celery_app = Celery(
    "worker",
    # Redis連接
    broker="redis://localhost:6379/0",
    # 結果後端
    backend="redis://localhost:6379/0",
    # 包含任務模組
    include=["app.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Taipei",
    enable_utc=False,
)

celery_app.conf.beat_schedule = {
    "sample_task_every_hour": {
        "task": "app.tasks.sample_periodic_task",
        "schedule": 60.0,  # 每分鐘執行一次
    },
    "daily_cleanup_task": {
        "task": "app.tasks.cleanup_database",
        # 每天執行一次
        "schedule": 86400.0,
        "kwargs": {"days": 30},
        # 指定隊列
        "options": {"queue": "maintenance"},
    },    
    "minute_time_report": {
        "task": "app.tasks.current_time",
        "schedule": 60.0,  # 每60秒執行一次
    },
}

from celery.schedules import crontab

celery_app.conf.beat_schedule.update({
    "run_at_midnight": {
        "task": "app.tasks.daily_report",
        # 每天午夜執行
        "schedule": crontab(hour=0, minute=0),
    },
    "weekday_morning_task": {
        "task": "app.tasks.business_task",
        # 平日早上9點
        "schedule": crontab(hour=9, minute=0, day_of_week="1-5"),
    },
})