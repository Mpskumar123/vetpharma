FROM python:3.10-slim

WORKDIR /app

# Install Rust and build essentials
RUN apt-get update && apt-get install -y \
    curl build-essential gcc \
 && curl https://sh.rustup.rs -sSf | sh -s -- -y \
 && . "$HOME/.cargo/env"

 
ENV PATH="/root/.cargo/bin:${PATH}"

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
