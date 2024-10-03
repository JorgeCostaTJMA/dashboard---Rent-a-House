import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Customizando a página streamilit
st.set_page_config(page_title="Dashboard - Rent a House", layout="wide")

# Aplicando estilo CSS na página
with open("./styles.css") as f:
    st.markdown(f"<style> {f.read()} </style>", unsafe_allow_html=True)

# Carregar o CSV
df = pd.read_csv("houses_to_rent_v2.csv")

# Definindo as faixas de quantidade de quartos
faixas_quartos = [
    (1, 1),    # Faixa 1: 1 quarto
    (2, 2),    # Faixa 2: 2 quartos
    (3, 3),    # Faixa 3: 3 quartos
    (4, 4),    # Faixa 4: 4 quartos
    (5, float('inf'))  # Faixa 5: 5 ou mais quartos
]

# Função para categorizar a quantidade de quartos


def categorizar_quartos(quartos):
    for i, (low, high) in enumerate(faixas_quartos):
        if low <= quartos <= high:
            return f"{low} {'' if high != float('inf') else 'ou mais'} quarto(s)"
    return None


# Definindo as faixas de área
faixas = [
    (1, 100),            # Faixa 1: 1 a 100 m²
    (101, 300),          # Faixa 2: 101 a 300 m²
    (301, 500),          # Faixa 3: 301 a 500 m²
    (501,  float('inf'))  # Faixa 4: 501 a 800 m²
]

# Função para categorizar os valores de 'area' dentro das faixas predefinidas


def categorizar_area(area):
    for i, (low, high) in enumerate(faixas):
        if low <= area <= high:
            return f"Faixa {i+1}: {low} - {high if high != float('inf') else 'maior que'}"
    return None


# Aplicando a função para criar a nova coluna de faixas
df['area_bins'] = df['area'].apply(categorizar_area)

# Aplicando a função para criar a nova coluna de faixas de quartos
df['quartos_bins'] = df['rooms'].apply(categorizar_quartos)


# list = df.columns
df_renamed = df.rename(columns={'city': 'Cidade',
                                'area': 'Area',
                                'area_bins': 'Faixas de Area',
                                'rooms': 'Quartos',
                                'quartos_bins': 'Qtd. de Quartos',
                                'bathroom': 'Banheiros',
                                'parking spaces': 'Vagas Estacionamento',
                                'animal': 'Pets',
                                'furniture': 'Mobilia',
                                'total (R$)': 'Aluguel Total (R$)'})

# Inclusão da coluna Totalizadora das Taxas
df_renamed['Taxas'] = df_renamed['hoa (R$)'] + \
    df_renamed['property tax (R$)'] + df_renamed['fire insurance (R$)']

# Customizando os valores das colunas
df_renamed.loc[df_renamed['Pets'] == 'acept', 'Pets'] = 'Sim'
df_renamed.loc[df_renamed['Pets'] == 'not acept', 'Pets'] = 'Não'

df_renamed.loc[df_renamed['Mobilia'] == 'furnished', 'Mobilia'] = 'Sim'
df_renamed.loc[df_renamed['Mobilia'] == 'not furnished', 'Mobilia'] = 'Não'

# Selecionando colunas específicas
colunas_desejadas = ['Cidade', 'Area', 'Faixas de Area', 'Quartos', 'Qtd. de Quartos',
                     'Banheiros', 'Vagas Estacionamento', 'Pets', 'Mobilia', 'Taxas', 'Aluguel Total (R$)']

novo_df = df_renamed[colunas_desejadas]

# Customizando os valores das colunas
novo_df.loc[novo_df['Pets'] == 'acept', 'Pets'] = 'Sim'
novo_df.loc[novo_df['Pets'] == 'not acept', 'Pets'] = 'Não'

novo_df.loc[novo_df['Mobilia'] == 'furnished', 'Mobilia'] = 'Sim'
novo_df.loc[novo_df['Mobilia'] == 'not furnished', 'Mobilia'] = 'Não'

# Título do dashboard
st.title("Dashboard - SELF SERVICE RENT A HOUSE")

# Aplicando estilo CSS na página
with open("./styles.css") as f:
    st.markdown(f"<style> {f.read()} </style>", unsafe_allow_html=True)

# Definido as cores para o Dashboard
cinza_claro = '#D3D3D3'
cinza_escuro = '#808080'
cinza_medio = '#C0C0C0'
azul_escuro = '#253760'
azul_claro = '#8db7eb'

# Sidebar para seleção de cidades
st.sidebar.header('Filtros:')
st.sidebar.subheader(
    'Aqui você escolhe as características do imóvel que procura!!!')

# Define se vão ser mostrados dados de Imóveis mobiliados ou não
mobiliados = True
if st.sidebar.checkbox('Quartos Mobiliados ?'):
    furnished_df = novo_df[novo_df['Mobilia'] == 'Sim']
#    st.subheader(
#        'Comparativos entre Cidades - Imóveis Mobiliados', divider='gray')
    # st.sidebar.write('Imóvel Mobiliado')
else:
    furnished_df = novo_df[novo_df['Mobilia'] == 'Não']
#    st.subheader(
#        'Comparativos entre Cidades - Imóveis não Mobiliados', divider='gray')
    mobiliados = False


aceita_pets = True
if st.sidebar.checkbox('Aceita Pets ?'):
    furnished_df = furnished_df[furnished_df['Pets'] == 'Sim']
    if mobiliados:
        st.subheader(
            'Comparativos entre Cidades - Imóveis Mobiliados / Aceitam Pets', divider='gray')
    else:
        st.subheader(
            'Comparativos entre Cidades - Imóveis Não Mobiliados / Aceitam Pets', divider='gray')
else:
    furnished_df = furnished_df[furnished_df['Pets'] == 'Não']
    aceita_pets = False
    if mobiliados:
        st.subheader(
            'Comparativos entre Cidades - Imóveis Mobiliados / Não Aceitam Pets', divider='gray')
    else:
        st.subheader(
            'Comparativos entre Cidades - Imóveis Não Mobiliados / Não Aceitam Pets', divider='gray')
# Checkbox para seleção de cidades na barra lateral
cities = novo_df['Cidade'].unique()
selected_cities = st.sidebar.multiselect(
    'Selecione a(s) cidade(s):', options=cities, default=cities)

# Filtrar dados com base nas cidades selecionadas
if selected_cities:
    furnished_df = furnished_df[furnished_df['Cidade'].isin(selected_cities)]
else:
    furnished_df = furnished_df

# Gráfico Comparativo 1: Imóveis por Faixa de Área por cidade

# Filtrar pela Faixa de Área Selecionada
selected_area_bins = st.multiselect(
    'Selecione as faixas de área', furnished_df['Faixas de Area'].unique(), default=furnished_df['Faixas de Area'].unique())

# Filtrar o DataFrame com base na seleção do usuário
df_filtrado_faixa = furnished_df[(furnished_df['Cidade'].isin(selected_cities)) & (
    furnished_df['Faixas de Area'].isin(selected_area_bins))]

# Agrupar o DataFrame filtrado para gerar o gráfico
area_grouped_df_filtrado = df_filtrado_faixa.groupby(
    'Faixas de Area').size().reset_index(name='count')


# Dividindo a visualização em duas colunas
col1, col2 = st.columns(2)

# Coluna 1: Exibindo o gráfico de barras
with col1:
    fig, ax0 = plt.subplots(figsize=(20, 13))

    # Título do gráfico
    ax0.set_title('Quant. de Imóveis por Área', fontsize=32,
                  color=cinza_escuro, fontweight='bold')

    # Removendo Grids e Eixos
    ax0.spines['top'].set_visible(False)
    ax0.spines['right'].set_visible(False)

    # Plotando os valores
    bars = ax0.bar(area_grouped_df_filtrado['Faixas de Area'],
                   area_grouped_df_filtrado['count'], color=cinza_escuro)

    # Adicionando os valores dentro das barras
    if mobiliados:
        for bar in bars:
            yval = bar.get_height()
            ax0.text(bar.get_x() + bar.get_width()/2, yval,
                     f'{yval:.2f}', va='bottom', ha='center', fontsize=20, color=cinza_escuro)
    else:
        for bar in bars:
            yval = bar.get_height()
            ax0.text(bar.get_x() + bar.get_width()/2, yval,
                     f'{yval:.2f}', va='bottom', ha='center', fontsize=20, color=cinza_escuro)

    # Removendo o eixo Y
    ax0.set_yticks([])

    # Definindo os marcadores do eixo X
    ax0.set_xticks(range(len(area_grouped_df_filtrado)))

    # Nomes das cidades no eixo X com fonte maior e rotação horizontal
    ax0.set_xticklabels(area_grouped_df_filtrado['Faixas de Area'],
                        fontsize=20, rotation=0)

    # Exibir o gráfico
    st.pyplot(fig)

# Coluna 2: Exibindo o DataFrame de médias
with col2:
    st.subheader("Imóveis Encontrados:")
    st.dataframe(df_filtrado_faixa)

# Gerando um espaço para o select
st.markdown("<br><br>", unsafe_allow_html=True)  # Espaço com HTML <br>

# Filtrar pelas faixas de quartos
selected_room_bins = st.multiselect(
    'Selecione as Faixas de quartos', furnished_df['Qtd. de Quartos'].unique(), default=furnished_df['Qtd. de Quartos'].unique())

# Fechando o espaço
st.markdown("<br><br>", unsafe_allow_html=True)


# Visualização do segundo gráfico e seu DataFrame
col3, col4 = st.columns(2)

# Gráfico Comparativo 2: Imóveis por Qtd. de Quartos
# Customizando os dados
df_filtrado_quartos = furnished_df[(furnished_df['Cidade'].isin(selected_cities)) & (
    furnished_df['Qtd. de Quartos'].isin(selected_room_bins))]

# Agrupar o DataFrame filtrado para gerar o gráfico
area_grouped_df_quartos = df_filtrado_quartos.groupby(
    'Qtd. de Quartos').size().reset_index(name='count')

with col3:
    fig2, ax2 = plt.subplots(figsize=(20, 13))

    # Título do gráfico
    ax2.set_title('Imóveis por Qtd. de Quartos', fontsize=36,
                  color=azul_escuro, fontweight='bold')

    # Plotando os valores
    bars2 = ax2.bar(area_grouped_df_quartos['Qtd. de Quartos'],
                    area_grouped_df_quartos['count'], color=azul_escuro)

    # Adicionando os valores dentro das barras
    if aceita_pets:
        if mobiliados:
            for bar in bars2:
                yval = bar.get_height() + 20
                ax2.text(bar.get_x() + bar.get_width()/2, yval,
                         f'{yval:.0f}', va='top', ha='center', fontsize=20, color=azul_escuro)
        else:
            for bar in bars2:
                yval = bar.get_height() + 80
                ax2.text(bar.get_x() + bar.get_width()/2, yval,
                         f'{yval:.0f}', va='top', ha='center', fontsize=20, color=azul_escuro)

    else:
        if mobiliados:
            for bar in bars2:
                yval = bar.get_height() + 15
                ax2.text(bar.get_x() + bar.get_width()/2, yval,
                         f'{yval:.0f}', va='top', ha='center', fontsize=20, color=azul_escuro)
        else:
            for bar in bars2:
                yval = bar.get_height() + 25
                ax2.text(bar.get_x() + bar.get_width()/2, yval,
                         f'{yval:.0f}', va='top', ha='center', fontsize=20, color=azul_escuro)

    # Removendo Grids e Eixos
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    # Removendo os valores no eixo Y
    ax2.set_yticks([])

    # Definindo os marcadores do eixo X
    ax2.set_xticks(range(len(area_grouped_df_quartos)))

    # Definindo os labels do eixo X
    ax2.set_xticklabels(
        area_grouped_df_quartos['Qtd. de Quartos'], fontsize=20, rotation=0)

    # Exibir o gráfico
    st.pyplot(fig2)

# Coluna 4
with col4:
    st.subheader("Imóveis Encontrados:")
    st.dataframe(df_filtrado_quartos)
