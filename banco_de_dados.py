import sqlite3 as sql
con = sql.connect('db_web.db')

#Create a Connection
cur = con.cursor()

#Drop users table if already exsist.
cur.execute("DROP TABLE IF EXISTS usuario")

#Create users table  in db_web database
sql ='''CREATE TABLE "usuario" (
    "id"  INTEGER PRIMARY KEY AUTOINCREMENT,
    "nome"  TEXT,
    "email"  TEXT,
    "senha"  TEXT,
    "permissoes"  BOOLEAN
)
'''
cur.execute(sql)
cur.execute("DROP TABLE IF EXISTS aula")
sql = '''CREATE TABLE "aula" (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'professor_id' INTEGER,
    'exercicios' TEXT
)
'''
cur.execute(sql)
cur.execute("DROP TABLE IF EXISTS notas")
sql = '''CREATE TABLE "notas" (
    'aluno_id' INTEGER,
    'aula_id' INTEGER,
    'exercicios_acertados' INTEGER,
    'exercicios_errados' INTEGER,
    'nota_final' INTEGER
)
'''
cur.execute(sql)
cur.execute("DROP TABLE IF EXISTS exercicios")
sql = '''CREATE TABLE "exercicios" (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'enunciado' TEXT,
    'resposta' TEXT ,
    'explicaçao' TEXT,
    'resposta_correta' TEXT
)
'''
cur.execute(sql)


#commit changes
con.commit()

#close the connection
con.close()
