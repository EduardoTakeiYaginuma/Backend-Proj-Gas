import json
from fastapi import FastAPI, Depends
import os
import mysql.connector
import uvicorn
from mysql.connector import Error
from dotenv import load_dotenv
from typing import List, Dict
import sqlite3 as sql
from fastapi.middleware.cors import CORSMiddleware





app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens (use com cuidado em produção)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP
    allow_headers=["*"],  # Permite todos os headers
)


# load_dotenv('.env')

# config = {
#     'user': os.getenv('MYSQL_USER'),
#     'password': os.getenv('MYSQL_PASSWORD'),
#     'host': os.getenv('MYSQL_HOST'),
#     'database': os.getenv('MYSQL_DATABASE'),
#     'port': os.getenv('MYSQL_PORT'),
#     'ssl_ca': os.getenv('MYSQL_SSL_CA'),
# }

# def connect_db():
#     try:
#         conn = mysql.connector.connect(**config)
#         if conn.is_connected():
#             return conn
#     except Error as err:
#         print(f"Erro: {err}")
#         return None


@app.get('/homeAluno')
async def index():
    try:
        conn=sql.connect('db_web.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM aula")
        data=cursor.fetchall()
        conn.close()
        return {"aula": json.dumps(data)}
    except Error as e:
        print(e)

@app.get('/fazer/aula/{id}')
async def get_aula(id: int):
    try:
        conn=sql.connect('db_web.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM aula WHERE id={id}")
        data=cursor.fetchone()
        conn.close()
        return {data} 
    except Error as e:
        print(e)

@app.post('/aula/criar')
async def create_aula(aula: Dict):
    try:
        dados = []
        conn = sql.connect('db_web.db')
        cursor = conn.cursor()
        for exercicio_id in aula['exercicios']:
            cursor.execute("INSERT INTO exercicios (enunciado, resposta, explicaçao, resposta_correta) VALUES (?, ?, ?, ?)", (exercicio_id["enunciado"],json.dumps(exercicio_id["respostas"]),exercicio_id["explicaçao"],exercicio_id["respostaCorreta"]),)
            result_id = cursor.lastrowid
            cursor.execute("SELECT * FROM exercicios WHERE id=?", (result_id,))
            result = cursor.fetchone()
            if result:
                dados.append(result)
        cursor.execute("INSERT INTO aula (professor_id, exercicios) VALUES (?, ?)", (1, json.dumps(dados)))
        conn.commit()
        aula_id = cursor.lastrowid
        cursor.execute("SELECT * FROM aula WHERE id=?", (aula_id,))
        row = cursor.fetchone()
        aula = {cursor.description[i][0]: value for i, value in enumerate(row)} if row else None
        conn.close()
        return {"aula": aula}
    except Error as e:
        print(e)
        return {"error": "Erro ao criar aula"}
@app.get('/aula/{id}/editar')
async def edit_aula(id: int):
    try:
        conn = sql.connect('db_web.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM aula WHERE id={id}")
        row = cursor.fetchone()
        data = {cursor.description[i][0]: row[i] for i in range(len(cursor.description))} if row else None
        conn.close()
        return {"aula": data}
    except Error as e:
        print(e)
        return {"error": "Erro ao editar aula"}
@app.put('/aula/{id}/editar')
async def update_aula(id: int, aula: Dict):
    try:
        dados = []
        conn = sql.connect('db_web.db')
        cursor = conn.cursor()
        for exercicio_id in aula['exercicios']:
            cursor.execute("UPDATE exercicios SET enunciado=? , resposta=? , explicaçao=?, resposta_correta=? WHERE id=?", (exercicio_id[1],json.dumps(exercicio_id[2]),exercicio_id[3],exercicio_id[4],exercicio_id[0],))
            cursor.execute("SELECT * FROM exercicios WHERE id=?", (exercicio_id[0],))
            result = cursor.fetchone()
            if result:
                dados.append(result)
        cursor.execute("UPDATE aula SET exercicios=? WHERE id=?", ( json.dumps(dados), id))
        conn.commit()
        cursor.execute(f"SELECT * FROM aula WHERE id={id}")
        row = cursor.fetchone()
        aula = {cursor.description[i][0]: value for i, value in enumerate(row)} if row else None
        conn.close()
        return {"aula": aula}
    except Error as e:
        print(e)
        return {"error": "Erro ao atualizar aula"}

@app.delete('/aula/{id}')
async def delete_aula(id: int):
    try:
        conn=sql.connect('db_web.db')
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM aula WHERE id={id}")
        conn.commit()
        conn.close()
        return {"message": "Aula deletada com sucesso"}
    except Error as e:
        print(e)

@app.post('/exercicio')

async def create_exercicio(exercicio: Dict):
    try:
        conn=sql.connect('db_web.db')
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO exercicios (enunciado, resposta, explicaçao, resposta_correta) VALUES ('{exercicio['enunciado']}', '{json.dumps(exercicio['resposta'])}', '{exercicio['explicaçao']}', '{exercicio['resposta_correta']}')")
        conn.commit()
        conn.close()
        return {"exercicio": exercicio}
    except Error as e:
        print(e)
    
@app.get('/fazer/exercicio/{id}')
async def get_exercicio(id: int):
    try:
        conn = sql.connect('db_web.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM exercicios WHERE id={id}")
        data = cursor.fetchone()
        conn.close()

        # Verifica se 'data' é None
        if data is None:
            return {"error": "Exercício não encontrado"}

        # Retorna o dado em formato JSON (sem necessidade de usar json.dumps manualmente)
        return {data}

    except Error as e:
        print(e)
        return {"error": "Erro ao buscar exercício"}


@app.delete('/exercicio/{id}')

async def delete_exercicio(id: int):
    try:
        conn=sql.connect('db_web.db')
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM exercicios WHERE id={id}")
        conn.commit()
        conn.close()
        return {"message": "Exercicio deletado com sucesso"}
    except Error as e:
        print(e)

@app.post('/register')

async def register(usuario: Dict):
    try:
        conn=sql.connect('db_web.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario WHERE email=?", (usuario['email'],))
        cursor.execute("SELECT * FROM usuario WHERE nome=?", (usuario['nome'],))
        existing_user = cursor.fetchone()
        if existing_user:
            conn.close()
            return {"error": "Nome ou Email already registered"}
        cursor.execute("INSERT INTO usuario (nome, email, senha, permissoes) VALUES (?, ?, ?, ?)", (usuario['nome'], usuario['email'], usuario['senha'], usuario['permissoes']))
        conn.commit()
        conn.close()
        return {"usuario": usuario}
    except Error as e:
        print(e)

@app.post('/login')

async def login(usuario: Dict):
    try:
        conn=sql.connect('db_web.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario WHERE email=? AND senha=?", (usuario['email'], usuario['senha']))
        data=cursor.fetchone()
        conn.close()
        return {"usuario": data}
    except Error as e:
        print(e)
@app.get('/usuarios')
async def get_usuarios():
    try:
        conn = sql.connect('db_web.db')
        conn.row_factory = sql.Row  # This allows us to access columns by name
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario")
        rows = cursor.fetchall()
        data = [dict(row) for row in rows]  # Convert rows to list of dictionaries
        conn.close()
        return {"usuarios": data}
    except Error as e:
        print(e)
        return {"error": "Erro ao buscar usuários"}

@app.get('/usuario/{id}')

async def get_usuario(id: int):
    try:
        conn=sql.connect('db_web.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM usuario WHERE id={id}")
        data=cursor.fetchone()
        conn.close()
        return {"usuario": data}
    except Error as e:
        print(e)

@app.put('/usuario/{id}')

async def update_usuario(id: int, usuario: Dict):
    try:
        conn=sql.connect('db_web.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE usuario SET nome=?, email=?, senha=?, permissoes=? WHERE id=?", (usuario['nome'], usuario['email'], usuario['senha'], usuario['permissoes'], id))
        conn.commit()
        conn.close()
        return {"usuario": usuario}
    except Error as e:
        print(e)

@app.delete('/usuario/{id}')

async def delete_usuario(id: int):
    try:
        conn=sql.connect('db_web.db')
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM usuario WHERE id={id}")
        conn.commit()
        conn.close()
        return {"message": "Usuario deletado com sucesso"}
    except Error as e:
        print(e)
@app.post('/moderador')
async def create_moderador(moderador: Dict):
    try:
        conn=sql.connect('db_web.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario WHERE email=? AND nome=?", (moderador['email'],moderador['nome'],))
        existing_user = cursor.fetchone()
        if existing_user:
            cursor.execute("UPDATE usuario SET permissoes=? WHERE email=? AND nome=?", (1, moderador['email'], moderador['nome']))
        conn.commit()
        conn.close()
        return {"moderador": moderador}
    except Error as e:
        print(e)

@app.post('/nota')
async def create_nota(nota: Dict):
    try:
        conn=sql.connect('db_web.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO notas (aluno_id, aula_id, nota_final) VALUES (?, ?, ?, ?, ?)", (nota['aluno_id'], nota['aula_id'], nota['nota_final']))
        conn.commit()
        conn.close()
        return {"nota": nota}
    except Error as e:
        print(e)
@app.post('/nota/{id}')
async def get_nota(id: int, nota: Dict):
    try:
        conn=sql.connect('db_web.db')
        cursor = conn.cursor()
        cursor.execute(f"UPDATE notas SET exercicios_acertados={nota['exercicios_acertados']}, exercicios_errados{nota['exercicios_errados']} WHERE id={id}")
        data=cursor.fetchone()
        conn.close()
        return {"nota": data}
    except Error as e:
        print(e)
@app.get('/nota_final/{id}')
async def get_nota_final():
    try:
        conn=sql.connect('db_web.db')
        cursor = conn.cursor()
        cursor.execute(f"UPDATE notas SET nota_final=(exercicios_acertados/exercicios_errados)*10 WHERE id={id}")
        data=cursor.fetchone()
        conn.close()
        return {"nota": data}
    except Error as e:
        print(e)
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000,)


