## 安裝 Redis
```bash
$ brew install redis
```
## 啟動 Redis
```bash
$ brew services start redis
```
## 檢查託管狀態
```bash
$ brew services info redis
```
## 執行
```bash
$ uvicorn main:app --reload
$ celery -A app.worker worker --loglevel=info
$ celery -A app.worker beat --loglevel-info
```