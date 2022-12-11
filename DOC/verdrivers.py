
"""
Este script es una pequenya herramienta para mirar que drivers de base de datos nos proporciona SQL SERVER
en el mejor de los casos tenemos 'ODBC Driver 17 for SQL Server' incluido o algun otro
"""


import pyodbc

print(pyodbc.drivers())

