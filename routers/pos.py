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
print("許可されたIP範囲:", allowed_networks)  # 環境変数の読み込み確認

class IPRequest(BaseModel):
    ip: str

@router.get("/client-ip/{client_ip}")
def check_client_ip(client_ip: str):
    try:
        # `None` や空のIPを拒否
        if not client_ip:
            raise HTTPException(status_code=400, detail="Invalid IP address format: Empty IP")

        client_ip_obj = ip_address(client_ip)  # str → IP アドレス変換
        print(f"チェック対象のIP: {client_ip_obj}")

        # 許可された範囲が定義されていない場合はデフォルト拒否
        if not allowed_networks:
            print("許可されたIP範囲が未設定のため、すべてのアクセスを拒否")
            raise HTTPException(status_code=403, detail="Access denied: No allowed IP ranges configured")

        # 許可された範囲内かチェック
        for network in allowed_networks:
            print(f"{network} 内に {client_ip_obj} が含まれているか確認")
            if client_ip_obj in network:
                print(f"{client_ip_obj} は {network} 内に含まれる")
                return {"status": "allowed", "ip": client_ip}

        print(f"{client_ip_obj} は許可されたネットワークに含まれていない")
        raise HTTPException(status_code=403, detail=f"Access denied: IP {client_ip} is not allowed")

    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid IP address format: {client_ip}")

    
# @router.post("/client-ip")
# def check_client_ip(request: IPRequest):
#     try:
#         client_ip_obj = ip_address(request.ip)

#         # 許可された範囲内かチェック
#         if any(client_ip_obj in network for network in allowed_networks):
#             return {"status": "allowed", "ip": request.ip}
#         else:
#             raise HTTPException(status_code=403, detail=f"Access denied: IP {request.ip} is not allowed")

#     except ValueError:
#         raise HTTPException(status_code=400, detail="Invalid IP address format")
    
@router.get("/client-ip-debug")
async def debug_client_ip(request: Request):
    headers = dict(request.headers)
    return {"headers": headers}