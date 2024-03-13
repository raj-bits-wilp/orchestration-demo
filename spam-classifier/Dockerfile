FROM ubuntu:20.04
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && \
    apt-get install -y python3 python3-pip

# Display Python and pip versions
RUN python3 --version && \
    pip3 --version

RUN apt-get update && apt-get install -y sudo && rm -rf /var/lib/apt/lists/*


RUN pip install -r requirements.txt
RUN pip install fastapi uvicorn pydantic

EXPOSE 8501
COPY . /app

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

