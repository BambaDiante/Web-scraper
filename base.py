#ce code la est le code me permmetant de me connecter et d'executer les requetes voulues vers ma base de donnees
from flask import redirect,url_for
import sqlite3
from flask import jsonify
def get_category():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table'
        AND name NOT LIKE 'sqlite_%';
    """)

    categories = [row[0] for row in cursor.fetchall()]

    connection.close()
    return categories

def get_product(produit, categories):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    resultats = []

    if categories:
        for cat in categories:
            requete = f"SELECT * FROM {cat} WHERE titre LIKE ?;"
            cursor.execute(requete, (f"%{produit}%",))
            lignes = cursor.fetchall()

            for ligne in lignes:
                produit_dict = {
                    'id': ligne[0],
                    'source': ligne[1],
                    'categorie': ligne[2],
                    'titre': ligne[3],
                    'prix': ligne[4],
                    'lien': ligne[5],
                }
                resultats.append(produit_dict)

        connection.close()
        return resultats

    connection.close()
    return []
def get_cat_from_source(source,category):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    requete = f"SELECT * FROM {category} WHERE source LIKE ?;"
    try:
        cursor.execute(requete, (f"%{source}%",))
        lignes = cursor.fetchall()
        resultats=[]
        for ligne in lignes:
            produit_dict = {
                'id': ligne[0],
                'source': ligne[1],
                'categorie': ligne[2],
                'titre': ligne[3],
                'prix': ligne[4],
                'lien': ligne[5],
            }
            resultats.append(produit_dict)
        connection.close()
        return resultats
    except Exception as e:
        print(f"Erreur :{e}")
        connection.close()
        return []
def compare(nom_produit):
    print("fonction compare")
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    categories = get_category()
    resultats = []
    try:

        for category in categories:
           requete=f"SELECT * FROM {category} WHERE titre LIKE ? ORDER BY prix DESC;"
           cursor.execute(requete, (f"%{nom_produit}%",))
           lignes = cursor.fetchall()

           for ligne in lignes:
               produit_dict = {
                   'id': ligne[0],
                   'source': ligne[1],
                   'categorie': ligne[2],
                   'titre': ligne[3],
                   'prix': ligne[4],
                   'lien': ligne[5],
               }
               resultats.append(produit_dict)
           return resultats
    except Exception as e:
        print(" produit introuvable")
        print(f"Erreur :{e}")
        connection.close()
        return []


def enregister(nom, mail, adresse, date, numero,password):
    try:
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        #creation de la table
        cursor.execute("""
           CREATE TABLE IF NOT EXISTS utilisateurs
               (
                   id      INTEGER PRIMARY KEY AUTOINCREMENT,
                   nom     VARCHAR NOT NULL,
                   mail    VARCHAR NOT NULL,
                   adresse VARCHAR NOT NULL,
                   password VARCHAR NOT NULL,
                   date    DATE NOT NULL,
                   numero  INTEGER NOT NULL
               )
           """)
        #insertion des donness
        cursor.execute("""
                       INSERT INTO utilisateurs (nom, mail, adresse, date, numero,password)
                       VALUES (?, ?, ?, ?, ?,?)
                       """,
                       (nom, mail, adresse, date, numero,password)
                       )


        connection.commit()

        print("Utilisateur enregistré avec succès !")
        redirect(url_for('template', filename='homepage.html'))

    except Exception as e:
        print(f"Erreur lors de l'enregistrement : {e}")
    finally:
        connection.close()
