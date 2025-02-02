from fastapi import FastAPI,HTTPException,APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from db_control import crud, mymodels
from models.params import CheckoutData
import json

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Hello, POS(FastAPI)"}

@router.get("/prd/{prd_id}")
def read_prd(prd_id: int):
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

@router.post("/checkout")
async def checkout(data: CheckoutData):
    print("###checkout:", data)
    if not data.cart:
        return {"message": "カートが空です", "total": 0}
    # total_amount = sum(item.totalPrice for item in data.cart)  # 合計金額を計算
    status,result = crud.insert_transaction(data)
    # ステータスコードに応じた処理
    if status != 200:
        raise HTTPException(
            status_code=status,
            detail=json.loads(result)
        )
    
    # 正常レスポンス
    return json.loads(result)  # JSON を直接返す