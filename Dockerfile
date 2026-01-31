FROM python:3.10-alpine
WORKDIR /src
ENV FLASK_RUN_HOST=0.0.0.0
RUN pip install flask
EXPOSE 5000
COPY . .
CMD ["flask", "--app", "src", "run"]