# Utiliser une image Python allégée
FROM python:3.10-slim

# Installer les dépendances système et le pilote ODBC 17 pour SQL Server
RUN apt-get update && apt-get install -y curl gnupg build-essential
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier des dépendances et l'installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . .

# Exposer le port sur lequel Uvicorn va écouter
EXPOSE 8000

# Définir la commande pour démarrer l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
