import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from db_control.models import Base, engine, SessionLocal, UserPreference, Beer

# CSVファイルの絶対パスを取得
base_dir = os.path.dirname(os.path.abspath(__file__))
user_preferences_path = os.path.join(base_dir, 'user_preferences.csv')
beer_data_path = os.path.join(base_dir, 'beer_data.csv')

# 初回のみテーブルを作成
Base.metadata.create_all(bind=engine)

# 初期データの投入
def init_db():
    db = SessionLocal()
    
    # CSVからデータを読み込み
    user_data = pd.read_csv(user_preferences_path)
    beer_data = pd.read_csv(beer_data_path)

    # データをデータベースに投入
    for _, row in user_data.iterrows():
        db.add(UserPreference(user_id=row['user_id'], beer_id=row['beer_id'], rating=row['rating']))

    for _, row in beer_data.iterrows():
        db.add(Beer(id=row['beer_id'], name=row['name'], description=row['description'], recommendation_reason=row['recommendation_reason']))
    
    db.commit()
    db.close()

if __name__ == "__main__":
    init_db()
