# CarePoint — Online Pharmacy Website

A responsive healthcare e-commerce platform built with Django, allowing users to browse medicines, manage a cart and wishlist, book doctor consultations, and upload prescriptions.

## Features

- Product categories with price and discount cards
- Add to Cart and Wishlist functionality
- Doctor consultation booking
- Prescription upload
- Search suggestions
- Fully responsive frontend integrated with a Django backend

## Tech Stack

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite

## Project Structure

```
carepoint_complete_backend_file/
├── manage.py
├── medicalproject/      # Django project settings
├── myapp/                # Main application (models, views, templates)
│   ├── templates/         # HTML templates
│   ├── static/             # CSS, JS, static assets
│   └── migrations/         # Database migrations
├── media/                 # Uploaded product images
└── db.sqlite3
```

## Setup Instructions

1. Clone the repository
   ```
   git clone https://github.com/akhil971/CarePoint-Online-Pharmacy-Website-.git
   cd CarePoint-Online-Pharmacy-Website-
   ```

2. Create and activate a virtual environment
   ```
   python -m venv env
   env\Scripts\activate      # Windows
   source env/bin/activate   # macOS/Linux
   ```

3. Install dependencies
   ```
   pip install django
   ```

4. Run migrations
   ```
   python manage.py migrate
   ```

5. Start the development server
   ```
   python manage.py runserver
   ```

## Author

**Akhil Kumar**
BCA Student | Aspiring Software Developer
[GitHub](https://github.com/akhil971) | [LinkedIn](https://linkedin.com/in/akhil-kumar-053510366)

*This project was implemented under mentor guidance as part of academic coursework.*
