from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db_control import crud, mymodels

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
    return crud.select_m_product(prd_id), 200
    # return {"prd_id": prd_id, "prd_name": "Product_Name"}