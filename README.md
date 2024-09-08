# **Backend Project Setup Guide**

## **Overview**

This guide provides instructions for setting up a Django project with PostgreSQL. The project includes essential features like virtual environment setup, dependency installation, PostgreSQL configuration, and VS Code setup.
It also includes built-in authentication, Swagger documentation, a structured file layout, and pre-configured settings to streamline your development process.

## **Project and App Information**

-   **Project Name**: `DRF_Starter_Kit`
-   **App Name**: `foundation`

## **Project Features**

-   **Virtual Environment Setup**: Preconfigured virtual environment for managing dependencies.
-   **Dependency Installation**: Automatically install packages via `npm run install:deps` or `pip install -r requirements.txt`.
-   **PostgreSQL Configuration**: Instructions for PostgreSQL setup on Unix-like systems and Windows.
-   **VS Code Setup**: Guide for configuring VS Code with necessary extensions.
-   **Authentication**: Built-in authentication with a custom user model.
-   **Swagger Documentation Support**: Integrated Swagger UI for API documentation and testing.
-   **Structured File Layout**: Organized files for admin, views, serializers, models, and URLs.
-   **Preconfigured Settings**: Simplified configuration to get started quickly.
-   **Middleware Logging**: Logs query counts and execution time per request (doesn't support multi-database).
-   **One-Click Project Setup**: Quick setup using `npm run setup:project` for default settings.

## **Prerequisites**

-   **Python**: Ensure Python 3.12+ is installed. [Download Python](https://www.python.org/downloads/)
-   **PostgreSQL**: Install PostgreSQL. [Download PostgreSQL](https://www.postgresql.org/download/)
    -   During installation, save the PostgreSQL superuser password for later use.
-   **Node.js**: Ensure Node.js is installed. [Download Node.js](https://nodejs.org/)
-   **npm**: Comes with Node.js, but ensure it's updated (`npm install -g npm`).
-   **VS Code**: Install [Visual Studio Code](https://code.visualstudio.com/)
-   **VS Code Extensions**:
    -   **Python**: For Python development.
    -   **Black Formatter**: For code formatting.

---

## **Clone the Repository**

To clone the project repository:

```bash
mkdir <repository-directory>
cd <repository-directory>
git clone <repository-url>
```

-   Ensure your virtual environment (`.venv`) is located in the cloned `<repository-directory>`.
-   Replace `<repository-url>` with the actual repository URL.

## **Create and Activate Virtual Environment**

1. **Create the virtual environment**:

    ```bash
    python -m venv .venv
    ```

2. **Activate the virtual environment**:

    - **On Unix-like systems**:

        ```bash
        source .venv/bin/activate
        ```

    - **On Windows**:

        ```cmd
        .venv\Scripts\activate
        ```

    You should see `(venv)` at the beginning of your command line prompt, indicating that the virtual environment is active.

## **Setup Options**

**You have two options for setting up the project. Choose only one of these options based on your preference.**

### **Option 1: Quick Setup with Default Configurations**

To quickly set up the project using default configurations, run the pre-configured management command:

```bash
npm run setup:project
```

This command will:

-   Install required Python packages.
-   Set up the PostgreSQL database with default configurations.
-   Apply database migrations.
-   Create a superuser (`admin@drf.com`/`password`), only if the server environment is in `["local", "test", "staging"]`.

After running this command, your project will be ready with the default settings.

### **Option 2: Manual Setup (Customizable)**

For more control over the project setup, follow the steps below:

#### **Additional Setup Instructions**

##### 1. **Install Project Dependencies**

With the virtual environment activated, install the project dependencies:

```bash
npm run install:deps
```

Alternatively:

```bash
pip install -r requirements.txt
```

##### 2. **Set Up PostgreSQL**

-   **On Unix-like Systems (Linux, macOS)**

    1. **Switch to the PostgreSQL user**:

        ```bash
        sudo su - postgres
        ```

    2. **Access the PostgreSQL prompt**:

        ```bash
        psql
        ```

-   **On Windows**

    1. **Run Command Prompt as Administrator**: Right-click on Command Prompt and select "Run as administrator."

    2. **Access the PostgreSQL prompt**:

        ```cmd
        psql -U postgres
        ```

-   **Run the Following SQL Commands**

    Once inside the PostgreSQL prompt, execute:

    ```sql
    CREATE DATABASE drf;
    CREATE USER drf_user WITH PASSWORD 'password';
    GRANT ALL PRIVILEGES ON DATABASE drf TO drf_user;
    ALTER USER drf_user SUPERUSER;
    ```

    -   Replace `drf`, `drf_user`, and `password` with your desired database, username, and password.
    -   Update these values in your `.env` file.

##### 3. **Running Migrations and Creating Superuser**

1. **For model changes or new migrations**:

    - **Generate migration files**:

        ```bash
        npm run makemigrations
        ```

    - **Apply database migrations**:

        ```bash
        npm run migrate
        ```

2. **Create a superuser**:

    ```bash
    npm run create:superuser
    ```

## **Running the Server and Handling Migrations**

-   To run the Django development server:

    ```bash
    npm run server
    ```

    The default port is 8000. Specify a different port if needed, e.g.:

    ```bash
    npm run server 15000
    ```

-   For database migrations, always:

    1. **Generate migration files**:

        ```bash
        npm run makemigrations
        ```

    2. **Apply the migrations**:

        ```bash
        npm run migrate
        ```

---

## **Additional Notes**

-   Ensure your `.env` file and Django settings are properly configured for your environment.

## **Troubleshooting**

-   **Environment Variables**: If issues arise, ensure your `.env` file is correctly loaded.
-   **django-environ**: Ensure it is installed in your virtual environment and that your IDE uses the correct interpreter.
-   **Windows Users**: If PostgreSQL commands fail, run the terminal as administrator.
