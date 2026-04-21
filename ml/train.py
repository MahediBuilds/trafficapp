import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
import joblib

df = pd.read_csv("../data/Metro_Interstate_Traffic_Volume.csv")

df['date_time'] = pd.to_datetime(df['date_time'])

df['hour'] = df['date_time'].dt.hour
df['day_of_week'] = df['date_time'].dt.dayofweek
df['month'] = df['date_time'].dt.month

df['holiday'] = df['holiday'].apply(lambda x: 0 if x == 'None' else 1)

df = pd.get_dummies(df, columns=['weather_main'], drop_first=True)

df = df.drop(['date_time', 'weather_description'], axis=1)

def classify(x):
    if x < 2000:
        return 0
    elif x < 4000:
        return 1
    else:
        return 2

df['traffic_level'] = df['traffic_volume'].apply(classify)

X = df.drop(['traffic_volume', 'traffic_level'], axis=1)
y_reg = df['traffic_volume']
y_clf = df['traffic_level']

X_train, X_test, y_train, y_test = train_test_split(X, y_reg, test_size=0.2)
model = LinearRegression()
model.fit(X_train, y_train)

X_train, X_test, y_train, y_test = train_test_split(X, y_clf, test_size=0.2)
clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)

joblib.dump(model, "../models/predict.pkl")
joblib.dump(clf, "../models/classify.pkl")
joblib.dump(X.columns.tolist(), "../models/columns.pkl")

print("Done")