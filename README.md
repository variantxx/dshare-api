# DShare API

DShare is a platform that allows users to share PDF, PPT, and DOC files. This repository is a ***REST API*** built with Python and FastAPI.

## Requirements

- [Python 3](https://www.python.org/downloads)
- [Git](https://git-scm.com/downloads)

## Getting Started

Follow the following steps to setup the project.

1. Create a virtual environment:

    ```bash
    python -m venv .venv
    ```

2. Activate the virtual environment:

    ```bash
    # Windows
    .\venv\Scripts\activate

    # macOS / Linux
    source venv/bin/activate
    ```

3. Install all packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Get the ```.env``` file from the admin, and paste inside the root directory.

5. Run the project:

    ```bash
    # Run in localhost
    uvicorn app.main:app

    # Run on local network
    uvicorn app.main:app --host 0.0.0.0 --port 8000
    ```

## License

This project is licensed under the terms described in the [LICENSE](./LICENSE) file.
