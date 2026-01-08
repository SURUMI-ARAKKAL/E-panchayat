# Panchayat Survey System

A modern web application for Panchayat government to conduct surveys and collect responses from citizens.

## Features

### Admin Dashboard
- Create and manage surveys with multiple question types
- View survey responses
- Add new users (admin or regular users)
- Post news and announcements
- View statistics (total surveys, responses, users)

### User Dashboard
- View available surveys
- Submit survey responses
- View latest news and announcements
- Track completed surveys

## Technology Stack

- **Backend**: Python Django
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (default, can be changed to PostgreSQL/MySQL)
- **UI Theme**: Modern design with Panchayat green color scheme

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create Superuser (Admin)**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin account.

4. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

5. **Access the Application**
   - Open your browser and go to: `http://127.0.0.1:8000/`
   - Login with the superuser credentials you created

## Default Admin Account

After creating a superuser, you can:
- Login at `/login/`
- Access admin dashboard at `/admin-dashboard/`
- Create surveys, add users, and post news

## User Roles

### Admin Users
- Can create surveys
- Can view all survey responses
- Can add new users
- Can post news/announcements
- Access to admin dashboard

### Regular Users
- Can view and submit surveys
- Can view news/announcements
- Access to user dashboard

## Survey Question Types

When creating a survey, you can add questions with the following types:
- **Text Input**: Single line text
- **Long Text**: Multi-line text area
- **Multiple Choice (Single)**: Radio buttons (one selection)
- **Multiple Choice (Multiple)**: Checkboxes (multiple selections)
- **Number**: Numeric input
- **Date**: Date picker

## Project Structure

```
panchayat_survey/
├── manage.py
├── requirements.txt
├── panchayat_survey/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── survey_app/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── templatetags/
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── admin_dashboard.html
│   ├── user_dashboard.html
│   ├── create_survey.html
│   ├── view_survey.html
│   ├── survey_responses.html
│   ├── add_user.html
│   └── add_news.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

## Usage Guide

### For Admins

1. **Create a Survey**
   - Go to Admin Dashboard
   - Click "Create Survey"
   - Enter title and description
   - Add questions using the question builder
   - Click "Create Survey"

2. **View Responses**
   - Go to Admin Dashboard
   - Click "View Responses" on any survey
   - See all user responses

3. **Add Users**
   - Go to Admin Dashboard
   - Click "Add User"
   - Fill in user details
   - Check "Admin User" if you want to give admin privileges

4. **Post News**
   - Go to Admin Dashboard
   - Click "Add News"
   - Enter title and content
   - News will appear on user dashboard

### For Users

1. **Take a Survey**
   - Login to your account
   - View available surveys on dashboard
   - Click "Take Survey"
   - Answer all questions
   - Submit the survey

2. **View News**
   - Latest news and announcements appear on the dashboard

## Color Scheme

The application uses a Panchayat green theme:
- **Primary Green**: #2d8659
- **Light Green**: #4a9d7a
- **Dark Green**: #1f5d3f
- **White**: #ffffff
- **Black**: #1a1a1a

## Security Notes

- Change the `SECRET_KEY` in `settings.py` before deploying to production
- Set `DEBUG = False` in production
- Use a proper database (PostgreSQL/MySQL) for production
- Implement proper authentication and authorization
- Use HTTPS in production

## License

This project is created for Panchayat government use.

## Support

For issues or questions, please contact the development team.

