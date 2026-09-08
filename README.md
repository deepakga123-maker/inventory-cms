# Inventory & Content Management System

A Django-based inventory and catalogue management system using PostgreSQL.

## Features

- PostgreSQL database
- Product and inventory management
- Nested drag-and-drop product categories
- Bulk inventory updates through Django admin
- Low-stock alerts and stock-status filtering
- Product catalogue pages
- Pagination
- PostgreSQL full-text search across product names, SKUs and descriptions
- Hierarchical category search
- Product and category detail pages
- Automated unit and view tests
- 90% test coverage

## Technology Stack

- Python 3.13
- Django 6.1
- PostgreSQL 17
- django-treebeard
- psycopg
- Coverage.py
- Django Templates

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/deepakga123-maker/inventory-cms.git
cd inventory-cms
```

### 2. Create and activate a virtual environment

On Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install django psycopg django-treebeard coverage
```

### 4. Create the PostgreSQL database

Open PostgreSQL and create the database and user:

```sql
CREATE DATABASE inventory_cms;

CREATE USER inventory_user WITH PASSWORD 'your_password';

ALTER DATABASE inventory_cms OWNER TO inventory_user;
```

For running Django tests, allow the user to create temporary test databases:

```sql
ALTER USER inventory_user CREATEDB;
```

### 5. Configure environment variables

On Windows PowerShell:

```powershell
setx DB_PASSWORD "your_database_password"
setx DJANGO_SECRET_KEY "your_secret_key"
setx DJANGO_DEBUG "True"
setx DJANGO_ALLOWED_HOSTS "127.0.0.1,localhost"
```

After running these commands, close the terminal and open a new one.

Do not commit real passwords or secret keys to Git.

### 6. Run migrations

```powershell
.\.venv\Scripts\python.exe manage.py migrate
```

### 7. Create an admin account

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

### 8. Start the development server

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

Django admin:

```text
http://127.0.0.1:8000/admin/
```

## Testing

Run the automated test suite with:

```powershell
.\.venv\Scripts\python.exe manage.py test products
```

The project currently includes tests for:

- Product model behaviour
- Stock status logic
- Product catalogue pages
- Product detail pages
- Category detail pages
- PostgreSQL full-text search
- Hierarchical category search

## Test Coverage

Run the tests with coverage enabled:

```powershell
.\.venv\Scripts\python.exe -m coverage run manage.py test products
```

View the coverage report:

```powershell
.\.venv\Scripts\python.exe -m coverage report
```

Current overall test coverage: **90%**, exceeding the required minimum of 80%.

## Deployment

The application can be deployed on a Linux server using PostgreSQL, Gunicorn and Nginx.

### 1. Install server dependencies

Install Python, PostgreSQL, Nginx and the required system packages on the Linux server.

Create a virtual environment and install the project dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install django psycopg django-treebeard coverage gunicorn
```

### 2. Configure PostgreSQL

Create the production database and database user:

```sql
CREATE DATABASE inventory_cms;
CREATE USER inventory_user WITH PASSWORD 'your_secure_password';
ALTER DATABASE inventory_cms OWNER TO inventory_user;
```

### 3. Configure environment variables

Set the database password securely on the server:

```bash
export DB_PASSWORD="your_secure_password"
```

Production secrets should be stored as environment variables and must not be committed to Git.

### 4. Run database migrations

```bash
python manage.py migrate
```

### 5. Create an administrator

```bash
python manage.py createsuperuser
```

### 6. Collect static files

```bash
python manage.py collectstatic
```

### 7. Run with Gunicorn

Example:

```bash
gunicorn config.wsgi:application
```

For production, Gunicorn should normally be managed by a system service such as `systemd`.

### 8. Configure Nginx

Configure Nginx as a reverse proxy so that incoming web requests are forwarded to Gunicorn.

Nginx should also be configured to serve static files directly.

### 9. Production settings

Before deployment:

- Set `DEBUG = False`
- Configure `ALLOWED_HOSTS`
- Keep database passwords and other secrets outside the source code
- Use HTTPS
- Use a strong production `SECRET_KEY`
- Run migrations before starting the application
- Regularly back up the PostgreSQL database