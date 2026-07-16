"""
Point d'entrée principal du projet.

Lance une interface locale en ligne de commande.
Utilisation :
    python -m src.main register alice correcthorsebatterystaple
    python -m src.main add GitHub alice Secr3t123 correcthorsebatterystaple
    python -m src.main list correcthorsebatterystaple
"""

import sys

from src.infrastructure.cli import PasswordManagerCLI


def main() -> None:
    cli = PasswordManagerCLI()
    result = cli.dispatch(sys.argv[1:])
    if isinstance(result, list):
        for item in result:
            print(item)
    else:
        print(result)


if __name__ == "__main__":
    main()
