# Libre Health GSOC-Backend
Django Rest Backend for serving Tensorflow models for **Libre Health**

*Installation process*

**after activating the virtual environment**

`cd libre_health`

`pip install -r requirements.txt`

`python manage.py runserver`

Curl command for the api endpoint:

curl --location --request POST 'http://127.0.0.1:8000/api/xray' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--form 'image=@[image_location]'

**GUI DEMO URL**
https://singhkislay.github.io/GSOC-Backend/
