# Startpunkt: et officielt image med Python installeret på en lille Linux
FROM python:3.12-slim

# Alle følgende kommandoer kører i mappen /app inde i imaget
WORKDIR /app

# Dependencies først: Docker genbruger dette lag, så længe requirements.txt
# ikke ændrer sig, og builds bliver hurtige
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Kør ikke som root inde i containeren
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

# fastapi run (ikke dev) er til drift, og lytter på 0.0.0.0, så den kan nås udefra
CMD ["fastapi", "run", "app.py", "--port", "8000"]
