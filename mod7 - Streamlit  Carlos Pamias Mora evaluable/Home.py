
import streamlit as st


st.set_page_config(
    page_title='Home', 
    page_icon=':house:'
)

# Header
st.header("- Ejercicio con el dataset de Diamonds -")
st.subheader("Análisis Exploratorio de Datos, Regresión y Clasificación")

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
    if st.button('Ver predicciones', type='primary'):
        st.switch_page('pages/4 📄 Ver predicciones.py')
        
st.markdown('Ejemplo de aplicación **Streamlit** para EDA, regresión y clasificación para mostrar la informacion de **Diamonds** y predecir las mediante regresión por precio y por clasificación el tipo de corte .')

# ponemos una imagen de los tipos de diamantes
st.image("data/Diamonds.jpg", caption="Tipos de diamantes")