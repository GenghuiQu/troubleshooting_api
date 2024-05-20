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

2. Configure the OpenAI API Key:
    - Open the `app.py` file.
    - Locate the following line:
		```python
		api_key = 'your_openai_api_key'  # Replace with your OpenAI API key
		```
    - Replace `'your_openai_api_key'` with your actual OpenAI API key, for example:
		```python
		api_key = 'sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'  # Your actual OpenAI API key
		```

3. Build the Docker image:
    ```bash
    docker build -t troubleshooting_api .
    ```

4. Run the Docker container:
    ```bash
    docker run -p 5000:5000 -v C:\path\to\your\logs:/app/logs troubleshooting_api
    ```

5. Test the API using Postman or curl:
    ```bash
    curl -F "file=@/path/to/your/file.pdf" http://localhost:5000/upload
    ```
	
## Viewing Logs

Logs are stored locally in the directory you specified when running the Docker container. For example, if you used `-v C:\path\to\your\logs:/app/logs`, the logs will be saved in `C:\path\to\your\logs`.

To view logs:

1. Open the log file using any text editor or use the following command to view the logs:
   ```bash
   cat C:\path\to\your\logs\app.log
   tail -f C:\path\to\your\logs\app.log  # Real-time log viewing
