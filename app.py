import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from alunos import criar_tabela, adicionar_aluno, listar_alunos
import sqlite3

criar_tabela()

st.title("📚 Sistema Escolar")

abas = st.tabs(["📝Cadastro", "❌Excluir", "📁Upload", "📊Lista & Gráfico"])

#Aba Cadastro
with abas[0]:

    st.markdown('<h2 style="color:#1f77b4;">Cadastro de Alunos</h2>', unsafe_allow_html=True)
    with st.form("form_cadastro"):
        nome_aluno = st.text_input("Nome completo:")
        sexo = st.selectbox("Sexo:", ["Masculino", "Feminino"])
        nota = st.number_input("Nota:", min_value=0.0, max_value=10.0, step=0.1)
        cadastrar = st.form_submit_button("Cadastrar")

        if cadastrar and nome_aluno.strip():
            adicionar_aluno(nome_aluno, sexo, nota)
            st.success(f"Aluno(a) {nome_aluno} cadastrado(a) com sucesso!")

#Aba Exclusão
with abas[1]:

    st.markdown('<h2 style="color:#d62728;">Excluir Aluno</h2>', unsafe_allow_html=True)
    with st.form("form_excluir"):
        id_excluir = st.number_input("Digite o ID do aluno para excluir:", min_value=1, step=1)
        excluir = st.form_submit_button("Excluir")

        if excluir:
            conexao = sqlite3.connect("banco_dados.db")
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM alunos WHERE id_aluno = ?", (id_excluir,))
            if cursor.rowcount > 0:
                st.success(f"Aluno com ID {id_excluir} excluído com sucesso!")
            else:
                st.warning(f"Nenhum aluno encontrado com ID {id_excluir}.")
            conexao.commit()
            conexao.close()

#Aba Upload
with abas[2]:

    st.markdown('<h2 style="color:#ff7f0e;">Upload de Arquivos</h2>', unsafe_allow_html=True)
    arquivo = st.file_uploader("Escolha um arquivo:", type=["csv","xlsx","txt"])
    if arquivo:
        st.success(f"Arquivo {arquivo.name} enviado com sucesso!")

        #se arquivo é CSV ou XLSX
        if arquivo.name.endswith(".csv"):
            dados_arquivo = pd.read_csv(arquivo)
            st.dataframe(dados_arquivo)
        elif arquivo.name.endswith(".xlsx"):
            dados_arquivo = pd.read_excel(arquivo)
            st.dataframe(dados_arquivo)

#Aba de lista e gráfico
with abas[3]:

    st.markdown('<h2 style="color:#2ca02c;">Lista de Alunos & Gráfico</h2>', unsafe_allow_html=True)
    resultados = listar_alunos() or []
    dados_alunos = pd.DataFrame(resultados, columns=["ID", "Nome", "Sexo", "Nota"])
    st.dataframe(dados_alunos)

    if not dados_alunos.empty:
        fig, ax = plt.subplots()
        cores = dados_alunos["Sexo"].map({"Masculino": "skyblue", "Feminino": "pink"})
        ax.bar(dados_alunos["Nome"], dados_alunos["Nota"], color=cores)
        for i, nota_val in enumerate(dados_alunos["Nota"]):
            ax.text(i, nota_val + 0.1, str(nota_val), ha="center")
        plt.xticks(rotation=45)
        plt.ylabel("Nota")
        st.pyplot(fig)
