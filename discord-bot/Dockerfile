FROM python:latest

# Create /app directory to store all the code files
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Set work directory to /app/src
WORKDIR /app/src
COPY src ./

CMD ["python3", "main.py"]
