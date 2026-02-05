FROM python:3.10-slim
WORKDIR /src
ENV FLASK_RUN_HOST=0.0.0.0
RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
	   build-essential \
	   libssl-dev \
	   libffi-dev \
	   python3-dev \
	   cargo \
	&& rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["gunicorn", "-b", "0.0.0.0:5000", "src:create_app()"]