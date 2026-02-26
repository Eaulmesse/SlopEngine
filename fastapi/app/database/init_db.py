#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'initialisation de la base de données.
Génère et applique les migrations si nécessaire.
"""

import os
import sys
import subprocess
import time

# Ajouter le chemin du projet
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.database.check_init import check_database_initialized, check_alembic_version


def run_alembic_command(command):
    """Exécute une commande Alembic et retourne le résultat."""
    try:
        print(f"Exécution de la commande: alembic {command}")
        result = subprocess.run(
            ["alembic"] + command.split(),
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(__file__)),
        )

        if result.returncode != 0:
            print(f"Erreur lors de l'exécution de 'alembic {command}':")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            return False

        print(f"Commande réussie: {result.stdout}")
        return True

    except FileNotFoundError:
        print("Erreur: Alembic n'est pas installé ou n'est pas dans le PATH.")
        return False
    except Exception as e:
        print(f"Erreur inattendue: {e}")
        return False


def wait_for_database(max_retries=30, retry_interval=2):
    """
    Attend que la base de données soit disponible.
    Retourne True si la base de données est disponible, False sinon.
    """
    print("Attente de la disponibilité de la base de données...")

    for attempt in range(max_retries):
        try:
            # Importer ici pour éviter les erreurs d'importation circulaire
            from app.database.session import engine

            with engine.connect() as connection:
                # Test simple de connexion
                connection.execute("SELECT 1")
                print(f"Base de données disponible après {attempt + 1} tentatives.")
                return True

        except Exception as e:
            if attempt < max_retries - 1:
                print(
                    f"Tentative {attempt + 1}/{max_retries}: Base de données non disponible: {e}"
                )
                time.sleep(retry_interval)
            else:
                print(f"Échec après {max_retries} tentatives: {e}")
                return False

    return False


def initialize_database():
    """Initialise la base de données si nécessaire."""
    print("=== Initialisation de la base de données ===")

    # Attendre que la base de données soit disponible
    if not wait_for_database():
        print("Échec: Base de données non disponible.")
        return False

    # Vérifier l'état actuel
    is_initialized = check_database_initialized()
    has_alembic_version = check_alembic_version()

    print(
        f"État initial - Base initialisée: {is_initialized}, Version Alembic: {has_alembic_version}"
    )

    # Cas 1: Tout est déjà initialisé
    if is_initialized and has_alembic_version:
        print("La base de données est déjà complètement initialisée.")
        return True

    # Cas 2: Rien n'est initialisé
    if not is_initialized and not has_alembic_version:
        print("Génération de la migration initiale...")

        # Générer la migration
        if not run_alembic_command("revision --autogenerate -m 'Initial migration'"):
            print("Échec de la génération de la migration.")
            return False

        # Appliquer la migration
        if not run_alembic_command("upgrade head"):
            print("Échec de l'application de la migration.")
            return False

        print("Migration initiale appliquée avec succès.")
        return True

    # Cas 3: État incohérent (tables existent mais pas alembic_version, ou vice versa)
    print("État incohérent détecté. Tentative de réparation...")

    if is_initialized and not has_alembic_version:
        print("Tables existent mais pas la table alembic_version.")
        print("Création d'une migration factice pour synchroniser Alembic...")

        # Créer une migration factice
        if not run_alembic_command("revision -m 'Sync existing database'"):
            print("Échec de la création de la migration factice.")
            return False

        # Appliquer la migration
        if not run_alembic_command("upgrade head"):
            print("Échec de l'application de la migration factice.")
            return False

        print("Base de données synchronisée avec Alembic.")
        return True

    if not is_initialized and has_alembic_version:
        print("Table alembic_version existe mais pas les tables d'application.")
        print("Suppression de la table alembic_version et réinitialisation...")

        # Supprimer la table alembic_version
        try:
            from app.database.session import engine

            with engine.connect() as connection:
                connection.execute("DROP TABLE IF EXISTS alembic_version")
                connection.commit()
                print("Table alembic_version supprimée.")
        except Exception as e:
            print(f"Erreur lors de la suppression de alembic_version: {e}")
            return False

        # Réinitialiser complètement
        return initialize_database()

    return False


def main():
    """Fonction principale."""
    try:
        success = initialize_database()

        if success:
            print("=== Initialisation terminée avec succès ===")
            sys.exit(0)
        else:
            print("=== Échec de l'initialisation ===")
            sys.exit(1)

    except Exception as e:
        print(f"Erreur inattendue: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
