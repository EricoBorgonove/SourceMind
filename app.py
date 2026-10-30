"""Interface principal: Streamlit + SQLite + Open-Meteo + Ollama."""
from datetime import datetime
import json
import sqlite3

import httpx
import streamlit as st

from services.database import initialize_database, list_categories, query_products
from services.ollama import ask_model, get_loaded_models
from services.responses import format_stock, format_weather, is_false_refusal
from services.weather import get_weather

st.set_page_config(page_title="IA integrada a fontes externas", page_icon="🔌")
initialize_database()
st.title("🔌 IA integrada a fontes externas")
st.caption("Streamlit + APIs REST + SQLite + Ollama")

with st.sidebar:
    st.subheader("Configurações")
    if st.button("🔄 Atualizar modelos ativos"):
        st.rerun()
    try:
        loaded_models = get_loaded_models()
        if loaded_models:
            model = st.selectbox("Modelo carregado no Ollama", loaded_models)
            st.success(f"Modelo selecionado: {model}")
        else:
            model = None
            st.warning("Nenhum modelo carregado. Execute `ollama run NOME_DO_MODELO` e atualize.")
    except (httpx.HTTPError, ValueError, KeyError) as exc:
        model = None
        st.error(f"Não foi possível consultar o Ollama: {exc}")

    source = st.radio("Fonte para a consulta", ["API de clima", "Banco de produtos"])
    if source == "API de clima":
        city = st.text_input("Cidade brasileira", "Manaus")
        explain_with_ai = st.checkbox("Interpretar clima com IA", value=True)
    else:
        category = st.selectbox("Categoria", ["Todas", *list_categories()])
        explain_with_ai = st.checkbox("Permitir explicação da IA (experimental)", value=False)

if "historico" not in st.session_state:
    st.session_state.historico = []

if st.button("Limpar conversa"):
    st.session_state.historico = []
    st.rerun()

for message in st.session_state.historico:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ex.: Qual é a temperatura? / Quais produtos estão disponíveis?")
if question:
    st.session_state.historico.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        try:
            with st.spinner("Consultando fonte..."):
                if source == "API de clima":
                    data = get_weather(city)
                    origin = "API pública Open-Meteo"
                    factual = format_weather(data)
                else:
                    data = query_products(category)
                    origin = "SQLite local"
                    factual = format_stock(data, question)

                context = json.dumps(data, ensure_ascii=False, indent=2)
                answer = factual
                used_model = "não utilizado (resposta direta da fonte)"

                if explain_with_ai:
                    if model is None:
                        st.info("Nenhum modelo carregado: exibindo somente a resposta factual.")
                    else:
                        # Confirma que o modelo continua carregado antes de chamá-lo.
                        active = get_loaded_models()
                        selected = model if model in active else (active[0] if active else None)
                        if selected:
                            used_model = selected
                            generated = ask_model(selected, question, context)
                            if not is_false_refusal(generated):
                                answer += "\n\n**Interpretação da IA:**\n\n" + generated
                            else:
                                st.info("O modelo apresentou uma recusa indevida; os dados da fonte continuam disponíveis abaixo.")
                        else:
                            st.info("O modelo deixou de estar carregado. Exibindo resposta factual.")

            st.markdown(answer)
            st.caption(f"Modelo utilizado: {used_model}")
            st.caption(f"Fonte consultada: {origin} | Consulta realizada: {datetime.now():%d/%m/%Y %H:%M:%S}")
            with st.expander("Ver dados brutos utilizados como contexto"):
                st.code(context, language="json")
        except (httpx.HTTPError, ValueError, KeyError, sqlite3.Error) as exc:
            answer = f"Não foi possível concluir a consulta: {exc}"
            st.error(answer)
        st.session_state.historico.append({"role": "assistant", "content": answer})
