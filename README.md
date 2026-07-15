password-manager/
├── README.md
├── requirements.txt
│
└── src/
    ├── domain/                    ← déjà fait
    │   ├── entities/
    │   │   ├── credential.py
    │   │   └── user.py
    │   └── exceptions/
    │       ├── credential_exceptions.py
    │       └── user_exceptions.py
    │
    ├── application/                ← à ajouter
    │   ├── interfaces/
    │   │   ├── credential_repository.py
    │   │   ├── user_repository.py
    │   │   └── encryption_service.py
    │   └── use_cases/
    │       ├── create_credential.py
    │       ├── list_credentials.py
    │       ├── update_credential.py
    │       ├── delete_credential.py
    │       ├── register_user.py
    │       └── authenticate_user.py
    │
    ├── adapters/                   ← à ajouter
    │   ├── repositories/
    │   │   ├── sqlite_credential_repository.py
    │   │   └── sqlite_user_repository.py
    │   ├── presenters/
    │   │   └── credential_presenter.py
    │   └── controllers/
    │       └── credential_resource.py
    │
    └── infrastructure/              ← à ajouter
        ├── security/
        │   └── fernet_encryption_service.py
        ├── db/
        │   └── connection.py
        └── api/
            └── app.py# password-manager