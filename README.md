# Pantry Pal

PantryPal is a an application that provides users the ability to find recipes based on the ingredients already in their pantry. Users will be able to enter ingredients into the search bar and find recipes based on those ingredients. Additionally, after trying those recipes a user will be able to provide a rating for others to view.

<br>

## Technologies
- **Python:** Programming language used for the backend
- **Django:** Framework used for building this application
- **SQLite:** Default database used during development
  - PostgreSQL or another database can easily be used for production
- **HTML/CSS/JS:** Styling and interactivity

<br>

## Local Set Up
### 1. Clone Repository
```
git clone https://github.com/SyncMyShip/PantryPal

cd recipe_app
```

### 2. Create Virtual Environment
```
python -m venv .venv

source venv/bin/activate
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```

### 4. Run Migrations
```
python manage.py makemigrations

python manage.py migrate
```

### 5. Create Super User
```
python manage.py createsuperuser
```

### 6. Run Development Server
```
python manage.py runserver
```

### 7. Access Application
Open browser and navigate to ```http://127.0.0.1:8000```

<br>

## Notes
This repository is a work in progress and contributions are always welcome. If you have suggestions for improvements or new features, please create an issue or submit a pull request.

1. Fork the repo
2. Create a new branch ```git checkout -b feature-branch```
3. Make you changes
4. Commit your changes ```git commit -m 'commit message'```
5. Push to the branch ```git push origin feature-branch```
6. Open your pull request

