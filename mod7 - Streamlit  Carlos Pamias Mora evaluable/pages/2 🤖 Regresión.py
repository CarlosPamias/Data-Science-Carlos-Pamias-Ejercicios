import streamlit as st
import joblib
import seaborn as sns
import pandas as pd 
import os
import pymysql
from datetime import datetime
import mysql.connector as con

@st.cache_resource
def load_scikit_model():
    model_path = 'models/pipeline_regresion.joblib'
    if not os.path.exists(model_path):
        st.error(f"El modelo no fue encontrado en la ruta: {model_path}")
        return None
    return joblib.load(model_path)

@st.cache_resource
def load_data():
    return sns.load_dataset('diamonds').dropna().reset_index(drop=True)

db_config = {
    'host': 'localhost',
    'port' : 3306,
    'user': 'root', 
    'password': 'admin',
    'database': 'predicciones'  
}
def create_database_and_table():
    try:
        # Conectar sin especificar la base de datos
        conn = pymysql.connect(
            host="localhost",
            port= 3306,
            user= "root",
            password= "admin"
        )
        cursor = conn.cursor()

        # Crear la base de datos si no existe
        cursor.execute("CREATE DATABASE IF NOT EXISTS predicciones")
        conn.commit()

        # Conectar a la base de datos recién creada
        conn.close()
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        # Crear la tabla si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prediccion (
                id_orden INT AUTO_INCREMENT PRIMARY KEY,
                Fecha_pred DATE,
                Hora_pred TIME,
                Tipo_prediccion VARCHAR(20),
                carat FLOAT,
                cut VARCHAR(10),
                color VARCHAR(10),
                clarity VARCHAR(10),
                depth FLOAT,
                table_size FLOAT,
                price INT,
                x FLOAT,
                y FLOAT,
                z FLOAT,
                pred_regresion INT,
                pred_clasificacion VARCHAR(20)
            )
        ''')
        conn.commit()

        return conn, cursor

    except Exception as e:
        st.error(f"Error al conectar a la base de datos: {e}")
        return None, None

# Función para insertar datos en la base de datos
def insert_prediccion(conn, cursor, data):
    try:
        cursor.execute('''
            INSERT INTO prediccion (
                Fecha_pred, Hora_pred, Tipo_prediccion, carat, cut, color, clarity, 
                depth, table_size, price, x, y, z, pred_regresion, pred_clasificacion
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', data)
        conn.commit()
    except Exception as e:
        st.error(f"Error al insertar datos: {e}")

st.set_page_config(
    page_title='Regresión', 
    page_icon=':robot_face:'
)

st.title('Página 2 - Regresión')

model = load_scikit_model()

df = load_data()

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button('Ir a EDAs', type='primary'):
        st.switch_page('pages/1 📊 EDAs.py')    
        
with col2:
    if st.button('Volver a inicio', type='primary'): 
        st.switch_page('Home.py')
        
with col3:
    if st.button('Ir a Clasificación', type='primary'):
        st.switch_page('pages/3 🤖 Clasificación.py')
        
with col4:
    if st.button('Ver predicciones', type='primary'):
        st.switch_page('pages/4 📄 Ver predicciones.py')

# Mostrar datos
with st.expander('Ver datos'):
    st.dataframe(df, use_container_width=True)

# 2. Formulario para predicción
st.header('Introduce datos para la predicción')
price_mean = df['price'].mean()

# Crear la base de datos y la tabla
conn, cursor = create_database_and_table()
if conn is None or cursor is None:
    st.stop()  # Detener la aplicación si hay un error de conexión
  
with st.form("diamonds_form"):
    
    carat = st.number_input(
                    'Introduce total Quilates (carat)', 
                    min_value=df['carat'].min(),
                    max_value=df['carat'].max(),
                    value=df['carat'].mean(), 
                    step=0.01
    )
    cut = st.selectbox('Introduce corte (cut)', options = df['cut'].unique().tolist())
    color = st.selectbox('Introduce color (color)', options= df['color'].unique().tolist())
    clarity = st.selectbox('Introduce claridad (clarity)',options= df['clarity'].unique().tolist())
    depth = st.number_input(
                    'Introduce total profundidad (depth)', 
                    min_value=df['depth'].min(),
                    max_value=df['depth'].max(),
                    value=df['depth'].mean(), 
                    step=0.1
    )
    table = st.number_input(    
                    'Introduce total tabla (table)', 
                    min_value=df['table'].min(),
                    max_value=df['table'].max(),
                    value=df['table'].mean(), 
                    step=1.0
    )
    x = st.number_input(
                    'Introduce total de X (x)', 
                    min_value=df['x'].min(),
                    max_value=df['x'].max(),
                    value=df['x'].mean(), 
                    step=0.01
    )
    y = st.number_input(    
                    'Introduce total de Y (y)', 
                    min_value=df['y'].min(),
                    max_value=df['y'].max(),
                    value=df['y'].mean(), 
                    step=0.01
    )
    z = st.number_input(
                    'Introduce total de Z (z)', 
                    min_value=df['z'].min(),
                    max_value=df['z'].max(),
                    value=df['z'].mean(), 
                    step=0.01
    )

    boton_enviar = st.form_submit_button("Generar predicción")

    if boton_enviar:
        if carat <= 0 or depth <= 0 or table <= 0 or x <= 0 or y <= 0 or z <= 0:
            st.error("Por favor, introduce valores válidos para todas las características.")
        else:
            X_new = pd.DataFrame({
                'carat': [carat],
                'cut': [cut],
                'color': [color],
                'clarity': [clarity],
                'depth': [depth],
                'table': [table],
                'x': [x],
                'y': [y],
                'z': [z]                       
            })
            try:
                prediccion = model.predict(X_new)[0] 
                delta_value = prediccion - price_mean
                col1, col2 = st.columns(2)
                col1.metric('Precio estimado (predicción)', value=f'{prediccion:,.2f} $', delta=f'{delta_value:,.2f} $')
                col2.metric('Precio medio', value=f'{price_mean:,.2f} $')
            # Obtener fecha y hora actuales
                now = datetime.now()
                fecha_pred = now.strftime("%Y-%m-%d")
                hora_pred = now.strftime("%H:%M:%S")

                # Tipo de predicción
                tipo_prediccion = "Regresion"

                # Preparar datos para guardar en la base de datos
                data = (
                    fecha_pred, hora_pred, tipo_prediccion, carat, cut, color, clarity,
                    depth, table, None, x, y, z, prediccion, None
                )

                # Insertar datos en la base de datos
                insert_prediccion(conn, cursor, data)
                st.success("Datos guardados correctamente en la base de datos.")

            except Exception as e:
                st.error(f"Error al generar la predicción: {e}")

    
    
    