# Portfolio Backend - Django REST API

Backend API REST per il portfolio informatico costruito con Django e Django REST Framework.

## Caratteristiche

- **API REST** completa per progetti, blog e messaggi di contatto
- **Autenticazione JWT** per l'accesso all'area admin
- **Database MySQL** per la persistenza dei dati
- **CORS abilitato** per comunicare con il frontend React
- **Modelli Django** ben strutturati e scalabili

## Requisiti

- Python 3.8+
- MySQL 5.7+
- pip

## Installazione

### 1. Clonare il repository e entrare nella cartella

```bash
cd portfolio-backend
```

### 2. Creare un ambiente virtuale

```bash
python3 -m venv venv
source venv/bin/activate  # Su Windows: venv\Scripts\activate
```

### 3. Installare le dipendenze

```bash
pip install -r requirements.txt
```

### 4. Configurare le variabili d'ambiente

Copiare il file `.env.example` in `.env` e configurare i valori:

```bash
cp .env.example .env
```

Modificare `.env` con i tuoi valori:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

DB_ENGINE=django.db.backends.mysql
DB_NAME=portfolio_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306

JWT_SECRET=your-jwt-secret
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

### 5. Creare il database

```bash
mysql -u root -p -e "CREATE DATABASE portfolio_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

### 6. Eseguire le migrazioni

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Creare un utente admin

```bash
python manage.py createsuperuser
```

### 8. Avviare il server di sviluppo

```bash
python manage.py runserver
```

Il server sarà disponibile su `http://localhost:8000`

## Endpoints API

### Autenticazione

- `POST /api/auth/login/` - Login con username e password
- `POST /api/auth/register/` - Registrazione nuovo utente
- `GET /api/auth/me/` - Dati dell'utente autenticato

### Progetti

- `GET /api/projects/` - Lista di tutti i progetti
- `GET /api/projects/{id}/` - Dettagli di un progetto
- `POST /api/projects/` - Creare un nuovo progetto (richiede autenticazione)
- `PUT /api/projects/{id}/` - Modificare un progetto (richiede autenticazione)
- `DELETE /api/projects/{id}/` - Eliminare un progetto (richiede autenticazione)
- `GET /api/projects/featured/` - Progetti in evidenza
- `GET /api/projects/by_category/?category=hardware` - Progetti per categoria

### Blog

- `GET /api/blog/` - Lista di articoli pubblicati
- `GET /api/blog/{slug}/` - Dettagli di un articolo
- `POST /api/blog/` - Creare un nuovo articolo (richiede autenticazione)
- `PUT /api/blog/{slug}/` - Modificare un articolo (richiede autenticazione)
- `DELETE /api/blog/{slug}/` - Eliminare un articolo (richiede autenticazione)
- `GET /api/blog/recent/?limit=5` - Ultimi articoli pubblicati

### Contatti

- `POST /api/contact/` - Inviare un messaggio di contatto
- `GET /api/contact/` - Lista messaggi (richiede autenticazione)
- `POST /api/contact/mark_as_read/` - Segnare messaggi come letti (richiede autenticazione)
- `DELETE /api/contact/{id}/` - Eliminare un messaggio (richiede autenticazione)

## Autenticazione

L'API utilizza JWT (JSON Web Tokens) per l'autenticazione. Per accedere agli endpoint protetti:

1. Effettuare il login a `/api/auth/login/` con username e password
2. Ricevere un token JWT nella risposta
3. Includere il token nell'header `Authorization: Bearer <token>` per le richieste successive

## Admin Panel

Accedere al pannello di amministrazione Django su `http://localhost:8000/admin/` con le credenziali create durante `createsuperuser`.

## Deployment

Per il deployment su un server VPS con Apache:

1. Installare Gunicorn: `pip install gunicorn`
2. Configurare Apache come reverse proxy
3. Usare Systemd per gestire il servizio Django
4. Configurare SSL/HTTPS con Let's Encrypt

Vedi `DEPLOYMENT_GUIDE.md` per istruzioni dettagliate.

## Struttura del Progetto

```
portfolio-backend/
├── api/
│   ├── models.py          # Modelli del database
│   ├── views.py           # ViewSet API
│   ├── serializers.py     # Serializzatori DRF
│   ├── auth.py            # Autenticazione JWT
│   ├── urls.py            # URL routing
│   └── admin.py           # Configurazione admin
├── portfolio_api/
│   ├── settings.py        # Configurazione Django
│   ├── urls.py            # URL principali
│   └── wsgi.py            # WSGI application
├── manage.py              # Django management
├── requirements.txt       # Dipendenze Python
└── .env.example          # Esempio variabili d'ambiente
```

## Troubleshooting

### Errore di connessione al database

Verificare che MySQL sia in esecuzione e che le credenziali nel file `.env` siano corrette.

### Errore di permessi su file

```bash
chmod -R 755 portfolio-backend
```

### Reimpostare il database

```bash
python manage.py flush
python manage.py migrate
```

## Supporto

Per domande o problemi, consultare la documentazione ufficiale:
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PyJWT Documentation](https://pyjwt.readthedocs.io/)
