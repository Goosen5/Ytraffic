FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    "flask>=3.0" \
    "flask-cors>=4.0" \
    "pandas>=2.1" \
    "scikit-learn>=1.4" \
    "numpy>=1.26"

COPY src ./src
COPY assets ./assets

EXPOSE 5000

CMD ["python", "-u", "src/main.py"]
