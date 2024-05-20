# Troubleshooting API
Manual troubleshooting test

## Prerequisites
- Docker
- Python 3.8+

## Setup Instructions

1. Clone the repository:
    ```bash
    git clone https://github.com/GenghuiQu/troubleshooting_api.git
    cd troubleshooting_api
    ```

2. Build the Docker image:
    ```bash
    docker build -t troubleshooting_api .
    ```

3. Run the Docker container:
    ```bash
    docker run -p 5000:5000 -v C:\path\to\your\logs:/app/logs troubleshooting_api
    ```

4. Test the API using Postman or curl:
    ```bash
    curl -F "file=@/path/to/your/file.pdf" http://localhost:5000/upload
    ```
