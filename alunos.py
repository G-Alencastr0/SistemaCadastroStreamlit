import sqlite3

def criar_tabela():
    conexao = sqlite3.connect('banco_dados.db')
    cursor = conexao.cursor()
    cursor.execute(''' CREATE TABLE IF NOT EXISTS alunos (
                   id_aluno INTEGER PRIMARY KEY AUTOINCREMENT,
                   nome_aluno TEXT,
                   sexo TEXT,
                   nota REAL
                )''')
    conexao.commit()
    conexao.close()


def adicionar_aluno(nome_aluno, sexo, nota):
    conexao = sqlite3.connect('banco_dados.db')
    cursor = conexao.cursor()
    cursor.execute(
        'INSERT INTO alunos (nome_aluno, sexo, nota) VALUES (?,?,?)',
        (nome_aluno, sexo, nota)
    )
    conexao.commit()
    conexao.close()


def listar_alunos():
    conexao = sqlite3.connect('banco_dados.db')
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM alunos')
    resultados = cursor.fetchall()
    conexao.close()
    return resultados or []


def excluir_aluno(id_aluno):
    conexao = sqlite3.connect('banco_dados.db')
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM alunos WHERE id_aluno = ?", (id_aluno,))
    conexao.commit()
    linha_afetada = cursor.rowcount
    conexao.close()
    return linha_afetada > 0

