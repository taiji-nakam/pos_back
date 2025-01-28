from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# routerオブジェクトをインポートし、posとしてエイリアスを付ける
from routers.pos import router as pos_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 必要に応じて特定のオリジンに制限
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# routerオブジェクトをアプリケーションに追加
app.include_router(pos_router)