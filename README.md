
# DiscoverMe API
##IMPORTANT!
When developing your issue, make sure you switch to the branch that corresponds to your issue. For example:
   ```
   git pull
   git checkout Issue-3 # This will move you to a branch dedicated to your issue so that you wont have any merge cnflicts when developing
   ```
Now you are on branch Isse-3. once that is done, commit your change, then push it.
   ```
   git add .
   git comit -m " A message"
   git push
   ```
Finally create a pull request for your issue. This is done in the GitHub Portal.
## Overview

Welcome to the DiscoverMe API repository! This API serves as the backend for the DiscoverMe project, providing mood logging, journal entry management, and mental health insights. It uses Django and Django REST Framework to create a scalable, secure API that connects with the frontend (Vue.js).

This guide will help team members with little to no experience in Django get started, create new models, and make necessary changes in the API.

## Prerequisites

Before getting started, ensure you have the following tools installed:
- **Python 3.12+**
- **pip** (Python package manager)
- **Virtualenv** (Optional but recommended)
- **PostgreSQL** (or other database, if not using SQLite)
- **Git**

### Setup Instructions

1. **Clone the Repository**

   Open a terminal and clone the API repository to your local machine:

   ```
   git clone https://github.com/your-team/discoverme-api.git
   cd discoverme-api
   ```

2. **Set Up a Virtual Environment**

   It's recommended to use a virtual environment to isolate your dependencies. You can set one up by running:

   ```
   python -m venv env
   source env/bin/activate  # For macOS/Linux
   env\Scripts\activate  # For Windows
   ```

3. **Install Dependencies**

   Install all the required dependencies using `pip`:

   ```
   pip install -r requirements.txt
   ```

4. **Set Up the Database**

   - We're using SQLite for local developement, leave the PSQL databse integration to me!

5. **Run Migrations**

   Before running, you will need to set up the initial database schema for your db file, run:

   ```
   cd discoverme_api # Switch to the project sub-repo containing the manage.py
   python manage.py makemigrations
   python manage.py migrate --run-syncdb
   ```

6. **Create a Superuser (Admin Account)**

   You’ll need an admin account to access the Django admin portal. Run the following command and follow the prompts:

   ```
   python manage.py createsuperuser
   ```

7. **Populate the database**

   You’ll need to add test data to the database by running the folowing
   ```
   python manage.py populate_data
   ```

8. **Run the Development Server**

   Start the Django development server to test locally:

   ```
   python manage.py runserver
   ```

   Open `http://127.0.0.1:8000/admin/` in your browser and log in with the superuser account.

## How to Create New Models

Models define the structure of the data in Django. Here's how you can create and manage models.

### 1. **Define a New Model**

In `base/models.py`, define your new model. For example, let’s say we want to create a `Task` model:

```python
from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Tied to a user
    title = models.CharField(max_length=255)
    description = models.TextField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
```

### 2. **Create Migrations**

Once the model is defined, create the migration file that will add the model to the database:

```bash
python manage.py makemigrations
```

### 3. **Apply Migrations**

Run the following to apply the migrations and create the table for the new model in the database:

```bash
python manage.py migrate
```

### 4. **Register the Model in Admin**

To manage the new model from the Django admin, register it in `base/admin.py`:

```python
from django.contrib import admin
from .models import Task

admin.site.register(Task)
```

### 5. **Create a Serializer for the Model**

To expose the model via the API, you need to create a serializer. Add the following in `base/serializers.py`:

```python
from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
```

### 6. **Create a View for the Model**

Now, create a viewset for the `Task` model in `base/views.py`:

```python
from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
```

### 7. **Add the URL for the View**

Finally, add the route to your API in `discoverme_api/urls.py`:

```python
from base import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet, basename='task')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
```

### Summary of Commands
- `python manage.py makemigrations`: Detect changes in models and prepare database migration files.
- `python manage.py migrate`: Apply database changes.
- `python manage.py createsuperuser`: Create an admin user to access the admin portal.

## Helpful Django Commands

- `python manage.py runserver`: Run the local development server.
- `python manage.py shell`: Open an interactive Python shell with Django.
- `python manage.py test`: Run unit tests for the project.

## Further Learning Resources

- [Django Documentation](https://docs.djangoproject.com/en/stable/)
- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

If you have any questions, feel free to reach out in the team chat!

