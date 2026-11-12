import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import json

#Página
st.set_page_config(
    page_title="AI Sales Analyst",
    page_icon="📈",
    layout="wide"
)

#Dados
@st.cache_data
def carregar_dados():
    df = pd.read_csv(
        "vendas_excel.csv",
        sep=";",
        decimal=",",
        encoding="utf-8-sig"
    )

    df.columns = df.columns.str.strip().str.lower()

    df["data_venda"] = pd.to_datetime(
        df["data_venda"],
        dayfirst=True
    )

    return df

df = carregar_dados()

#Formatando valor
def formatar_moeda(valor):
    return(f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

#Cabeçalho
st.title("AI Sales Analyst")

st.subheader("Inteligência Artificial aplicada à análise de vendas")

st.write("Bem-Vindo a AI Sales Analyst  \n"
         "Aqui você poderá analisar suas vendas com maior facilidade.")

st.divider()

st.sidebar.title("Filtros")

categorias = sorted(df["categoria"].unique())
estados = sorted(df["estado"].unique())

categorias_selecionadas = st.sidebar.multiselect(
    "Categorias",
    options=categorias,
    default=categorias
)

estados_selecionados = st.sidebar.multiselect(
    "Estados",
    options=estados,
    default=estados
)

data_min = df["data_venda"].min().date()
data_max = df["data_venda"].max().date()

periodo = st.sidebar.date_input(
    "Periodo das vendas",
    value=(data_min, data_max),
    min_value=data_min,
    max_value=data_max
)

if len(periodo) == 2:
    data_inicio, data_fim = periodo
    df_filtrado = df[
        (df["categoria"].isin(categorias_selecionadas)) &
        (df["estado"].isin(estados_selecionados)) &
        (df["data_venda"].dt.date >= data_inicio) &
        (df["data_venda"].dt.date <= data_fim)
    ]

else:
    df_filtrado = df.iloc[0:0]

#Indicadores
st.header("Visão geral")

if df_filtrado.empty:
    st.warning("Nenhuma venda encontrada")

else:
    faturamento = df_filtrado["valor_total"].sum()

    quantidade_vendas = df_filtrado["id_venda"].nunique()

    unidades_vendidas = df_filtrado["quantidade"].sum()

    ticket_medio = faturamento / quantidade_vendas

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Faturamento total",
        formatar_moeda(faturamento)
    )

    col2.metric(
        "Vendas realizadas",
        f"{quantidade_vendas:,}".replace(",", ".")
    )

    col3.metric(
        "Unidades vendidas",
        f"{unidades_vendidas:,}".replace(",", ".")
    )

    col4.metric(
        "Ticket médio",
        formatar_moeda(ticket_medio)
    )

    st.divider()

    st.dataframe(df_filtrado.head(10), width="stretch")

    st.header("Desempenho de vendas")

    vendas_mensais = (
        df_filtrado
        .assign(mes=df_filtrado["data_venda"].dt.to_period("M"))
        .groupby("mes")["valor_total"]
        .sum()
        .reset_index()
    )

    vendas_mensais["mes"] = (
        vendas_mensais["mes"].astype(str)
    )

    fig_mensal = px.line(
        vendas_mensais,
        x="mes",
        y="valor_total",
        markers=True,
        title="Evolução mensal do faturamento",
        labels={
            "mes": "Mês",
            "valor_total": "Faturamento (R$)"
        }
    )

    fig_mensal.update_layout(
        xaxis_title="Mês",
        yaxis_title="Faturamento (R$)",
        hovermode="x unified"
    )

    st.plotly_chart(fig_mensal, width="stretch")

    #Faturamento separado por categoria

    col1, col2 = st.columns(2)

    with col1:

        faturamento_categoria = (
            df_filtrado
            .groupby("categoria")["valor_total"]
            .sum()
            .reset_index()
            .sort_values("valor_total", ascending=False)
        )

        fig_categoria = px.bar(
            faturamento_categoria,
            x="categoria",
            y="valor_total",
            title="Faturamento por categoria",
            labels={
                "categoria": "Categoria",
                "valor_total": "Faturamento (R$)"
            },
            text_auto=".2s"
        )

        st.plotly_chart(
            fig_categoria,
            width="stretch"
        )

    #Ranking dos produtos
    with col2:

        ranking_produtos = (
            df_filtrado
            .groupby("produto")["quantidade"]
            .sum()
            .reset_index()
            .sort_values("quantidade", ascending=False)
            .head(10)
        )

        fig_produtos = px.bar(
            ranking_produtos,
            x="quantidade",
            y="produto",
            orientation="h",
            title="Top 10 produtos mais vendidos",
            labels={
                "produto": "Produto",
                "quantidade": "Unidades vendidas"
            }
        )

        fig_produtos.update_layout(
            yaxis={"categoryorder": "total ascending"}
        )

        st.plotly_chart(
            fig_produtos,
            width="stretch"
        )

    #Faturamento separado por Estado
    st.header("Desempenho por região")

    faturamento_estado = (
        df_filtrado
        .groupby("estado")["valor_total"]
        .sum()
        .reset_index()
        .sort_values("valor_total", ascending=False)
    )

    fig_estado = px.bar(
        faturamento_estado,
        x="estado",
        y="valor_total",
        title="Faturamento por estado",
        labels={
            "estado": "Estado",
            "valor_total": "Faturamento (R$)"
        },
        text_auto=".2s"
    )

    st.plotly_chart(
        fig_estado,
        width="stretch"
    )

    #Tabela de vendas
    st.header("Dados detalhados")

    st.dataframe(
        df_filtrado.sort_values(
            "data_venda",
            ascending=False
        ),
        width="stretch",
        hide_index=True
    )

    #Exportação dos dados
    csv_exportacao = df_filtrado.to_csv(
        index=False,
        sep=";",
        decimal=",",
        encoding="utf-8-sig"
    )

    st.download_button(
        label="📥 Exportar dados filtrados",
        data=csv_exportacao,
        file_name="relatorio_vendas.csv",
        mime="text/csv"
    )

    #Inteligencia Artificial 
    st.divider()

    st.header("Converse com nossa IA 🤖")

    st.write("Faça perguntas sobre suas vendas")

    assinatura_filtros = json.dumps({
        "categorias": categorias_selecionadas,
        "estados": estados_selecionados,
        "periodo": [str(data_inicio), str(data_fim)]
    }, sort_keys=True)

    if st.session_state.get("assinatura_filtros") != assinatura_filtros:
        st.session_state["historico_chat"]= []
        st.session_state["assinatura_filtros"] = assinatura_filtros

    if "historico_chat" not in st.session_state:
        st.session_state["historico_chat"] = []

    #Preparar informações para a IA
    faturamento_categoria_ia = (
        df_filtrado.groupby("categoria")["valor_total"]
        .sum()
        .round(2)
        .to_dict()
    )

    faturamento_estado_ia = (
        df_filtrado.groupby("estado")["valor_total"]
        .sum()
        .round(2)
        .to_dict()
    )

    produtos_ia = (
        df_filtrado.groupby("produto")["quantidade"]
        .sum()
        .sort_values(ascending=False)
        .to_dict()
    )

    vendas_mensais_ia = (
        df_filtrado
        .assign(mes=df_filtrado["data_venda"].dt.to_period("M").astype(str))
        .groupby("mes")["valor_total"]
        .sum()
        .round(2)
        .to_dict()
    )

    contexto = {
        "periodo_analisado": {
            "inicio": str(data_inicio),
            "fim": str(data_fim)
        },
        "filtros": {
            "categorias": categorias_selecionadas,
            "estados": estados_selecionados
        },
        "indicadores": {
            "faturamento_total": round(float(faturamento), 2),
            "quantidade_vendas": int(quantidade_vendas),
            "unidades_vendidas": int(unidades_vendidas),
            "ticket_medio": round(float(ticket_medio), 2)
        },
        "faturamento_por_categoria": faturamento_categoria_ia,
        "faturamento_por_estado": faturamento_estado_ia,
        "quantidade_por_produto": produtos_ia,
        "faturamento_mensal": vendas_mensais_ia
    }

    contexto_json = json.dumps(
        contexto,
        ensure_ascii=False,
        indent=2
    )

    #Histórico da conversa
    for mensagem in st.session_state["historico_chat"]:
        with st.chat_message(mensagem["role"]):
            st.markdown(mensagem["content"])

    #Campo para enviar perguntas
    pergunta = st.chat_input(
        "Ex.: Qual categoria teve o maior faturamento?"
    )

    if pergunta:

        st.session_state["historico_chat"].append({
            "role": "user",
            "content": pergunta
        })

        with st.chat_message("user"):
            st.markdown(pergunta)

        try:

            api_key = st.secrets["OPENROUTER_API_KEY"]

            mensagens_api = [
                {
                    "role": "system",
                    "content": f"""
                    Você é um analista de vendas especializado
                    em inteligência de negócios.

                    Responda sempre em português brasileiro.

                    Analise exclusivamente os dados fornecidos
                    no contexto abaixo.

                    Regras:
                    - Não invente números ou informações.
                    - Utilize os indicadores fornecidos para responder.
                    - Considere os filtros aplicados no dashboard.
                    - Explique os resultados de maneira clara.
                    - Apresente comparações quando forem possíveis.
                    - Sugira oportunidades comerciais com base nos dados.
                    - Se não houver informação suficiente, diga isso.
                    - O ticket médio corresponde ao faturamento
                      dividido pelo número de vendas.
                    - O faturamento representa a soma de valor_total
                      registrado no conjunto de dados.

                    CONTEXTO DOS DADOS:

                    {contexto_json}
                    """
                },
                *st.session_state["historico_chat"]
            ]

            with st.chat_message("assistant"):

                with st.spinner("Analisando seus dados..."):

                    response = requests.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {api_key}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
                            "messages": mensagens_api
                        },
                        timeout=90
                    )

                    if response.status_code == 200:

                        resultado = response.json()

                        resposta_ia = (
                            resultado["choices"][0]["message"]["content"]
                        )

                        if not resposta_ia:
                            st.error("A IA retornou uma resposta vazia.")

                        else:
                            st.markdown(resposta_ia)

                            st.session_state["historico_chat"].append({
                                "role": "assistant",
                                "content": resposta_ia
                            })

                    else:
                        st.error(
                            f"Erro na API ({response.status_code}): "
                            f"{response.text[:500]}"
                        )

        except requests.exceptions.RequestException as erro:
            st.error(f"Erro de comunicação: {erro}")

        except Exception as erro:
            st.error(f"Erro ao utilizar a IA: {erro}")

#Rodapé
st.divider()

st.caption(
    "AI Sales Analyst | Projeto de análise de dados com Python, "
    "Pandas, Streamlit e Plotly."
)