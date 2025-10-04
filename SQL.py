import mysql.connector
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

load_dotenv()
sql_user = os.getenv('sql_user', 'root')
sql_password = os.getenv('sql_password')

# connection to SQL Server
connection = mysql.connector.connect(
    host="localhost",
    user=sql_user,
    password=sql_password,
    database='templayer'
)

if not connection:
    raise("Could not establish sql connection")
else:
    print("sucess")

query = "SELECT temp, humidity, wind_speed, layer_count FROM userData WHERE layer_count IS NOT NULL;"
df = pd.read_sql(query, connection)

# features (X) and Target (y)
X = df[['temp', 'humidity', 'wind_speed']]
y = df['layer_count']


print(y)

# build model
model = LinearRegression()
model.fit(X, y)

print("Coefficients:", model.coef_)
print("Intercept:", model.intercept_)

plt.plot(X, y)
plt.ylabel('layer_count')
plt.show()