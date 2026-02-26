#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de vérification d'initialisation de la base de données.
Vérifie si les tables nécessaires existent avant d'appliquer les migrations.
"""

import sys
import os
from sqlalchemy import inspect, text
from sqlalchemy.exc import OperationalError, ProgrammingError

# Ajouter le chemin du projet
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.database.session import engine
from app.models.user import User
from app.models.video import GeneratedVideo


def check_database_initialized():
    """
    Vérifie si la base de données a déjà été initialisée.
    Retourne True si les tables principales existent, False sinon.
    """
    try:
        # Créer un inspecteur pour examiner la base de données
        inspector = inspect(engine)

        # Vérifier si les tables principales existent
        existing_tables = inspector.get_table_names()

        # Tables requises
        required_tables = [User.__tablename__, GeneratedVideo.__tablename__]

        # Vérifier si toutes les tables requises existent
        missing_tables = [
            table for table in required_tables if table not in existing_tables
        ]

        if missing_tables:
            print(f"Tables manquantes: {missing_tables}")
            return False

        print("Base de données déjà initialisée.")
        return True

    except (OperationalError, ProgrammingError) as e:
        print(f"Erreur de connexion à la base de données: {e}")
        return False
    except Exception as e:
        print(f"Erreur inattendue: {e}")
        return False


def check_alembic_version():
    """
    Vérifie si la table alembic_version existe.
    Retourne True si elle existe, False sinon.
    """
    try:
        with engine.connect() as connection:
            # Vérifier si la table alembic_version existe
            result = connection.execute(
                text(
                    "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'alembic_version')"
                )
            )
            exists = result.scalar()
            return exists
    except Exception as e:
        print(f"Erreur lors de la vérification de la table alembic_version: {e}")
        return False


def main():
    """Fonction principale."""
    print("Vérification de l'initialisation de la base de données...")

    # Vérifier si la base de données est initialisée
    is_initialized = check_database_initialized()

    # Vérifier si la table alembic_version existe
    has_alembic_version = check_alembic_version()

    print(f"Base de données initialisée: {is_initialized}")
    print(f"Table alembic_version existante: {has_alembic_version}")

    # Déterminer l'état global
    if is_initialized and has_alembic_version:
        print("La base de données est complètement initialisée.")
        sys.exit(0)  # Tout est bon
    elif not is_initialized and not has_alembic_version:
        print("La base de données n'est pas du tout initialisée.")
        sys.exit(1)  # Nécessite une initialisation complète
    else:
        print("État partiel détecté. Nécessite une vérification manuelle.")
        sys.exit(2)  # État incohérent


if __name__ == "__main__":
    main()
