FROM selenium/standalone-chrome:latest

# Install necessary Python dependencies
RUN pip install selenium boto3

# Copy your Lambda function code
Copy solo/automatic_translation.py /solo/automatic_translation.py
COPY solo/app.py /solo/app.py

CMD ["python", "/app/app.py"]