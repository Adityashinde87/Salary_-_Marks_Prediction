# import mysql.connector

# # Create connection
# conn = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="root",
#     database="your_database"
# )

# # Create cursor
# #cursor = conn.cursor()
# #print("Connected to MySQL successfully")

# # Close connection
# #conn.close()


# from flask import Flask, render_template, request, jsonify
# import pickle
# # import sqlite3
# import pandas as pd
# import os

# app = Flask(__name__)

# # Database Setup
# def init_db():
#     conn = mysql.connector('your_database')
#     cursor = conn.cursor()
#     # Naya schema: Name, Age, Model type sab save hoga
#     cursor.execute('''CREATE TABLE IF NOT EXISTS user_data (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT, age INTEGER, model TEXT, input REAL, prediction TEXT
#     )''')
#     conn.commit()
#     conn.close()

# init_db()

# # Models Load Karein
# def load_brains():
#     try:
#         m1 = pickle.load(open('models/linear_model.pkl', 'rb'))
#         p_data = pickle.load(open('models/poly_model.pkl', 'rb'))
#         return m1, p_data[0], p_data[1]
#     except:
#         return None, None, None

# lin_m, poly_t, poly_m = load_brains()

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         u_name = request.form.get('u_name')
#         u_age = request.form.get('u_age')
#         algo = request.form.get('algo')
        
#         if algo == 'linear':
#             val = float(request.form.get('val_linear'))
#             # Use DataFrame to avoid feature name warnings
#             X = pd.DataFrame([[val]], columns=['Experience'])
#             res = lin_m.predict(X)[0]
#             ans = f"₹{round(res, 2)}"
#         else:
#             val = float(request.form.get('val_poly'))
#             X = pd.DataFrame([[val]], columns=['Experience'])
#             res = poly_m.predict(poly_t.transform(X))[0]
#             ans = f"{round(res, 2)} Marks"

#         # Save to SQLite Database
#         conn = mysql.connector('your_database')
#         cur = conn.cursor()
#         cur.execute("INSERT INTO user_data (name, age, model, input, prediction) VALUES (?,?,?,?,?)",
#                     (u_name, u_age, algo, val, ans))
#         conn.commit()
#         conn.close()

#         return jsonify({'success': True, 'result': ans, 'user': u_name})
#     except Exception as e:
#         print(f"Internal Error: {e}")
#         return jsonify({'success': False, 'result': "Server Error: Check your input data."})

# if __name__ == '__main__':
#     app.run(debug=True)


import mysql.connector
from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# ✅ MySQL Configuration (use everywhere)
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "your_database"
}

# -------------------- Database Setup --------------------
def init_db():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        age INT,
        model VARCHAR(50),
        input FLOAT,
        prediction VARCHAR(100)
    )
    """)

    conn.commit()
    conn.close()

init_db()

# -------------------- Load Models --------------------
def load_brains():
    try:
        m1 = pickle.load(open('models/linear_model.pkl', 'rb'))
        p_data = pickle.load(open('models/poly_model.pkl', 'rb'))
        return m1, p_data[0], p_data[1]
    except:
        return None, None, None

lin_m, poly_t, poly_m = load_brains()

# -------------------- Routes --------------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        u_name = request.form.get('u_name')
        u_age = request.form.get('u_age')
        algo = request.form.get('algo')

        if algo == 'linear':
            val = float(request.form.get('val_linear'))
            X = pd.DataFrame([[val]], columns=['Experience'])
            res = lin_m.predict(X)[0]
            ans = f"₹{round(res, 2)}"
        else:
            val = float(request.form.get('val_poly'))
            X = pd.DataFrame([[val]], columns=['Experience'])
            res = poly_m.predict(poly_t.transform(X))[0]
            ans = f"{round(res, 2)} Marks"

        # ✅ MySQL Insert (FIXED)
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO user_data (name, age, model, input, prediction) VALUES (%s, %s, %s, %s, %s)",
            (u_name, u_age, algo, val, ans)
        )

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'result': ans, 'user': u_name})

    except Exception as e:
        print(f"Internal Error: {e}")
        return jsonify({'success': False, 'result': "Server Error: Check your input data."})

# -------------------- Run App --------------------
if __name__ == '__main__':
    app.run(debug=True)