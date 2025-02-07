from pydantic import BaseModel
from typing import List

# 商品のデータモデル
class Item(BaseModel):
    prdId: int
    code: str
    name: str
    price: int
    quantity: int
    totalPrice: int

# カート全体のデータモデル
class Cart(BaseModel):
    cart: List[Item]

# チェックアウトのデータモデル
class CheckoutData(BaseModel):
    cart: List[Item]
    emp_cd: str  # レジ担当者コード
    store_cd: str  # 店舗コード
    pos_no: str  # POS機 ID
    tax_code: str # 税コード
    tax_percent: float # 税率