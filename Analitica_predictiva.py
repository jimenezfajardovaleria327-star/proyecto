import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score

# ==========================================
# 1. CARGA DE DATOS
# ==========================================
df = pd.read_csv("/home/val/Descargas/Food_Delivery_Times.csv")

print("--- PRIMERAS FILAS ---")
print(df.head())

print("\n--- COLUMNAS Y TIPOS DE DATOS ---")
print(df.columns)

# Eliminar identificador no relevante
df.drop(columns=['Order_ID'], inplace=True)

print("\n--- INFORMACIÓN DEL DATASET ---")
df.info()

# ==========================================
# 2. VISUALIZACIÓN DE VALORES FALTANTES
# ==========================================
plt.figure(figsize=(10, 6))
sns.heatmap(df.isnull(), cbar=False, cmap='viridis', yticklabels=False)
plt.title('Missing Values Heatmap', fontsize=16)
plt.xlabel('Columns', fontsize=12)
plt.ylabel('Rows', fontsize=12)
plt.savefig("1_missing_values.png")
plt.close()

# ==========================================
# 3. PROCESAMIENTO Y LIMPIEZA
# ==========================================
print("\n--- PROCESAMIENTO DE DATOS ---")

# Rellenar nulos categóricos con la Moda
columns_to_fill = ['Weather', 'Traffic_Level', 'Time_of_Day', 'Vehicle_Type']
for column in columns_to_fill:
    mode_value = df[column].mode()[0]
    df[column] = df[column].fillna(mode_value)
    print(f"Column: {column} | Mode used for filling: {mode_value}")

# Rellenar nulos de experiencia con la Media
mean_value = df['Courier_Experience_yrs'].mean()
df['Courier_Experience_yrs'] = df['Courier_Experience_yrs'].fillna(mean_value)

print(f"\nMissing values in 'Courier_Experience_yrs': {df['Courier_Experience_yrs'].isnull().sum()}")
print(f"Mean value used for filling: {mean_value}")

print("\nTotal de nulos restantes:")
print(df.isnull().sum())

# ==========================================
# 4. CODIFICACIÓN (LABEL ENCODING)
# ==========================================
columns_to_encode = ['Weather', 'Traffic_Level', 'Time_of_Day', 'Vehicle_Type']
label_encoders = {}

for column in columns_to_encode:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column].astype(str))
    label_encoders[column] = le

print("\n--- PRIMERAS FILAS CODIFICADAS ---")
print(df.head())

# ==========================================
# 5. MATRIZ DE CORRELACIÓN
# ==========================================
features = [
    'Distance_km', 'Weather', 'Traffic_Level', 'Time_of_Day',
    'Vehicle_Type', 'Preparation_Time_min', 'Courier_Experience_yrs'
]
target = 'Delivery_Time_min'

correlation_matrix = df[features + [target]].corr()
correlation_with_target = correlation_matrix[target]

print("\nCorrelations with Delivery_Time_min:")
print(correlation_with_target)

plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Matrix")
plt.savefig("2_correlation_matrix.png")
plt.close()

# ==========================================
# 6. DIVISIÓN Y MODELADO
# ==========================================
print("\n--- MODELADO Y EVALUACIÓN ---")

X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Linear Regression
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
y_pred_lr = lr_model.predict(X_test)
mse_lr = mean_squared_error(y_test, y_pred_lr)
r2_lr = r2_score(y_test, y_pred_lr)

# Decision Tree Regression
dt_model = DecisionTreeRegressor(random_state=42)
dt_model.fit(X_train, y_train)
y_pred_dt = dt_model.predict(X_test)
mse_dt = mean_squared_error(y_test, y_pred_dt)
r2_dt = r2_score(y_test, y_pred_dt)

# Random Forest Regression
rf_model = RandomForestRegressor(random_state=42, n_estimators=100)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

# Gradient Boosting Regression
gb_model = GradientBoostingRegressor(random_state=42)
gb_model.fit(X_train, y_train)
y_pred_gb = gb_model.predict(X_test)
mse_gb = mean_squared_error(y_test, y_pred_gb)
r2_gb = r2_score(y_test, y_pred_gb)

print("\nModel Performance Comparison:")
print(f"Linear Regression: MSE={mse_lr:.2f}, R²={r2_lr:.2f}")
print(f"Decision Tree: MSE={mse_dt:.2f}, R²={r2_dt:.2f}")
print(f"Random Forest: MSE={mse_rf:.2f}, R²={r2_rf:.2f}")
print(f"Gradient Boosting: MSE={mse_gb:.2f}, R²={r2_gb:.2f}")

# Cross validation para Linear Regression
scores = cross_val_score(lr_model, X, y, scoring='r2', cv=5)
print(f"\nCross-validated R²: {np.mean(scores):.2f}")

# ==========================================
# 7. GRÁFICA COMPARATIVA FINAL
# ==========================================
models = ['Linear Regression', 'Decision Tree', 'Random Forest', 'Gradient Boosting']
mse = [mse_lr, mse_dt, mse_rf, mse_gb]
r2 = [r2_lr, r2_dt, r2_rf, r2_gb]

x = np.arange(len(models))
width = 0.35

fig, ax1 = plt.subplots(figsize=(10, 6))

rects1 = ax1.bar(x - width/2, mse, width, color='skyblue', label='MSE')
ax1.set_ylabel('Mean Squared Error (MSE)', color='skyblue')
ax1.set_xticks(x)
ax1.set_xticklabels(models)
ax1.set_xlabel('Models')
ax1.tick_params(axis='y', labelcolor='skyblue')

ax2 = ax1.twinx()
rects2 = ax2.bar(x + width/2, r2, width, color='orange', label='R²')
ax2.set_ylabel('R² Score', color='orange')
ax2.tick_params(axis='y', labelcolor='orange')

plt.title('Model Performance Comparison')
fig.tight_layout()

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper center', bbox_to_anchor=(0.3, 1.15), ncol=2)

plt.savefig("3_model_comparison.png")
plt.close()

print("\n¡Ejecución completada con éxito! Las imágenes se guardaron en la carpeta del proyecto.")