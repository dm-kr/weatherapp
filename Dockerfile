FROM python:3.12

COPY . .

RUN pip install -r requirements.txt

WORKDIR /src

CMD ["python3.12", "main.py"]