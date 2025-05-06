# DDS Project
## Клонирование и установка

```powershell
git clone https://github.com/wiut00012803/ITsolutions.git dds_project
cd dds_project
python -m venv venv
.venv\Scripts\activate
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser
# введите логин, email и пароль

python manage.py runserver
```

Фронтенд для пользователей: http://127.0.0.1:8000/

Django-admin: http://127.0.0.1:8000/admin 

REST API: http://127.0.0.1:8000/api/
