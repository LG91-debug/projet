from modules.gestion_produits import *
import csv 
import os
import hashlib


def verif_mdp(password):
    password_hash = hashlib.md5(password.encode()).hexdigest()  

    try:
        with open('mdp_compromis.csv', mode='r') as file:
            reader = csv.reader(file)
            # next(reader)  
            for row in reader:
                if row[0] == password_hash:
                    return True 
        return False  
    except FileNotFoundError:
        return False  





def inscription():
    id = input("Entrez votre numero d'identifiant: ")
    nom = input("Entrez votre nom: ")
    username = input("Entrez votre nom d'utilisateur: ")

    while True:
        password = input("Entrez votre mot de passe: ")
        
        if verif_mdp(password):
            print("Ce mot de passe est compromis. Veuillez en choisir un autre.")
        else:
            break  
    
    password_hash = hashlib.md5(password.encode()).hexdigest() 

    with open('data_user.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        
        file.seek(0, 2)  
        if file.tell() == 0:
            writer.writerow(["ID", "Nom", "Username", "Password"]) 
        
        writer.writerow([id, nom, username, password_hash])

    print("Inscription réussie!")


def connexion():
    username = input("Entrez votre nom d'utilisateur: ")
    password = input("Entrez votre mot de passe: ")

    with open('data_user.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Sauter l'entête du fichier CSV
        for row in reader:
            stored_username = row[2]
            stored_password = row[3]
            
            if stored_username == username and stored_password == password:
                print("Connexion réussie!")
                
                # Chemin du dossier 'data' et création de ce dossier s'il n'existe pas
                folder_path = 'data'
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                
                # Création du fichier de l'utilisateur dans le dossier 'data'
                user_filename = os.path.join(folder_path, f"{username}.csv")
                
                if not os.path.exists(user_filename):
                    with open(user_filename, mode='w', newline='') as user_file:
                        writer = csv.writer(user_file)  # Vous pouvez y écrire des données si nécessaire

                menu_user(username) 
                return  
    print("Nom d'utilisateur ou mot de passe incorrect.")

def quitter():
    print("Au revoir !")
    sys.exit()  # Termine le programme



def connexion_et_supprimer_fichier():
    # Demander le nom d'utilisateur et le mot de passe
    username = input("Entrez votre nom d'utilisateur: ")
    password = input("Entrez votre mot de passe: ")

    # Ouvrir le fichier CSV contenant les données des utilisateurs
    try:
        with open('data_user.csv', mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Passer l'en-tête
            
            # Vérifier les informations de connexion
            for row in reader:
                nom, stored_username, stored_password = row
                
                if stored_username == username and stored_password == password:
                    print("Connexion réussie!")

                    # Vérifier si le fichier correspondant à l'utilisateur existe
                    user_filename = f"{username}.csv"
                    
                    if os.path.exists(user_filename):
                        try:
                            # Supprimer le fichier de l'utilisateur
                            os.remove(user_filename)
                            print(f"Le fichier {user_filename} a été supprimé avec succès.")
                        except Exception as e:
                            print(f"Une erreur est survenue lors de la suppression du fichier: {e}")
                    else:
                        print(f"Le fichier {user_filename} n'existe pas.")
                    
                    return  # Fin de la fonction, l'utilisateur est authentifié et le fichier supprimé
                    
            print("Nom d'utilisateur ou mot de passe incorrect.")
            
    except FileNotFoundError:
        print("Le fichier 'data_user.csv' est introuvable.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")


from colorama import Fore, Style, init
from modules.auth import *

init(autoreset=True)

def menu_user(username):
    while True:  # Boucle infinie pour revenir au menu après chaque action
        print(Fore.BLUE + """
 ::::::::  :::::::::: :::::::: ::::::::::: ::::::::::: ::::::::  ::::    ::: 
:+:    :+: :+:       :+:    :+:    :+:         :+:    :+:    :+: :+:+:   :+: 
+:+        +:+       +:+           +:+         +:+    +:+    +:+ :+:+:+  +:+ 
:#:        +#++:++#  +#++:++#++    +#+         +#+    +#+    +:+ +#+ +:+ +#+ 
#+#   +#+# +#+              +#+    +#+         +#+    +#+    +#+ +#+  +#+#+# 
#+#    #+# #+#       #+#    #+#    #+#         #+#    #+#    #+# #+#   #+#+# 
 ########  ########## ########     ###     ########### ########  ###    ####
    """)

        print(Fore.LIGHTBLACK_EX + Style.BRIGHT + "==============================")
        print(Fore.MAGENTA + f"   Menu de {username}   ")  
        print(Fore.LIGHTBLACK_EX + Style.BRIGHT + "==============================")
        print()

        print(Fore.CYAN + "Que souhaitez-vous faire ?")
        print(Fore.GREEN + "1. Créer")
        print(Fore.YELLOW + "2. Supprimer")
        print(Fore.BLUE + "3. Ajouter un produit")
        print(Fore.RED + "4. Afficher")
        print(Fore.LIGHTGREEN_EX + "5. Rechercher")
        print(Fore.LIGHTYELLOW_EX + "6. Trier")
        print(Fore.LIGHTYELLOW_EX + "7. Quitter")

        print()

        choix = input(Fore.LIGHTCYAN_EX + "Entrez votre choix : ")

        if choix == '1':
            print(Fore.GREEN + Style.BRIGHT + "\nCréation en cours...")  
            create(username)
        elif choix == '2':
            print(Fore.RED + Style.BRIGHT + "\nSuppression en cours...")  
            supprimer(username)
        elif choix == '3':
            print(Fore.BLUE + Style.BRIGHT + "\nAjout de produit en cours...")  
            add_produit(username)
        elif choix == '4':
            print(Fore.RED + Style.BRIGHT + "\nAffichage en cours...") 
            afficher(username)

        elif choix == '5':
            print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "\nRecherche en cours...")  
            rechercher_sequ(username)
        elif choix == '6':
            print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "\nTri en cours...")  
            tri_bul(username)
        elif choix == '7':
            quitter()  # Quitter la fonction et le programme
        else:
            print(Fore.RED + Style.BRIGHT + "\nChoix invalide. Veuillez essayer à nouveau.")  # Erreur en rouge