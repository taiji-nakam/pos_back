from fastapi import FastAPI,HTTPException,APIRouter,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from db_control import crud, mymodels
from models.params import CheckoutData
import json
import os
from ipaddress import ip_address, ip_network
from pydantic import BaseModel

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

@router.get("/tax")
def read_tax():
    # 最新の税情報の取得
    result = None
    status,result = crud.select_m_tax()
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

@router.get("/prd_ex/{prd_id}")
def read_prd_ex(prd_id: int):
    # 製品情報の取得(LV3)
    result = None
    status,result = crud.select_m_product_ex(prd_id)
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

# 許可されたIP範囲を .env から取得し、リスト化
ALLOWED_IP_RANGES = os.getenv("ALLOWED_IP_RANGES", "").split(",")
# 許可された IP 範囲を `ip_network` に変換
allowed_networks = [ip_network(range.strip()) for range in ALLOWED_IP_RANGES if range.strip()]

class IPRequest(BaseModel):
    ip: str

@router.post("/client-ip")
def check_client_ip(request: IPRequest):
    try:
        client_ip_obj = ip_address(request.ip)

        # 許可された範囲内かチェック
        if any(client_ip_obj in network for network in allowed_networks):
            return {"status": "allowed", "ip": request.ip}
        else:
            raise HTTPException(status_code=403, detail=f"Access denied: IP {request.ip} is not allowed")

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid IP address format")
    
@router.get("/client-ip-debug")
async def debug_client_ip(request: Request):
    headers = dict(request.headers)
    return {"headers": headers}