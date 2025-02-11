from sqlalchemy import ForeignKey,DECIMAL
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    pass

class m_product(Base):
    __tablename__ = 'm_product_taig'
    prd_id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code:Mapped[str] = mapped_column()
    name:Mapped[str] = mapped_column()
    price:Mapped[int] = mapped_column()
    from_date:Mapped[datetime] = mapped_column()
    to_date:Mapped[datetime] = mapped_column()

class m_tax(Base):
    __tablename__ = 'm_tax_taig'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column()
    percent: Mapped[float] = mapped_column()

class t_transaction(Base):
    __tablename__ = 't_transaction_taig'
    trd_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    datetime: Mapped[str] = mapped_column()
    emp_cd: Mapped[str] = mapped_column()
    store_cd: Mapped[str] = mapped_column()
    pos_no: Mapped[str] = mapped_column()
    total_amt: Mapped[int] = mapped_column()
    ttl_amt_ex_tax: Mapped[int] = mapped_column()

class d_transaction_details(Base):
    __tablename__ = 'd_transaction_details_taig'
    trd_id: Mapped[int] = mapped_column(ForeignKey('t_transaction_taig.trd_id'), primary_key=True)  # 取引 ID（FK）
    dtl_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # 明細 ID（PK）
    prd_id: Mapped[int] = mapped_column(ForeignKey('m_product_taig.prd_id'))  # 商品 ID（FK）
    prd_code: Mapped[str] = mapped_column()
    prd_name: Mapped[str] = mapped_column()
    prd_price: Mapped[int] = mapped_column()
    tax_cd: Mapped[str] = mapped_column(ForeignKey('m_tax_taig.code'))  # 税コード（FK）

class m_promotion_plan(Base):
    __tablename__ = 'm_promotion_plan_taig'
    prm_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # プロモーションID（PK）
    prm_code: Mapped[str] = mapped_column()  # プロモーションコード（13桁）
    from_date: Mapped[datetime] = mapped_column()  # 開始日（デフォルト現在時刻）
    to_date: Mapped[datetime] = mapped_column()  # 終了日（NULL 許可）
    name: Mapped[str] = mapped_column()  # プロモーション名（最大50文字）
    percent: Mapped[float] = mapped_column()  # 割引率（5桁、少数2桁）
    discount: Mapped[int] = mapped_column()  # 割引額（整数）
    prd_id: Mapped[int] = mapped_column(ForeignKey('m_product_taig.prd_id'), nullable=False)  # 商品 ID（FK）

# 以下 削除予定
class assessment_answer(Base):
    __tablename__ = 'assessment_answer'
    assessment_id:Mapped[int] = mapped_column(ForeignKey("assessment.assessment_id"), primary_key=True)
    question_id:Mapped[int] = mapped_column(primary_key=True)
    answer:Mapped[int] = mapped_column()

class assessment_result(Base):
    __tablename__ = 'assessment_result'
    assessment_id:Mapped[int] = mapped_column(ForeignKey("assessment.assessment_id"), primary_key=True)
    category:Mapped[str] = mapped_column(primary_key=True)
    priority:Mapped[int] = mapped_column()

class basic_info(Base):
    __tablename__ = 'basic_info'
    assessment_id:Mapped[int] = mapped_column(ForeignKey("assessment.assessment_id"), primary_key=True)
    age_group:Mapped[str] = mapped_column()
    country_origin:Mapped[str] = mapped_column()
    nearest_station:Mapped[str] = mapped_column()
    time_tostation:Mapped[int] = mapped_column()
    budget_lower_limit:Mapped[int] = mapped_column()
    budget_upper_limit:Mapped[int] = mapped_column()
    area_fg_smaller:Mapped[int] = mapped_column()
    area_fg_average:Mapped[int] = mapped_column()
    area_fg_larger:Mapped[int] = mapped_column()
    # MySQL変更時に沼りそうなのでboolは使わずint(0:no,1:yes)で実装始める

class area_result(Base):
    __tablename__ = 'area_result'
    assessment_id:Mapped[int] = mapped_column(ForeignKey("assessment.assessment_id"), primary_key=True)
    recommended:Mapped[str] = mapped_column()
    note:Mapped[str] = mapped_column()
    latitude: Mapped[float] = mapped_column(DECIMAL(9, 6))  # 緯度
    longitude: Mapped[float] = mapped_column(DECIMAL(9, 6))  # 経度

# # TEST Table
class Customers(Base):
    __tablename__ = 'customers'
    customer_id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_name:Mapped[str] = mapped_column()
    age:Mapped[int] = mapped_column()
    gender:Mapped[str] = mapped_column()
    