import pyodbc

connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=tcp:kaassisqlserver.database.windows.net,1433;"
    "DATABASE=ussba;"
    "UID=admindbserver;"
    "PWD=Lhousseine!;"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"  # Pour tester, afin de bypasser la vérification du certificat
    "Connection Timeout=30;"
)



try:
    with pyodbc.connect(connection_string) as conn:
        print("Connexion réussie!")
except Exception as e:
    print("Erreur de connexion :", e)
