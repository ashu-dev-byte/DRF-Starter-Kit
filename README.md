# BACKEND Project Setup Guide

## Overview

This guide provides instructions for setting up a Django project with PostgreSQL. The project includes essential features like virtual environment setup, dependency installation, PostgreSQL configuration, and VS Code setup.
It also comes with built-in authentication, a structured file layout for admin, views, serializers, models, and URL structure, and pre-configured settings to streamline your development process.

## Prerequisites

-   **Python**: Ensure Python is installed on your system. [Download Python](https://www.python.org/downloads/)
-   **PostgreSQL**: Install PostgreSQL for the database. [Download PostgreSQL](https://www.postgresql.org/download/)
-   **VSCode**: Install [Visual Studio Code](https://code.visualstudio.com/)
-   **VSCode Extensions**:
    -   **Python**: For Python development
    -   **Black Formatter**: For code formatting

## Setup Instructions

### 1. Create and Activate Virtual Environment

1. **Create a virtual environment**:

    Open your terminal or command prompt and run:

    ```bash
    python -m venv .venv
    ```

2. **Activate the virtual environment**:

    - **On Unix-like systems (Linux, macOS)**:

        ```bash
        source .venv/bin/activate
        ```

    - **On Windows**:

        ```cmd
        .venv\Scripts\activate
        ```

    You should see `(venv)` at the beginning of your command line prompt indicating that the virtual environment is active.

### 2. Clone the Repository

Clone the project repository to your local machine:

```bash
git clone <repository-url>
cd <repository-directory>
```

Replace `<repository-url>` with the actual repository URL and `<repository-directory>` with the directory name where the repository is cloned.

### 3. Install Project Dependencies

With the virtual environment activated, install the project dependencies:

```bash
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL

1. **Switch to the PostgreSQL user**:

    ```bash
    sudo su - postgres
    ```

2. **Access the PostgreSQL prompt**:

    ```bash
    psql
    ```

3. **Run the following commands in the PostgreSQL prompt**:

    ```sql
    CREATE DATABASE drf;
    CREATE USER drf_user WITH PASSWORD 'password';
    GRANT ALL PRIVILEGES ON DATABASE drf TO drf_user;
    ALTER USER drf_user superuser;
    ```

    Replace `drf`, `drf_user`, and `password` with your desired database name, username, and password. Make the same changes in the `.env` file as well.

### 5. Run Migrations and Start the Server

1. **Generate database migrations (Optional)**:
   Run this only when you have made changes to the models or added a migration manually.

    ```bash
    npm run migrate
    ```

2. **Run database migrations**:

    ```bash
    npm run migrations
    ```

3. **Create a superuser**:

    ```bash
    npm run create:superuser
    ```

4. **Start the Django development server**:

    ```bash
    npm run server
    ```

    Alternatively, you can start the server directly with:

    ```bash
    python manage.py runserver 15000
    ```

## Project and App Information

-   **Project Name**: `DRF_Starter_Kit`
-   **App Name**: `foundation`

## Project Features

-   **Virtual Environment Setup**: Preconfigured virtual environment to manage dependencies.
-   **Dependency Installation**: Automatically install necessary packages via `requirements.txt`.
-   **PostgreSQL Configuration**: Includes steps to set up PostgreSQL database and user.
-   **VS Code Setup**: Instructions for configuring VS Code with essential extensions.
-   **Authentication**: Built-in authentication with a custom user model extending `BaseUser` and `BaseUserManager`.
-   **Structured File Layout**: Pre-organized files for admin, views, serializers, models, and URL structure.
-   **Preconfigured Settings**: Settings are already configured to simplify setup.
-   **Middleware Logging**: Logs the number of queries executed and the total time taken for each request. Note: Does not support multi-database configurations.

## Additional Notes

-   Make sure your `.env` file and Django settings are correctly configured for your environment.

## Troubleshooting

-   If you encounter issues with environment variables, ensure your `.env` file is correctly configured and loaded.
-   For `django-environ` issues, make sure it is installed in your virtual environment and that your IDE is using the correct interpreter.
