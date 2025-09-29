import pandas as pd
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer, MinMaxScaler
from sklearn.neighbors import NearestNeighbors
from db_connection import get_connection

def get_technicians_df():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM technicians", conn)
    conn.close()
    return df

def preprocess(df):
    # Split skills and one-hot encode
    df['skills'] = df['skills'].apply(lambda x: x.lower().split(','))
    mlb = MultiLabelBinarizer()
    skills_encoded = mlb.fit_transform(df['skills'])
    skills_df = pd.DataFrame(skills_encoded, columns=mlb.classes_, index=df.index)

    # Numerical features
    num_features = df[['avg_rating', 'experience_years', 'price_rate', 'job_count']]
    scaler = MinMaxScaler()
    num_scaled = pd.DataFrame(scaler.fit_transform(num_features), columns=num_features.columns, index=df.index)

    # Combine features
    X = pd.concat([skills_df, num_scaled], axis=1)
    return X, df, mlb, scaler

def recommend(skill_query, max_price=1000, location_query=''):
    df = get_technicians_df()
    X, df, mlb, scaler = preprocess(df)

    # Build NearestNeighbors model
    model = NearestNeighbors(n_neighbors=len(df), metric='euclidean')
    model.fit(X)

    # Build input vector
    skill_list = skill_query.lower().split(',')
    input_skills = [1 if s in skill_list else 0 for s in mlb.classes_]
    input_num = [0.9, 0.5, 0.2, 0.5]  # placeholder, will normalize later
    input_vector = np.array(input_skills + input_num).reshape(1, -1)

    distances, indices = model.kneighbors(input_vector)
    recommended = df.iloc[indices[0]].copy()

    # Filter by price and location
    recommended = recommended[recommended['price_rate'] <= max_price]
    if location_query:
        recommended = recommended[recommended['location'].str.lower() == location_query.lower()]

    recommended = recommended.head(5)  # top 5
    return recommended.to_dict(orient='records')
