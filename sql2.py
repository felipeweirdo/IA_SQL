## conectar a la base de datos

import pymysql
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()  #cargar Variables de entorno

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

HOST_BD=os.getenv("HOST_BD")
PUERTO_BD=os.getenv("PUERTO_BD")
USUARIO_BD=os.getenv("USUARIO_BD")
PASSWORD_BD=os.getenv("PASSWORD_BD")
BASE_DE_DATOS=os.getenv("BASE_DE_DATOS")


def respuesta_gemini(question, prompt):
    model= genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt, question])
    return response.text

#Funcion para regresar query
def leer_sql(sql, db):
    conn = pymysql.connect(
        host=HOST_BD, 
        port=int(PUERTO_BD), 
        user=USUARIO_BD,
        password=PASSWORD_BD, 
        database=BASE_DE_DATOS
        )
    #print(conn)
    cursor = conn.cursor()
    cursor.execute(sql)
    rows=cursor.fetchall()
    for x in rows:
        print(x)

    conn.commit()
    conn.close()


prompt=[""" Eres un experto en convertir una pregunta en un query de SQL
        La base de datos tiene la tabla ordenes con las siguientes columnas idEmpresa, monto, Fecha, estatus, hora
        por ejemplo para obtener el total de ordenes en una fecha se hace de la siguiente forma
        SELECT SUM(*) from ordenes where idEmpresa = 1.
        La tabla Empresa tiene los campos idEmpresa, Nombre, RFC, insignia, alias y logo y se relaciona con la tabla
        ordenes con el campo idEmpresa, por ejemplo si quiero saber las ordenes de la empresa "RAFAS restaurant" seria algo así:
        SELECT * from ordenes where idEmpresa = (SELECT idEmpresa from Empresa WHERE nombre = "RAFAS restaurant").
        Debes considerar que el query del resultado no debe tener ``` al inicio o al final ni tampoco la palabra sql
    """,
    """ Muestra en una tabla HTML el siguiente arreglo: """]

pregunta = "quiero los nombres de las empresas registradas"
print(pregunta)

respuesta = respuesta_gemini(pregunta, prompt[0])
print(respuesta)
data= leer_sql(respuesta,"Venta.db")






