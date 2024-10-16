# Django REST API for Warehouse Management System

This API, built with Django REST Framework, provides a comprehensive solution for managing a warehouse. It allows for seamless product management, order handling, managing stocks and...


## Prerequisites
Before setting up the project, ensure that you have the following installed:

- Python 3.11
- Django 5.1 or higher
- Django REST Framework
- Virtualenv (optional but recommended)


## Installation

To set up the project on your local machine, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mohammd-1819/warehousing_api.git


2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate


3. **Install the required dependencies:**
   ```bash
    pip install -r requirements.txt


4. **Apply the migrations:**
   ```bash
    python manage.py migrate


5. **Create a superuser for the admin panel (optional but recommended):**
   ```bash
    python manage.py createsuperuser
    default is: admin@gmail.com
    password : admin


6. **Run the development server:**
    ```bash
    python manage.py runserver


7. **Access the application:**
    Open your browser and go to http://127.0.0.1:8000/ for the main page

## Features
- Add, edit, and remove products
- Order Creation
- API endpoints for managing products, categories, orders, and users
- Pagination for datasets

## Usage
After the server is running, users can:

- View and manage products
- Place orders for items in stock
- Administrators can add, edit, and delete products, and manage orders from the admin interface.

## Managing Products

- Only authorized admin users can create and manage new products. Each product has attributes such as price, description, and categories.

## Technologies Used
- Backend: Django REST Framework
- Database: PostgreSQL
- Authentication: Customized Django built-in authentication system

## Authors
Developed by Mohammad Charipour For more details, visit:
- https://github.com/mohammd-1819
