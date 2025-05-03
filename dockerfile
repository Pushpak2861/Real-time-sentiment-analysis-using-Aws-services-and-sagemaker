
FROM python:3.12-slim

WORKDIR /app
COPY ./streamlit_util.py /app/
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir streamlit boto3 pandas matplotlib

EXPOSE 8501 

CMD ["streamlit" , "run" , "streamlit_util.py" , "--server.port=8501" , "--server.address=0.0.0.0"]
