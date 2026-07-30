import streamlit as st
from PIL import Image
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations, product
import Analise



# Título e cabeçalho
st.title("Dashboard interativo :streamlit:", help = "Organização de dados - 03/12/2024" )
st.header("Dataset: Top 1000 filmes IMDB")

# Cria diferentes abas no site
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Entendendo o dataset", "Análises com no_of_votes","A. com Runtime", "A. com Pontuação", "A. com gross", "A. com gênero","A. com ano"])

# Cria uma aba lateral com o título escrito
st.sidebar.title("Configurações")

#Adiciona uma caixa de escolha na aba lateral
nota = st.sidebar.selectbox("Escolha aqui qual pontuação do filme deve ser usada.",
                    ["IMDB_Rating", "Avarage_score", "Meta_score"], help="Só se aplica a gráficos que utilizem a pontuação")

# Dicionário de cores com nome e código hexadecimal
cores = {
    "Vermelho": "#B22222",
    "Azul": "#4169E1",
    "Roxo": "#663399",
    "Rosa": "#FF69B4",
    "Verde": "#00FF7F",
    "Laranja": "#FF4500",
    "Amarelo": "#F0E68C",
    "Preto": "#2F4F4F",
    "Branco": "#FFFAFA"
}

# Seleção de cores pelo nome
cor_nome = st.sidebar.selectbox(
    "Escolha aqui a cor que será utilizada nos gráficos.",
    list(cores.keys())  # Mostra os nomes das cores
)

# Obtém o código hexadecimal correspondente
cor = cores[cor_nome]

# Permite que o usuário escolha quais colunas ele deseja ver nas tabelas interativas
colunas = st.sidebar.multiselect("Escolha as colunas que serão exibidas nas tabelas interativas.", Analise.df.columns, placeholder="Digite aqui")
# As funções serão executas na aba x
with tab1:

    # Função permite que o usuário visualize o dataset dinamicamente
    def tabela_interativa():
        st.write("##### Tabela interativa: Selecione os dados nas configurações para acessá-la #####")
        if colunas:
            # Põe texto no site e permite formatação
            st.write("### Dados selecionados: ###")
            st.dataframe(Analise.df[colunas])
        else:
            st.write(" *Nenhum* dado selecionado.")
          
    tabela_interativa()     
    st.write("### Esse dataset contém informações, como o nome sugere, sobre os 1000 filmes com maior pontuação IMDB. ###")
    st.write("Suas colunas são:")

    #Divide a exibição em colunas
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    #Os comandos serão executados na coluna x
    with col1:
        st.write(" **Series_Title** \nTítulo do filme\n")
        st.write("**Director**  \nNome do diretor")
    with col2:
        st.write("**Released_Year** \nData de lançamento do filme\n")
        st.write("**Stars(1,2,3,4)** \nNome das estrelas")
    with col3:
        st.write("**Runtime** \n Duração total do filme\n")
        st.write("**No_of_votes**  \nTotal de votos recebidos")
    with col4:
        st.write("**Genre**  \nGênero do filme\n")
        st.write("**Gross**  \nDinheiro arrecadado")
    with col5:
        st.write("**IMDB_Rating**  \nPontuação do filme no site do IMDB\n")
        st.write("**Score_diff**  \nDiferença entre a pontuação IMDB e o Metascore")
    with col6:
        st.write("**Meta_score**  \nNota dada pelo Metacritic ao filme\n")
        st.write("**Avarage_score**  \nPontuação média entre IMDB e o Metascore")
    st.write(Analise.df.describe())

with tab2:
    st.write(f'## Análises utilizando a coluna "*No_of_Votes*" ##')
    tabela_interativa()

    # Função exibe gráfico que relaciona o número de votos de um filme e sua pontuação
    def votes_p_score(x):
        st.write('#### Relação entre o número de votos do filme e a sua pontuação ####')
        # Permite que o usuário faça uma escolha, nesse caso, o tipo de gráfico
        tipo = st.selectbox("Selecione o tipo de gráfico:", ["Selecione", "Dispersão"], key="votes_p_score" + f'{x}')

        if tipo == "Dispersão":
            st.write(":warning: Selecione o tipo de pontuação nas configurações")

            # Gera o gráfico de barras
            fig = px.scatter(Analise.df,
                             # O tipo de pontuação é escolhida nas configurações
                             x=f'{nota}',
                             y='No_of_Votes',
                             orientation='v',  # Gráfico vertical
                             color_discrete_sequence=[f'{cor}'],  # Cor única para a linha
                             title='Relação entre número de votos de um filme e sua pontuação')
            st.plotly_chart(fig, key = 11 + x)
    votes_p_score(1)

    # Função mostra gráfico relacionando a arrecadação bruta de um filme e a quantidade de votos recebidos
    def gross_p_votes(x):
        st.write('#### Relação entre o ganho bruto do filme e o seu número de votos ####')
        # Permite que o usuário faça uma escolha, nesse caso, o tipo de gráfico
        tipo = st.selectbox("Selecione o tipo de gráfico:", ["Selecione", "Dispersão"], key="gross_p_votes" + f'{x}')

        if tipo == "Dispersão":
            # Gera o gráfico de barras
            fig = px.scatter(Analise.df,
                             # O tipo de pontuação é escolhida nas configurações
                             x='No_of_Votes',
                             y='Gross',
                             orientation='v',  # Gráfico vertical
                             color_discrete_sequence=[f'{cor}'],  # Cor única para a linha
                             title='Relação entre ganho bruto do filme (em média) e o seu número de votos')
            st.plotly_chart(fig, key = 21 + x)
    gross_p_votes(1)

    # Número de votos de um filme por sua duração
    def votes_p_runtime(x):
        st.write('#### Relação entre o número de votos e a duração do filme ####')
        tipo = st.selectbox("Selecione o tipo de gráfico:", ["Selecione", "Dispersão"], key="votes_p_year" + f'{x}')

        if tipo == "Dispersão":
            # Gera o gráfico de dispersão
            fig = px.scatter(Analise.df,
                             y='Runtime',
                             x='No_of_Votes',
                             orientation='v',  # Gráfico vertical
                             color_discrete_sequence=[f'{cor}'],  # Cor única para a linha
                             title='Relação entre o número de votos e a duração do filme')

            st.plotly_chart(fig, key = 31 + x)
    votes_p_runtime(1)

with tab3:
    st.write(f'## Análises utilizando a coluna "*Runtime*" ##')
    tabela_interativa()

    # Duração média por gênero
    def runtime_p_genre(x):
        st.write("#### Relação entre gênero e duração do filme ####")
        # Permite que o usuário faça uma escolha, nesse caso, o tipo de gráfico
        tipo = st.selectbox("Selecione o tipo de gráfico:", ["Selecione", "Barras"], key="runtime_p_genre" + f'{x}')

        if tipo == "Barras":

            # Gera o gráfico de barras
            fig = px.bar(Analise.runtime_p_genre,
                         x='Genre',
                         y='Runtime',
                         orientation='v',  # Gráfico vertical
                         color_discrete_sequence=[f'{cor}'],  # Cor única para todas as barras (vermelho)
                         labels={'y': 'Gênero', 'x': 'Duração'},
                         title='Relação entre gênero e duração do filme (em média)')

            # Ajusta o intervalo do eixo X
            fig.update_layout(
                yaxis=dict(
                    range=[
                        Analise.runtime_p_genre['Runtime'].min() - 10,  # Menor ano - 10
                        Analise.runtime_p_genre['Runtime'].max() + 10  # Maior ano + 10
                    ]
                )
            )

            st.plotly_chart(fig, key = 41 + x)

            # Se o usuário pressionar esse botão, ele vê o dataframe, se ele pressionar reset, ele volta
            st.button("Resetar", type="primary", key="runtime_p_genre1" + f'{x}')
            if st.button("Ver tabela", help="Relação gênero e duração média", key = "runtime_p_genre2" + f'{x}'):
                st.dataframe(Analise.runtime_p_genre)
    runtime_p_genre(1)

    # Número de votos de um filme por sua duração
    votes_p_runtime(2)

    # Função que imiprime o gráfico relacionando pontuação e duração do filme
    def score_p_runtime(x):
        st.write('#### Relação entre a pontuação e a duração do filme ####')
        tipo = st.selectbox("Selecione o tipo de gráfico:", ["Selecione", "Dispersão"], key="score_p_runtime" + f'{x}')

        if tipo == "Dispersão":
            st.write(":warning: Selecione o tipo de pontuação nas configurações")

            # Gera o gráfico de dispersão
            fig = px.scatter(Analise.df,
                            # O tipo de pontuação é escolhida nas configurações
                            x='Runtime',
                            y=f'{nota}',
                            orientation='v',  # Gráfico vertical
                            color_discrete_sequence=[f'{cor}'],  # Cor única para a linha
                            title='Relação entre a pontuação e a duração do filme')
            st.plotly_chart(fig, key = 51 + x)
    score_p_runtime(1)

    # Função que gera um gráfico comparando a duração e a data de lançamento dos filmes
    def runtime_p_year(x):
        st.write('#### Relação entre a data de lançamento e a duração do filme ####')
        tipo = st.selectbox("Selecione o tipo de gráfico:", ["Selecione", "Dispersão"], key="runtime_p_year" + f'{x}')

        if tipo == "Dispersão":
            # Gera o gráfico de dispersão
            fig = px.scatter(Analise.df,
                             y='Runtime',
                             x='Released_Year',
                             orientation='v',  # Gráfico vertical
                             color_discrete_sequence=[f'{cor}'],  # Cor única para a linha
                             title='Relação entre a data de lançamento e a duração do filme')
            st.plotly_chart(fig, key = 61 + x)
    runtime_p_year(1)

    # Cria e exibe gráfico de comparação entre a arrecadação bruta de um filme e sua duração
    def gross_p_runtime(x):
        st.write('#### Relação entre o ganho bruto do filme e a sua duração ####')
        # Permite que o usuário faça uma escolha, nesse caso, o tipo de gráfico
        tipo = st.selectbox("Selecione o tipo de gráfico:", ["Selecione", "Dispersão"], key="gross_p_runtime" + f'{x}')

        if tipo == "Dispersão":
            st.write(":warning: Selecione o tipo de pontuação nas configurações")

            # Gera o gráfico de barras
            fig = px.scatter(Analise.df,
                             # O tipo de pontuação é escolhida nas configurações
                             x='Runtime',
                             y='Gross',
                             orientation='v',  # Gráfico vertical
                             color_discrete_sequence=[f'{cor}'],  # Cor única para a linha
                             title='Relação entre ganho bruto do filme (em média) e sua duração')
            st.plotly_chart(fig, key = 71 + x)
    gross_p_runtime(1)

with tab4:
    st.write(f'## Análises utilizando a coluna "*{nota}*" ##')
    tabela_interativa()

    # Função que imiprime o gráfico relacionando pontuação e duração do filme
    score_p_runtime(2)

    # Função que imprime o gráfico ocorrência de cada gênero entre os top 1000 filmes
    def genre_counts(x):
        st.write("#### Ocorrência de cada gênero entre os top 1000 filmes ####")
        # Permite que o usuário faça uma escolha, nesse caso, o tipo de gráfico
        tipo = st.selectbox("Selecione o tipo de gráfico:", ["Selecione", "Barras", "Pizza"], key = 'genre_counts' + f'{x}')

        if tipo == "Barras":
            #Gera o gráfico de barras
            fig = px.bar(Analise.genre_counts,
                        x=Analise.genre_counts.index,
                        y=Analise.genre_counts.values,
                        orientation='v',  # Gráfico vertical
                        color_discrete_sequence=[f'{cor}'],  # Cor única para todas as barras selecionada nas configurações
                        labels={'y': 'Gênero', 'x': 'Número de filmes'},
                        title='Ocorrência de cada gênero entre os top 1000 filmes')
            st.plotly_chart(fig, key = 81 + x)
        else:
            if tipo == "Pizza":
                #Gera o gráfico de Pizza ou Torta
                fig = px.pie(Analise.genre_counts,
                            values=Analise.genre_counts.values,  # Os valores são os números de filmes
                            names=Analise.genre_counts.index,  # Os rótulos são os gêneros
                            color=Analise.genre_counts.index,
                            color_discrete_sequence= px.colors.qualitative.Vivid, # Usando uma paleta de cores
                            title='Distribuição dos Gêneros entre os Top 1000 Filmes')
                st.plotly_chart(fig, key = 91 + x)
    genre_counts(1)

    def score_p_year(x):
        st.write('#### Relação entre a pontuação e a data de lançamento do filme ####')
        tipo = st.selectbox("Selecione o tipo de gráfico:", ["Selecione", "Dispersão", "Barras", "Pizza"], key="score_p_year" + f'{x}')

        if tipo == "Dispersão":
            st.write(":warning: Selecione o tipo de pontuação nas configurações")

            # Gera o gráfico de dispersão
            fig = px.scatter(Analise.df,
                             # O tipo de pontuação é escolhida nas configurações
                             x='Released_Year',
                             y=f'{nota}',
                             orientation='v',  # Gráfico vertical
                             color_discrete_sequence=[f'{cor}'],  # Cor única para a linha
                             title='Relação entre a pontuação e a duração do filme')
            st.plotly_chart(fig, key = 101 + x)
            return
        if tipo == 'Barras':

            # Gera o gráfico de barras
            fig = px.bar(Analise.year_counts,
                         x=Analise.year_counts.index.astype(str),
                         y=Analise.year_counts.values,
                         orientation='v',  # Gráfico vertical
                         color_discrete_sequence=[f'{cor}'],  # Cor única para todas as barras (vermelho)
                         labels={'y': 'Período de lançamento', 'x': 'Número de filmes'},
                         title='Ocorrência de cada período entre os top 1000 filmes')
            st.plotly_chart(fig, key = 111 + x)
            return
        if tipo == 'Pizza':
            fig = px.pie(Analise.year_counts,
                        values=Analise.year_counts.values,  # Os valores são os números de filmes
                        names=Analise.year_counts.index.astype(str),  # Os rótulos são os gêneros
                        color=Analise.year_counts.index.astype(str),
                        color_discrete_sequence= px.colors.qualitative.Vivid, # Usando uma paleta de cores
                        title='Ocorrência de cada período entre os top 1000 filmes')
            st.plotly_chart(fig, key = 121 + x)
    score_p_year(1)

    # Função mostra gráfico relacionando gross e pontuação do filme
    def gross_p_score(x):
        st.write('#### Relação entre o ganho bruto do filme e a sua pontuação ####')
        # Permite que o usuário faça uma escolha, nesse caso, o tipo de gráfico
        tipo = st.selectbox("Selecione o tipo de gráfico:", ["Selecione", "Dispersão"], key="gross_p_score" + f'{x}')

        if tipo == "Dispersão":
            st.write(":warning: Selecione o tipo de pontuação nas configurações")

            # Gera o gráfico de barras
            fig = px.scatter(Analise.df,
                             # O tipo de pontuação é escolhida nas configurações
                             x=f'{nota}',
                             y='Gross',
                             orientation='v',  # Gráfico vertical
                             color_discrete_sequence=[f'{cor}'],  # Cor única para a linha
                             title='Relação entre ganho bruto do filme (em média) e sua pontuação')
            st.plotly_chart(fig, key = 131 + x)
    gross_p_score(1)

    votes_p_score(2)

with tab5:
    st.write('## Análises utilizando a coluna "*Gross*" ##')
    tabela_interativa()


    # Ganho bruto (médio) por gênero
    def gross_p_genre(x):
        st.write("#### Relação entre gênero e ganho bruto do filme ####")
        # Permite que o usuário faça uma escolha, nesse caso, o tipo de gráfico
        tipo = st.selectbox("Selecione o tipo de gráfico:", ["Selecione", "Barras"], key="genre_p_gross" + f'{x}')

        if tipo == "Barras":

            # Gera o gráfico de barras
            fig = px.bar(Analise.gross_p_genre,
                         x='Genre',
                         y='Gross',
                         orientation='v',  # Gráfico vertical
                         color_discrete_sequence=[f'{cor}'],  # Cor única para todas as barras
                         labels={'y': 'Gênero', 'x': 'Arrecadação'},
                         title='Relação entre gênero e ganho bruto do filme (em média)')
            st.plotly_chart(fig, key = 141 + x)

            # Se o usuário pressionar esse botão, ele vê o dataframe, se ele pressionar reset, ele volta
            st.button("Resetar", type="primary", key = "genre_p_gross1" + f'{x}')
            if st.button("Ver tabela", help="Relação gênero e ganho bruto médio", key = "genre_p_gross2" + f'{x}'):
                st.dataframe(Analise.gross_p_genre)
        st.write('#### Relação entre gênero e ganho bruto do filme ####')
        # Permite que o usuário faça uma escolha, nesse caso, o tipo de gráfico
        tipo = st.selectbox("Selecione o tipo de gráfico:", ["Selecione", "Barras"], key="gross_p_genre" + f'{x}')

        if tipo == "Barras":

            # Gera o gráfico de barras
            fig = px.bar(Analise.gross_p_genre,
                         x='Genre',
                         y='Gross',
                         orientation='v',  # Gráfico vertical
                         color_discrete_sequence=[f'{cor}'],  # Cor única para todas as barras 
                         labels={'y': 'Gênero', 'x': 'Arrecadação'},
                         title='Relação entre ganho bruto do filme (em média) e seus gêneros')
            st.plotly_chart(fig, key = 151 + x)

            # Se o usuário pressionar esse botão, ele vê o dataframe, se ele pressionar reset, ele volta
            st.button("Resetar", type="primary", key="gross_p_genre1" + f'{x}')
            if st.button("Ver tabela", help="Relação gênero e ganho bruto médio", key = 'gross_p_genrex2' + f'{x}'):
                st.dataframe(Analise.gross_p_genre)
    gross_p_genre(1)

    # Função mostra gráfico relacionando gross e pontuação do filme
    gross_p_score(2)

    # Função mostra gráfico relacionando a arrecadação bruta de um filme e a quantidade de votos recebidos
    gross_p_votes(2)

    # Cria e exibe gráfico de comparação entre a arrecadação bruta de um filme e sua data de lançamento
    def gross_p_year(x):
        st.write('#### Relação entre o ganho bruto do filme e a data de seu lançamento ####')
        tipo = st.selectbox("Selecione o tipo de gráfico:", ["Selecione", "Dispersão"], key="gross_p_year" + f'{x}')

        if tipo == "Dispersão":

            # Gera o gráfico de barras
            fig = px.scatter(Analise.df,
                             # O tipo de pontuação é escolhida nas configurações
                             x='Released_Year',
                             y='Gross',
                             orientation='v',  # Gráfico vertical
                             color_discrete_sequence=[f'{cor}'],  # Cor única para a linha
                             title='Relação entre ganho bruto do filme (em média) e a sua data de lançamento')
            st.plotly_chart(fig, key = 161 + x)
    gross_p_year(1)

    # Cria e exibe gráfico de comparação entre a arrecadação bruta de um filme e sua duração
    gross_p_runtime(2)

with tab6:
    st.write('## Análises utilizando a coluna "*Genre*" ##')
    tabela_interativa()

    # Ocorrência de cada gênero entre os top 1000 filmes
    genre_counts(2)

    # Ganho bruto (médio) por gênero
    gross_p_genre(2)

    # Duração média por gênero
    runtime_p_genre(2)

    # Função que mostra o gráfico relacionando a data de lançamento mais comum por gênero
    def year_p_genre(x):
        st.write("#### Relação entre data de lançamento mais comum por gênero ####")
        tipo = st.selectbox("Selecione o tipo de gráfico:", ["Selecione", "Barras"], key ="year_p_genre" + f'{x}')

        if tipo == "Barras":
            # Gera o gráfico de barras
            fig = px.bar(Analise.year_p_genre,
                         x='Genre',
                         y='Released_Year',
                         orientation='v',  # Gráfico vertical
                         color_discrete_sequence=[f'{cor}'],  # Cor única para todas as barras (vermelho)
                         labels={'y': 'Gênero', 'x': 'Ano de lançamento'},
                         title='Relação entre gênero e data de lançamento mais comum')

            # Ajusta o intervalo do eixo X
            fig.update_layout(
                yaxis=dict(
                    range=[
                        Analise.year_p_genre['Released_Year'].min() - 10,  # Menor ano - 10
                        Analise.year_p_genre['Released_Year'].max() + 10  # Maior ano + 10
                    ]
                )
            )

            st.plotly_chart(fig, key = 171 + x)

            # Se o usuário pressionar esse botão, ele vê o dataframe, se ele pressionar reset, ele volta
            st.button("Resetar", type = "primary", key = "year_p_genre1" + f'{x}')
            if st.button("Ver tabela", help = "Relação gênero e data de lançamento mais comum", key = "year_p_genre2" + f'{x}'):
                st.dataframe(Analise.year_p_genre)
    year_p_genre(1)


    # Função que mostra o gráfico relacionando a data de lançamento média por gênero
    def year_p_genre_m(x):
        st.write("#### Relação entre data de lançamento média por gênero ####")
        tipo = st.selectbox("Selecione o tipo de gráfico:", ["Selecione", "Barras"], key="year_p_genre_M" + f'{x}')

        if tipo == "Barras":
            # Gera o gráfico de barras
            fig = px.bar(Analise.year_p_genre_M,
                         x='Genre',
                         y='Released_Year',
                         orientation='v',  # Gráfico vertical
                         color_discrete_sequence=[f'{cor}'],  # Cor única para todas as barras (vermelho)
                         labels={'y': 'Gênero', 'x': 'Ano de lançamento'},
                         title='Relação entre gênero e data de lançamento média')

            # Ajusta o intervalo do eixo X
            fig.update_layout(
                yaxis=dict(
                    range=[
                        Analise.year_p_genre_M['Released_Year'].min() - 10,  # Menor ano - 10
                        Analise.year_p_genre_M['Released_Year'].max() + 10  # Maior ano + 10
                    ]
                )
            )

            st.plotly_chart(fig, key = 181 + x)

            # Se o usuário pressionar esse botão, ele vê o dataframe, se ele pressionar reset, ele volta
            st.button("Resetar", type="primary", key="year_p_genre_M1" + f'{x}')
            if st.button("Ver tabela", help="Relação gênero e média de data de lançamento", key="year_p_genre_M2" + f'{x}'):
                st.dataframe(Analise.year_p_genre_M)
    year_p_genre_m(1)

with tab7:
    st.write('## Análises utilizando a coluna "*Released_Year*" ##')
    tabela_interativa()
    
    # Exibe os gráfico que relacionam o ano de lançamento do filme com seu gênero
    year_p_genre(2)
    year_p_genre_m(2)

    # Função que cria visualizações para a relação entre a pontuação de um filme e o seu ano de lançamento
    score_p_year(2)

    # Função que cria visualizações para a relação entre a duração do filme e sua data de lançamento
    runtime_p_year(2)

    # Função que cria visualizações para a relação entre a arrecadação bruta de bilheteria de um filme e sua data de lançamento
    gross_p_year(2)
