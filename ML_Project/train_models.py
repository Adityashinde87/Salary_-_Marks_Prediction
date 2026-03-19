import pandas as pd
import pickle
import os
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

# 1. Folder check
if not os.path.exists('models'):
    os.makedirs('models')

print("⏳ Training models from CSV files...")

try:
    # 2. Salary Model (Linear)
    # Check karein ki file isi folder mein ho
    df_lin = pd.read_csv('linear_regression_sample.csv')
    m1 = LinearRegression().fit(df_lin[['Experience']], df_lin['Salary'])
    pickle.dump(m1, open('models/linear_model.pkl', 'wb'))
    print("✅ Salary Model Ready.")

    # 3. Performance Model (Polynomial)
    df_poly = pd.read_csv('polynomial_regression_data.csv')
    poly_feat = PolynomialFeatures(degree=2)
    X_poly = poly_feat.fit_transform(df_poly[['Experience']])
    m2 = LinearRegression().fit(X_poly, df_poly['Salary'])
    pickle.dump((poly_feat, m2), open('models/poly_model.pkl', 'wb'))
    print("✅ Performance Model Ready.")
    
    print("\n🚀 DONE! Now you can run app.py")

except Exception as e:
    print(f"❌ ERROR: {e}")
    print("Check: Kya CSV files isi folder mein hain?")