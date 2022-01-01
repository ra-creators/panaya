# Panaya

## Process to install

1. Create a new virtual environment by using the following command:

   `python3 -m venv venv`

2. Activate virtual environment by using the following command:

   `source venv/bin/activate` (for Linux)

   `venv\Scripts\activate` (for Windows)

3. Install the required packages by using the following command:

   `pip install -r requirements.txt`

## TODOS :

### Shop :

- [ ] pagination
- [ ] short vs long description
- [ ] dont let cart go above stock
- [ ] buy now
- [ ] ?per product Q&A

### Cart :

### Order :

### RazorPay integration :

- [X]

# Notes :

## file structure of "settings_secrets.py"

# email settings

```
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = "<mail>"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = "<password>"
```
