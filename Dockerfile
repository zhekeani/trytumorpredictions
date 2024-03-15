FROM tensorflow/tensorflow

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app ./

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]