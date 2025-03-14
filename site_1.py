import json
from fastapi import FastAPI, Depends
import os
import mysql.connector
import uvicorn
from mysql.connector import Error
from dotenv import load_dotenv
from typing import List, Dict
import sqlite3 as sql

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

app = FastAPI()

@app.get('/')
async def index():
    try:
        conn=sql.connect('db_web.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM aula")
        data=cursor.fetchall()
        conn.close()
        return {"aula": data}
    except Error as e:
        print(e)

@app.get('/aula/{id}')
async def get_aula(id: int):
    try:
        conn=sql.connect('db_web.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM aula WHERE id={id}")
        data=cursor.fetchone()
        conn.close()
        return {"aula": data}
    except Error as e:
        print(e)

@app.post('/aula')
async def create_aula(aula: Dict):
    try:
        conn=sql.connect('db_web.db')
        cursor = conn.cursor()
        data = []
        for exercicio_id in aula['exercicios']:
            cursor.execute("SELECT * FROM exercicios WHERE id=?", (exercicio_id,))
            data.extend(cursor.fetchall())
        cursor.execute("INSERT INTO aula (professor_id, exercicios) VALUES (?, ?)", (aula['professor_id'], json.dumps(data)))
        conn.commit()
        conn.close()
        return {"aula": aula}
    except Error as e:
        print(e)

@app.put('/aula/{id}')
async def update_aula(id: int, aula: Dict):
    try:
        conn=sql.connect('db_web.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM exercicos WHERE id=?", (aula['exercicios'],))
        data = cursor.fetchall()
        cursor.execute("UPDATE aula SET professor_id=?, exercicios=? WHERE id=?", (aula['professor_id'], json.dumps(data), id))
        conn.commit()
        conn.close()
        return {"aula": aula}
    except Error as e:
        print(e)

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
        resposta_json = json.dumps(exercicio['resposta'])
        cursor.execute(f"INSERT INTO exercicios (enunciado, resposta, explicaçao, resposta_correta) VALUES ('{exercicio['enunciado']}', '{json.dumps(exercicio['resposta'])}', '{exercicio['explicaçao']}', '{exercicio['resposta_correta']}')")
        conn.commit()
        conn.close()
        return {"exercicio": exercicio}
    except Error as e:
        print(e)
    
@app.get('/exercicio/{id}')
async def get_exercicio(id: int):
    try:
        conn=sql.connect('db_web.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM exercicios WHERE id={id}")
        data=cursor.fetchone()
        conn.close()
        return {"exercicio": data}
    except Error as e:
        print(e)

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
        cursor.execute(f"UPDATE notas SET exercicios_acertados={nota["exercicios_acertados"]}, exercicios_errados{nota["exercicios_errados"]} WHERE id={id}")
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


