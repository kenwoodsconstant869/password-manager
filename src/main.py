"""
Point d'entrée principal du projet.

Lance le serveur API avec waitress. Utilisation :
    python -m src.main
"""

import os
import sys

from waitress import serve

from src.infrastructure.api.app import app


def main() -> None:
    if not os.environ.get("ENCRYPTION_KEY"):
        print(
            "ERREUR : la variable d'environnement ENCRYPTION_KEY n'est pas définie.\n"
            "Génère-en une avec :\n"
            "  python -c \"from src.infrastructure.security.fernet_encryption_service "
            "import FernetEncryptionService; print(FernetEncryptionService.generate_key().decode())\"\n"
            "Puis exporte-la (PowerShell) :\n"
            "  $env:ENCRYPTION_KEY=\"ta_cle_ici\""
        )
        sys.exit(1)

    print("Démarrage du serveur sur http://localhost:8000 ...")
    serve(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()