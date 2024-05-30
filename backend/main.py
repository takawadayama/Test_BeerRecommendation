from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from db_control.models import SessionLocal, UserPreference, Beer

app = FastAPI()

# データベースセッションを取得する依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserPreferences(BaseModel):
    user_id: int

@app.post("/recommend")
def recommend_beers(preferences: UserPreferences, db: Session = Depends(get_db)):
    try:
        # 指定されたユーザーの評価データをデータベースから取得
        user_ratings = db.query(UserPreference).filter(UserPreference.user_id == preferences.user_id).all()
        
        if not user_ratings:
            return {"recommendations": []}

        # 評価データをDataFrameに変換
        user_ratings_df = pd.DataFrame([(r.beer_id, r.rating) for r in user_ratings], columns=['beer_id', 'rating'])
        print("User Ratings DataFrame:")
        print(user_ratings_df)

        # 全ビールデータをデータベースから取得
        beer_data = db.query(Beer).all()
        beer_data_df = pd.DataFrame([(b.id, b.name, b.description, b.recommendation_reason) for b in beer_data], columns=['beer_id', 'name', 'description', 'recommendation_reason'])

        # 仮の特徴量を追加
        beer_data_df['feature1'] = [0.1 * i for i in range(len(beer_data_df))]
        beer_data_df['feature2'] = [0.2 * i for i in range(len(beer_data_df))]
        
        print("Beer Data DataFrame:")
        print(beer_data_df)

        # データフレームから必要なカラムを抽出
        X = beer_data_df[['feature1', 'feature2']]
        print("Features for Model Fitting:")
        print(X)

        # 協調フィルタリングの実行
        model = NearestNeighbors(n_neighbors=5, algorithm='auto')
        model.fit(X)
        
        # ユーザー評価データとビールデータをマージ
        merged_df = user_ratings_df.merge(beer_data_df, on='beer_id')
        print("Merged DataFrame:")
        print(merged_df)

        # 予測に使用する特徴量を抽出
        user_features = merged_df[['feature1', 'feature2']]
        print("User Features for Prediction:")
        print(user_features)

        distances, indices = model.kneighbors(user_features)
        recommendations = beer_data_df.iloc[indices[0]]
        
        return {"recommendations": recommendations.to_dict('records')}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
