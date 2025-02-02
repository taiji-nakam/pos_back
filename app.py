from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import traceback
from fastapi.exceptions import RequestValidationError

# routerオブジェクトをインポートし、posとしてエイリアスを付ける
from routers.pos import router as pos_router

app = FastAPI()


# 例外ハンドラー: 一般的な例外をキャッチ
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    print(f"一般的なエラー発生: {exc}")
    print(f"リクエストデータ: {await request.body()}")
    traceback.print_exc()  # ✅ エラースタックを表示
    return JSONResponse(
        status_code=500,
        content={"message": "サーバーエラーが発生しました"}
    )

# 例外ハンドラー: FastAPI のリクエストバリデーションエラーをキャッチ
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"バリデーションエラー発生: {exc}")
    print(f"リクエストデータ: {await request.body()}")
    traceback.print_exc()  # ✅ エラースタックを表示
    return JSONResponse(
        status_code=422,
        content={"message": "リクエストバリデーションエラー", "details": exc.errors()}
    )

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