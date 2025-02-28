
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

@st.cache_resource
def load_data():
    return sns.load_dataset('diamonds').dropna().reset_index(drop=True)


@st.cache_resource
def load_edas(df_filtered):
    st.header('Gráficos univariantes')

    fig, ax = plt.subplots(figsize=(6,4))
    sns.kdeplot(df_filtered, x='price', color='b', fill=True)
    sns.rugplot(df_filtered, x='price', color='g')
    sns.histplot(df_filtered, x='price', kde=True)
    ax.set_title('Análisis univariante price')
    st.pyplot(fig)

    
    fig, ax = plt.subplots(figsize=(6,4))
    fig = px.box(df_filtered, x='price', labels={'price': 'Precio'}, title='Distribución de Precios (Boxplot)',template='plotly_white')
    st.plotly_chart(fig)
       
 
    st.header('Gráficos bivariantes')

    fig, ax = plt.subplots(figsize=(6,4))
    sns.scatterplot(df_filtered, x='price', y='cut', hue='color', palette='viridis', s=50,alpha=0.8,  ax=ax)
    ax.set_title('Relación entre precio, corte y color')
    ax.set_xlabel('Precio')
    ax.set_ylabel('Corte')
    ax.legend(title='Color', loc='lower center' ,bbox_to_anchor=(0.5, -0.35), ncol=7) 
    ax.grid()
    st.pyplot(fig)


    fig, ax = plt.subplots(figsize=(6,4))
    sns.scatterplot(df_filtered, x='price', y='carat', hue='clarity', palette='viridis', s=50,alpha=0.8,  ax=ax)
    ax.set_title('Relación entre precio, corte y color')
    ax.set_title('Precio')
    ax.set_ylabel('Quilates')
    ax.legend(title='Color', loc='lower center' ,bbox_to_anchor=(0.5, -0.35), ncol=8) 
    ax.grid()
    st.pyplot(fig)    
    
    st.header('Gráficos multivariantes')
    fig, ax = plt.subplots(figsize=(6,4))
    sns.heatmap(df_filtered.corr(numeric_only=True).round(2), annot=True, cmap='viridis',linewidths=0.5, ax=ax)
    ax.set_title('Correlaciones')
    st.pyplot(fig)

    # Gráfico de cajas: Distribución de precios por color
    fig, ax = plt.subplots(figsize=(6,4))
    sns.boxplot(data=df_filtered,x='color', y='price', hue='color')
    ax.set_title('Distribución de Precios por color')
    ax.set_title('Color')
    ax.set_title('Precio')
    st.pyplot(fig)
    
 
    st.header('Gráficos interactivos')

    fig, ax = plt.subplots(figsize=(6,4))
    fig = px.violin(
        df_filtered, x="cut", y="price", color="cut", box=True, title="Distribución de Precios por Corte",
        labels={"cut": "Corte", "price": "Precio"},
    )
    st.plotly_chart(fig)

    fig, ax = plt.subplots(figsize=(6,4))
    fig = px.pie(
        df_filtered, names="color", values="price", title="Distribución de colores",
        labels={"color": "Color"},
    )
    st.plotly_chart(fig)
    
st.set_page_config(
    page_title='EDAs', 
    page_icon=':bar_chart:'
)

st.title('Página 1 - EDAs ')
st.write('En esta página se presentan gráficos univariantes, bivariantes y multivariantes con Seaborn y Plotly. Además, puede filtrar los datos.')

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button('Volver a inicio', type='primary'): 
        st.switch_page('Home.py')
        
with col2:
    if st.button('Ir a Regresión',type='primary'):
        st.switch_page('pages/2 🤖 Regresión.py')
        
with col3:
    if st.button('Ir a Clasificación', type='primary'):
        st.switch_page('pages/3 🤖 Clasificación.py')

with col4:
    if st.button('Ver predicciones', type='primary'):
        st.switch_page('pages/4 📄 Ver predicciones.py')


df = load_data()
        
st.header('1. Carga de datos')
# Cargar datos
df = sns.load_dataset('diamonds').dropna()
# Mostrar datos
with st.expander('Ver datos'):
    st.dataframe(df, use_container_width=True)
# Filtros
st.header('Filtros globales')
st.subheader('Filtros categóricos')

# Filtro por cut
cut = df['cut'].unique().tolist()
selected_cut = st.multiselect('Selecciona uno o varios cortes:', options=cut, default=cut)

# Filtro por color
color = df['color'].unique().tolist()
selected_color = st.multiselect('Selecciona uno o varios colores', options=color, default=color)

# Filtro por clarity
clarity = df['clarity'].unique().tolist()
selected_clarity = st.multiselect('Selecciona una o varias claridades', options=clarity, default=clarity)

st.subheader('Filtros numéricos')

# obtenemos mínimo y máximo para usarlo en los filtros de abajo de carat
carat_min, carat_max = st.slider(
    'Selecciona rango de Quilates', 
    min_value=df['carat'].min(),
    max_value=df['carat'].max(),
    value=(df['carat'].min(), df['carat'].max())
)
# obtenemos mínimo y máximo para usarlo en los filtros de abajo de depth
depth_min, depth_max = st.slider(
    'Selecciona rango de profundidad', 
    min_value=df['depth'].min(),
    max_value=df['depth'].max(),
    value=(df['depth'].min(), df['depth'].max())
)
# obtenemos mínimo y máximo para usarlo en los filtros de abajo de table
table_min, table_max = st.slider(
    'Selecciona rango de table', 
    min_value=df['table'].min(),
    max_value=df['table'].max(),
    value=(df['table'].min(), df['table'].max())
)
# Aplicar los filtros
df_filtered = df[
    (df['cut'].isin(selected_cut)) & 
    (df['color'].isin(selected_color)) &
    (df['clarity'].isin(selected_clarity)) &
    (df['carat'] >= carat_min) & (df['carat'] <= carat_max) &
    (df['depth'] >= depth_min) & (df['depth'] <= depth_max) &
    (df['table'] >= table_min) & (df['table'] <= table_max)
]

# Mostrar datos
with st.expander('Ver datos filtrados'):
    st.dataframe(df_filtered, use_container_width=True)
st.write(f'Nº filas antes de filtrar: **{df.shape[0]}**')
st.write(f'Nº filas después de filtrar: **{df_filtered.shape[0]}**')
st.write(f'Nº filas eliminadas por filtro: **{df.shape[0] - df_filtered.shape[0]}**')



if st.button('Presentar EDA', type='primary'): 
    load_edas(df_filtered)    

 
st.header('Descargar datos')
st.html('<p style="text-align:center">Descarga el dataset original o con los filtros actuales</p>')

col1, col2 = st.columns(2, vertical_alignment='center')

with col1:
    st.download_button(
        'Descargar datos originales',
        data=df.to_csv(index=False),
        file_name='diamonds.csv',
        mime='text/csv',
        type='primary'
    ) 
    
with col2:    
    st.download_button(
        'Descargar datos filtrados',
        data=df_filtered.to_csv(index=False),
        file_name='diamonds_filtered.csv',
        mime='text/csv',
        type='primary'
    )
    
st.write()