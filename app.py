from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# routerオブジェクトをインポートし、posとしてエイリアスを付ける
from routers.pos import router as pos_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 必要に応じて特定のオリジンに制限
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],  # 追加: レスポンスヘッダーをクライアント側で取得可能にする
)
# routerオブジェクトをアプリケーションに追加
app.include_router(pos_router)

# uvicorn.access のロガーを有効にする
logging.getLogger("uvicorn.access").setLevel(logging.INFO)

# アプリの起動
# uvicorn起動コマンド
# uvicorn main:app --reload

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")