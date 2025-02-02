# uname() error回避
import platform
print("platform", platform.uname())

from sqlalchemy import create_engine, insert, delete, update, select
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json
import pandas as pd
from datetime import datetime
from typing import Tuple

from db_control.connect import engine
from db_control.mymodels import m_product, t_transaction, d_transaction_details

from models.params import CheckoutData

# m_productデータ取得
def select_m_product(code) -> Tuple[int,str]:
    
    # 初期化
    result_json = None
    status_code = 200

    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(m_product).filter(m_product.code == code)
    status_code = 200

    try:
        #トランザクションを開始
        with session.begin():
            result = query.first()
        
        # 結果をチェック
        if not result:
            # データが見つからない場合
            result_json = json.dumps({"message": "Product not found"}, ensure_ascii=False)
            status_code = 404
        else:
            # 結果を辞書に変換
            result_json = json.dumps({
                "prd_id": result.prd_id,
                "code": result.code,
                "name": result.name,
                "price": result.price
            }, ensure_ascii=False)
    except Exception as e:
        result_json = json.dumps(
            {"error": "例外が発生しました。", "details": str(e)}, 
            ensure_ascii=False
        )
        print("!!error!!")
        print(e)
        status_code = 500
    finally:
        # セッションを閉じる
        session.close()

    return status_code, result_json

# transactionデータ追加
def insert_transaction(data:CheckoutData) -> Tuple[int,str]:

    # 初期化
    result_json = None
    status_code = 200
    # 固定値
    emp_cd = data.emp_cd or "9999999999"
    store_cd = data.store_cd or "30"
    pos_no = data.pos_no or "90"
    tax_cd="10"

    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        #トランザクションを開始
        with session.begin():
            # 取引データ追加
            total_amount = sum(item.totalPrice for item in data.cart)  # 合計金額を計算
            new_transaction = t_transaction(
                datetime=datetime.now(),
                emp_cd=emp_cd,
                store_cd=store_cd,
                pos_no=pos_no,
                total_amt=total_amount,
                ttl_amt_ex_tax=total_amount #LV1では消費税計算なし
                # ttl_amt_ex_tax=round(total_amount / 1.1)
            )
            session.add(new_transaction)
            session.flush() #IDを取得するためにflush
            session.refresh(new_transaction) # 新しいtrd_id取得
            # 発行されたトランザクションIDを取得
            transaction_id = new_transaction.trd_id

            # 取引明細データ追加
            details_to_insert = [
                d_transaction_details(
                    trd_id=transaction_id,
                    dtl_id=index + 1,  # 明細ID（取引ごとに連番）
                    prd_id=item.prdId,
                    prd_code=item.code,
                    prd_name=item.name,
                    prd_price=item.price,
                    # quantity=item.quantity,
                    tax_cd=tax_cd
                )
                for index, item in enumerate(data.cart)
            ]
            session.add_all(details_to_insert)
            #正常終了
            result_json = json.dumps(
                {"total_amount":total_amount}, 
                ensure_ascii=False
            )

    except Exception as e:
        result_json = json.dumps(
            {"error": "例外が発生しました。", "details": str(e)}, 
            ensure_ascii=False
        )
        session.rollback()
        print("error:",e)
        status_code = 500
    finally:
        session.close()
    return status_code, result_json


# assessmentデータ追加
# def insert_assessment():
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     # SQLAlchemy ORMを使ったデータ挿入
#     new_assessment = assessment(
#         assessment_datetime=datetime.now().strftime("%Y%m%d%H%M%S")
#     )
#     try:
#         # トランザクションを開始
#         with session.begin():
#             # データの挿入
#             session.add(new_assessment)
#     except sqlalchemy.exc.IntegrityError:
#         print("[insert_assessment]一意制約違反によりデータ挿入に失敗しました")
#         session.rollback()
#     except Exception as e:
#         print(f"[insert_assessment]例外が発生しました: {e}")
#         session.rollback()
    
#     new_assessment_id = new_assessment.assessment_id
#     # セッションを閉じる
#     session.commit()
#     session.close()
#     return new_assessment_id

# # area_resultデータ取得
# def select_area_result(assessment_id):
#     # 初期化
#     result = None
#     result_list = None  
#     # session構築
#     Session = sessionmaker(bind=engine)
#     session = Session()       
#     query = session.query(area_result).filter(area_result.assessment_id == assessment_id)
#     try:
#         #トランザクションを開始
#         with session.begin():
#             result = query.one()
#         # 結果をオブジェクトから辞書に変換し、リストに追加
#             result_list={
#                 "assessment_id": assessment_id,
#                 "recommended": result.recommended,
#                 "note": result.note,
#                 "latitude": float(result.latitude),  # Decimal -> floatに変換
#                 "longitude": float(result.longitude)  # Decimal -> floatに変換
#             }
#     except Exception as e:
#         print(f"[select_area_result]例外が発生しました: {e}")
#         session.rollback()
#     # セッションを閉じる
#     session.close()
#     return result_list

# # データ追加(単短レコード)
# def myinsert(data_to_insert):
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     try:
#         # トランザクションを開始
#         with session.begin():
#             # データの挿入
#             session.add(data_to_insert)
#     except sqlalchemy.exc.IntegrityError:
#         print("[myinsert]一意制約違反によりデータ挿入に失敗しました")
#         session.rollback()
#     except Exception as e:
#         print(f"[myinsert]例外が発生しました: {e}")
#         session.rollback()
#     # セッションを閉じる
#     session.commit()
#     session.close()
#     return 1

# # データ追加(複数レコード)
# def myinsert_all(data_to_insert):
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     try:
#         # トランザクションを開始
#         with session.begin():
#             # データの挿入
#             session.add_all(data_to_insert)
#     except sqlalchemy.exc.IntegrityError:
#         print("[myinsert_all]一意制約違反によりデータ挿入に失敗しました")
#         session.rollback()
#     except Exception as e:
#         print(f"[myinsert_all]例外が発生しました: {e}")
#         session.rollback()
#     # セッションを閉じる
#     session.commit()
#     session.close()
#     return len(data_to_insert)

# def myselect(mymodel, customer_id):
#     # session構築
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     query = session.query(mymodel).filter(mymodel.customer_id == customer_id)
#     try:
#         # トランザクションを開始
#         with session.begin():
#             result = query.all()
#         # 結果をオブジェクトから辞書に変換し、リストに追加
#         result_dict_list = []
#         for customer_info in result:
#             result_dict_list.append({
#                 "customer_id": customer_info.customer_id,
#                 "customer_name": customer_info.customer_name,
#                 "age": customer_info.age,
#                 "gender": customer_info.gender
#             })
#         # リストをJSONに変換
#         result_json = json.dumps(result_dict_list, ensure_ascii=False)
#     except sqlalchemy.exc.IntegrityError:
#         print("一意制約違反により、挿入に失敗しました")

#     # セッションを閉じる
#     session.close()
#     return result_json

# def myselectAll(mymodel):
#     # session構築
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     query = select(mymodel)
#     try:
#         # トランザクションを開始
#         with session.begin():
#             df = pd.read_sql_query(query, con=engine)
#             result_json = df.to_json(orient='records', force_ascii=False)

#     except sqlalchemy.exc.IntegrityError:
#         print("一意制約違反により、挿入に失敗しました")
#         result_json = None

#     # セッションを閉じる
#     session.close()
#     return result_json

# def myupdate(mymodel, values):
#     # session構築
#     Session = sessionmaker(bind=engine)
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     query = update(mymodel)
#     # クエリの内容をターミナルに出力
#     print("Parameters:", query.compile().params)  # クエリに渡されるパラメータを出力
#     # クエリ実行
#     try:
#         # トランザクションを開始
#         with session.begin():
#             result = session.execute(query)
#     except sqlalchemy.exc.IntegrityError:
#         print("一意制約違反により、挿入に失敗しました")
#         session.rollback()
#     # セッションを閉じる
#     session.close()
#     return "put"

# def mydelete(mymodel, assessment_id):
#     # session構築
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     query = delete(mymodel)
#     try:
#         # トランザクションを開始
#         with session.begin():
#             result = session.execute(query)
#     except sqlalchemy.exc.IntegrityError:
#         print("一意制約違反により、挿入に失敗しました")
#         session.rollback()
 
#     # セッションを閉じる
#     session.close()
#     return "delete"