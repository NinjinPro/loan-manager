# LOAN MANAGER

# Project Structure

```
loan-manager/
├── README.md
├── alembic.ini
├── requirements.txt
├── run.py
├── alembic/
│   ├── README
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── notifications.py
│   └── theme.py
├── crud/
│   ├── __init__.py
│   ├── base.py
│   ├── notification.py
│   ├── person.py
│   ├── transaction.py
│   └── user.py
├── db/
│   ├── __init__.py
│   └── database.py
├── instance/
│   └── loan_manager.db
├── models/
│   ├── __init__.py
│   ├── notification.py
│   ├── person.py
│   ├── transaction.py
│   └── user.py
├── routes/
│   ├── __init__.py
│   ├── api.py
│   ├── auth.py
│   ├── main.py
│   ├── notifications.py
│   ├── person.py
│   ├── settings.py
│   └── transactions.py
├── static/
│   ├── css/
│   │   └── main.css
│   └── js/
│       ├── LoadingIndicator.js
│       ├── NotificationManager.js
│       ├── SyncManager.js
│       ├── ThemeManager.js
│       ├── app.js
│       ├── db.js
│       └── utils.js
└── templates/
    ├── auth/
    │   ├── login.html
    │   └── register.html
    ├── base.html
    ├── components/
    │   ├── loading.html
    │   └── notifications_container.html
    ├── dashboard.html
    ├── people/
    │   ├── detail.html
    │   ├── form.html
    │   └── list.html
    ├── settings.html
    └── transactions/
        ├── detail.html
        ├── form.html
        └── list.html
```

---

# Screenshots

«Screenshots will be added as development progresses.»

---

# Installation

1. Clone the repository. `git clone https://github.com/ninjinpro/loan-manager.git`
2. Navigate into the project. `cd loan-manager`
3. Create a virtual environment. `python -m venv venv`
4. Activate it:
	- Linux/macOS: ```source venv/bin/activate```
	- Windows: ```venv\Scripts\activate```
5. Install dependencies. ```pip install -r requirements.txt```
6. Create your ".env" file.
```
SECRET_KEY=your-secret-key
DATABASE_URI=sqlite:///loan_manager.db
DEBUG=True
```

7. Run database migrations. ```alembic upgrade head```
8. Start the application. ```python run.py```
9. Open your browser. ```http://localhost:8080```

---

# Configuration

Create a ".env" file in the project root.

```
SECRET_KEY=your-secret-key
DATABASE_URI=sqlite:///loan_manager.db
DEBUG=True
```

The application can easily be configured to use PostgreSQL or MySQL by updating "DATABASE_URI".

---

# Usage

1. Register an account.
2. Log in.
3. Add people you interact with financially.
4. Create transactions.
5. Choose whether the money was:
   - Money Out (you paid them)
   - Money In (they paid you)
6. View balances from the dashboard.
7. Customize your preferred application theme.
8. Continue using the application even when offline—changes will automatically synchronize once the connection is restored.

---

# API Endpoints

## People

Method	| Endpoint				| Description
--------|-----------------------|-----------------
GET		| "/api/people"			| Get all people
POST	| "/api/people"			| Create person
PUT		| "/api/people/<id>"	| Update person
DELETE	| "/api/people/<id>"	| Delete person

## Transactions

Method	| Endpoint					| Description
--------|---------------------------|-----------------
GET		| "/api/transactions"		| Get all transactions
POST	| "/api/transactions"		| Create transaction
PUT		| "/api/transactions/<id>"	| Update transaction
DELETE	| "/api/transactions/<id>"	| Delete transaction

«Swagger/OpenAPI: Not available yet.»

«Postman Collection: Planned.»

---

# Testing

Testing has not yet been implemented.

Planned additions include:

- Unit tests
- Integration tests
- API endpoint tests
- UI tests

---

# Deployment

The project is ready for deployment on platforms such as:

- Render
- Railway
- Heroku
- PythonAnyWhere

General deployment steps:

1. Configure environment variables.
2. Install dependencies.
3. Run database migrations.
4. Start the application using Gunicorn.

## Deployed Live Details

1. Link: [link](https://ninjinpro.pythonanywhere.com/)
2. Login credintials:
    - username: `user`
    - password: `user@123`

---

# Roadmap

Planned improvements include:

- Email verification
- Password reset
- Recurring transactions
- Excel export
- PDF export
- Financial reports and charts
- Progressive Web App (PWA)
- Service Worker support
- Automated testing
- Shared accounts with role-based permissions

---

# Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open an Issue if needed.
5. Submit a Pull Request.

Please:

- Follow PEP 8.
- Keep JavaScript clean and modular.
- Add tests where applicable.
- Document new features.

---

#️ Known Limitations

- Offline synchronization currently uses sequential replay with basic conflict resolution.
- Automated tests have not yet been implemented.
- The application is still an MVP and not production-hardened.
- SQLite is the default database; PostgreSQL is recommended for production.
- Email verification is not yet available.

---

# License

This project is licensed under the MIT License.

---

# Author

- Name: NIYIGENA Gracieux
- GitHub: [@ninjinpro](https://github.com/ninjinpro)
- LinkedIn: [niyigena-gracieux](https://linkedin.com/in/niyigena-gracieux)
- Email: [gracieuxdevelop@gmail.com](mailto:gracieuxdevelop@gmail.com)

---

# Acknowledgements

Special thanks to the amazing open-source community and the projects that made this application possible.

- Flask
- SQLAlchemy
- Bootstrap
- Bootstrap Icons
- Alembic
- Werkzeug
- Python Community

---

# Inspiration

This project was inspired by the need for a simple, intuitive way to track personal loans without forcing people into permanent creditor or debtor roles.

It is actively maintained and will continue to evolve as new features are added.