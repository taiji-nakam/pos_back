from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.db_control import crud, mymodels
import json

app = FastAPI()

# CORS 設定を追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 必要に応じて特定のオリジンに制限
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/prd/{prd_id}")
def read_prd(prd_id: int, q: str = None):
    # 製品情報の取得
    result = None
    status,result = crud.select_m_product(prd_id)
    # ステータスコードに応じた処理
    if status == 404:
        return JSONResponse(
            content=json.loads(result),  # JSON を直接返す
            status_code=404
        )
    elif status != 200:
        raise HTTPException(
            status_code=status,
            detail=json.loads(result)
        )

    # 正常レスポンス
    return json.loads(result)  # JSON を直接返す
    # return {"prd_id": prd_id, "prd_name": "Product_Name"}