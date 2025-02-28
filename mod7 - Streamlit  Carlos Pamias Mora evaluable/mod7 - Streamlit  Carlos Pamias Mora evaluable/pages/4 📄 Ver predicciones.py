import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Configuración de la conexión a MySQL usando SQLAlchemy
db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root', 
    'password': 'admin',
    'database': 'predicciones'  
}

def connect_to_database():
    """Establece una conexión a la base de datos usando SQLAlchemy."""
    try:
        # Crear la URL de conexión
        connection_string = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
        engine = create_engine(connection_string)
        return engine
    except Exception as e:
        st.error(f"Error al conectar a la base de datos: {e}")
        return None

def fetch_data(engine):
   
    try:
        query = "SELECT * FROM prediccion"
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        st.error(f"Error al recuperar datos: {e}")
        return None

# Configuración de la página
st.set_page_config(
    page_title='Ver predicciones', 
    page_icon='📄'
)

st.title('Página 4 - Ver predicciones')

col1, col2, col3, col4= st.columns(4)

with col1:
    if st.button('Ir a EDAs', type='primary'):
        st.switch_page('pages/1 📊 EDAs.py')
        
with col2:
    if st.button('Ir a Regresión',type='primary'):
        st.switch_page('pages/2 🤖 Regresión.py')
        
with col3:
    if st.button('Ir a Clasificación', type='primary'):
        st.switch_page('pages/3 🤖 Clasificación.py')

with col4:
    if st.button('Volver a inicio', type='primary'): 
        st.switch_page('Home.py')

# Conectar a la base de datos
engine = connect_to_database()
if engine is None:
    st.stop()  

# Recuperar datos
df = fetch_data(engine)
if df is not None and not df.empty:
    st.write("Datos almacenados en la base de datos:")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No se encontraron datos en la base de datos.")

# Cerrar la conexión
engine.dispose()  