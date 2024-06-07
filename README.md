## HTTP Get All 

This Python script helps you download files and entire folder structures from a networked machine running a simple HTTP server to another machine.

**Requirements:**

* Python 3 (tested on Python 3.11)

**How to Use:**

1.  **Start the HTTP Server:**

    On the machine containing the files you want to download, run the following command:

    ```bash
    python -m http.server
    ```

    This will start a simple HTTP server on port 8000 by default. You can specify a different port by adding `<port number>` after `http.server`:

    ```bash
    python -m http.server 8080  # Starts server on port 8080
    ```

    **Note:** Replace `8000` or your chosen port number with the actual port used by the server.

2.  **Run the Downloader Script:**

    On the machine you want to download the files to, navigate to the directory containing the script (`main.py`) and run the following command:

    ```bash
    python main.py -u http://<MACHINE_IP>:<PORT>/<FOLDER_PATH> -d <DESTINATION_FOLDER>
    ```

    **Replace the placeholders with your information:**

    * `<MACHINE_IP>`: The IP address of the machine running the HTTP server.
    * `<PORT>`: The port number used by the HTTP server (default is 8000 if not specified).
    * `<FOLDER_PATH>`: The path to the folder you want to download on the HTTP server (relative path from the server's root directory).
    * `<DESTINATION_FOLDER>`: The path to the folder where you want to save the downloaded files and recreate the folder structure.

**Example:**

```bash
python main.py -u http://192.168.1.10:8080/documents/ -d C:/Users/JohnDoe/Downloads/
```