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
    