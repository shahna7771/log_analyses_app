FROM python:3.8-slim
WORKDIR /app
COPY . /app/
RUN pip install -r requirement.txt
CMD ["python","Data_processing.py"]

