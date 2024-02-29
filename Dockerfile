# Use the official Python image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY ./ ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the Flask app to run on
EXPOSE 5000

RUN python --version
# Run app.py when the container launches
CMD ["python", "apiSqlite3.py"]
#CMD ["python api.py"]
