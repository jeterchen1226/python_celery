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
## 安裝必要套件
```bash
$ poetry add uvicorn fastapi celery redis
```
## 執行
###### app、worker are customized, and you can name them according to your own ideas.
```bash
$ uvicorn main:app --reload
$ celery -A app.worker worker --loglevel=info
$ celery -A app.worker beat --loglevel-info
```