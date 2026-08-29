import os
import sys
import socket
import platform
import random
import string
import hashlib
import base64
import time
import subprocess
import secrets
import uuid
import datetime
import json
from urllib.parse import urlparse
import requests

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

BANNER = rf"""{CYAN}
  ____  _____ __  __ 
 / ___|| ____|  \/  |
| |    |  _| | |\/| |
| |___ | |___| |  | |
 \____||_____|_|  |_|
   --- CEM Multi-Tool v3.0 ---
{RESET}"""


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input(f"\n{YELLOW}[Appuie sur Entrée pour revenir au menu...]{RESET}")


def afficher_banniere():
    print(BANNER)


def tool_ping():
    print("\n--- [ Pinger une cible ] ---")
    target = input("IP ou domaine : ").strip()
    if not target:
        print(f"{RED}[-] Erreur : aucune cible renseignée.{RESET}")
        pause()
        return
    param = "-n" if os.name == "nt" else "-c"
    commande = ["ping", param, "4", target]
    try:
        subprocess.run(commande, check=True)
    except subprocess.CalledProcessError:
        print(f"{RED}[-] La cible est injoignable ou la commande a échoué.{RESET}")
    except FileNotFoundError:
        print(f"{RED}[-] L'utilitaire 'ping' est introuvable sur le système.{RESET}")
    pause()


def tool_ip_public():
    print("\n--- [ Mon IP Publique ] ---")
    try:
        reponse = requests.get("https://api.ipify.org", timeout=5)
        print(f"{GREEN}[+] Ton IP publique : {reponse.text.strip()}{RESET}")
    except requests.exceptions.RequestException as e:
        print(f"{RED}[-] Impossible de récupérer l'IP publique : {e}{RESET}")
    pause()


def tool_local_ip():
    print("\n--- [ Mon IP Locale ] ---")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        print(f"{GREEN}[+] Ton IP locale : {ip}{RESET}")
    except Exception as e:
        print(f"{RED}[-] Erreur : {e}{RESET}")
    pause()


def tool_dns_lookup():
    print("\n--- [ Résolution DNS ] ---")
    domaine = input("Domaine (ex: google.com) : ").strip()
    try:
        ip = socket.gethostbyname(domaine)
        print(f"{GREEN}[+] Adresse IP de {domaine} : {ip}{RESET}")
    except socket.gaierror:
        print(f"{RED}[-] Domaine introuvable.{RESET}")
    pause()


def proposer_export_json(donnees, nom_fichier):
    choix = input(f"\nExporter le résultat dans {nom_fichier} ? (y/n) : ").strip().lower()
    if choix == "y":
        try:
            with open(nom_fichier, "w", encoding="utf-8") as f:
                json.dump(donnees, f, indent=4, ensure_ascii=False)
            print(f"{GREEN}[+] Résultat exporté dans {nom_fichier}{RESET}")
        except Exception as e:
            print(f"{RED}[-] Erreur lors de l'export : {e}{RESET}")


def scanner_ports(cible):
    ports = [21, 22, 80, 443, 3306, 8080]
    resultats = {}
    print(f"Scan des ports {ports} sur {cible}...\n")
    for port in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            resultat = s.connect_ex((cible, port))
            s.close()
            ouvert = resultat == 0
            resultats[port] = "OUVERT" if ouvert else "FERMÉ"
            if ouvert:
                print(f"{GREEN}[+] Port {port} : OUVERT{RESET}")
            else:
                print(f"[-] Port {port} : FERMÉ")
        except Exception as e:
            resultats[port] = f"ERREUR ({e})"
            print(f"{RED}[-] Erreur sur le port {port} : {e}{RESET}")
    return resultats


def tool_port_scanner():
    print("\n--- [ Scanner de ports ] ---")
    target = input("IP ou domaine à scanner : ").strip()
    if not target:
        print(f"{RED}[-] Erreur : aucune cible renseignée.{RESET}")
        pause()
        return
    resultats = scanner_ports(target)
    proposer_export_json({target: resultats}, "resultats_scan.json")
    pause()


def tool_http_headers():
    print("\n--- [ Vérification d'en-têtes HTTP ] ---")
    url = input("URL (ex: exemple.com) : ").strip()
    if not url:
        print(f"{RED}[-] Erreur : aucune URL renseignée.{RESET}")
        pause()
        return
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    domaine = urlparse(url).netloc
    try:
        reponse = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        infos = {
            "domaine": domaine,
            "statut": reponse.status_code,
            "serveur": reponse.headers.get("Server", "Inconnu"),
            "type_contenu": reponse.headers.get("Content-Type", "Inconnu"),
        }
        print(f"{GREEN}[+] Statut : {infos['statut']}{RESET}")
        print(f"[+] Serveur : {infos['serveur']}")
        print(f"[+] Type de contenu : {infos['type_contenu']}")
        proposer_export_json(infos, "resultats_headers.json")
    except requests.exceptions.RequestException:
        print(f"{RED}[-] La cible est hors ligne ou injoignable.{RESET}")
    pause()


def outil_base64():
    print("\n--- [ Encodage / Décodage Base64 ] ---")
    choix = input("1. Encoder | 2. Décoder -> ").strip()
    texte = input("Texte : ")
    if choix == "1":
        resultat = base64.b64encode(texte.encode()).decode()
        print(f"{GREEN}[+] Résultat : {resultat}{RESET}")
    elif choix == "2":
        try:
            resultat = base64.b64decode(texte.encode()).decode()
            print(f"{GREEN}[+] Texte clair : {resultat}{RESET}")
        except Exception:
            print(f"{RED}[-] Erreur de décodage.{RESET}")
    else:
        print(f"{RED}[-] Choix invalide.{RESET}")
    pause()


def tool_hash_sha256():
    print("\n--- [ Hash SHA-256 ] ---")
    texte = input("Texte à hasher : ")
    resultat = hashlib.sha256(texte.encode()).hexdigest()
    print(f"{GREEN}[+] Hash : {resultat}{RESET}")
    pause()


def tool_gen_key():
    print("\n--- [ Générateur de clé Hex ] ---")
    cle = secrets.token_hex(16)
    print(f"{GREEN}[+] Clé 128-bit : {cle}{RESET}")
    pause()


def tool_sys_info():
    print("\n--- [ Infos Système ] ---")
    print(f"OS : {platform.system()} {platform.release()}")
    print(f"Nom de la machine : {platform.node()}")
    print(f"Architecture : {platform.machine()}")
    print(f"Processeur : {platform.processor()}")
    print(f"Version Python : {platform.python_version()}")
    pause()


def conversion_octets():
    print("\n--- [ Convertisseur d'octets ] ---")
    try:
        nombre_octets = float(input("Entrez le nombre d'octets : "))
        ko = nombre_octets / 1000
        mo = nombre_octets / (1000 ** 2)
        go = nombre_octets / (1000 ** 3)
        print(f"\nRésultats pour {nombre_octets:.0f} octet(s) :")
        print(f"- {ko:.4f} Ko")
        print(f"- {mo:.6f} Mo")
        print(f"- {go:.9f} Go")
    except ValueError:
        print(f"{RED}[-] Veuillez entrer un nombre valide.{RESET}")
    pause()


def password_safe():
    print("\n--- [ Vérificateur de mot de passe ] ---")
    mdp = input("Entrez votre mot de passe : ")
    contient_chiffre = any(c.isdigit() for c in mdp)
    contient_majuscule = any(c.isupper() for c in mdp)
    contient_special = any(c in string.punctuation for c in mdp)
    longueur_ok = len(mdp) >= 8

    if longueur_ok and contient_chiffre and contient_majuscule and contient_special:
        print(f"{GREEN}[+] Mot de passe sécurisé.{RESET}")
    else:
        print(f"{YELLOW}[-] Mot de passe pas assez sécurisé, il manque :{RESET}")
        if not longueur_ok:
            print("  - au moins 8 caractères")
        if not contient_chiffre:
            print("  - un chiffre")
        if not contient_majuscule:
            print("  - une majuscule")
        if not contient_special:
            print("  - un caractère spécial")
    pause()


def tool_password_gen():
    print("\n--- [ Générateur de mot de passe ] ---")
    try:
        longueur = int(input("Longueur du mot de passe (min 8) : "))
        if longueur < 8:
            print(f"{RED}[-] Longueur trop courte.{RESET}")
            pause()
            return
        alphabet = string.ascii_letters + string.digits + string.punctuation
        mdp = ''.join(secrets.choice(alphabet) for _ in range(longueur))
        print(f"{GREEN}[+] Mot de passe généré : {mdp}{RESET}")
    except ValueError:
        print(f"{RED}[-] Veuillez entrer un nombre valide.{RESET}")
    pause()


def tool_weather():
    print("\n--- [ Météo ] ---")
    ville = input("Ville : ").strip()
    if not ville:
        print(f"{RED}[-] Erreur : aucune ville renseignée.{RESET}")
        pause()
        return
    try:
        reponse = requests.get(f"https://wttr.in/{ville}?format=3", timeout=5)
        print(f"{GREEN}[+] {reponse.text.strip()}{RESET}")
    except requests.exceptions.RequestException:
        print(f"{RED}[-] Erreur de récupération de la météo.{RESET}")
    pause()


def tool_uuid_gen():
    print("\n--- [ Générateur UUID ] ---")
    print(f"{GREEN}[+] UUID4 : {uuid.uuid4()}{RESET}")
    pause()


def tool_text_to_binary():
    print("\n--- [ Texte -> Binaire ] ---")
    texte = input("Texte : ")
    resultat = ' '.join(format(ord(c), '08b') for c in texte)
    print(f"{GREEN}[+] Binaire : {resultat}{RESET}")
    pause()


def tool_binary_to_text():
    print("\n--- [ Binaire -> Texte ] ---")
    bin_txt = input("Binaire (séparé par des espaces) : ").strip()
    try:
        octets = bin_txt.split()
        resultat = ''.join(chr(int(b, 2)) for b in octets)
        print(f"{GREEN}[+] Texte : {resultat}{RESET}")
    except ValueError:
        print(f"{RED}[-] Format binaire invalide.{RESET}")
    pause()


def tool_minuteur():
    print("\n--- [ Minuteur ] ---")
    try:
        secondes = int(input("Temps en secondes : "))
        print("Démarrage...")
        while secondes > 0:
            mins, secs = divmod(secondes, 60)
            print(f"{mins:02d}:{secs:02d}", end="\r")
            time.sleep(1)
            secondes -= 1
        print(f"{GREEN}Temps écoulé !            {RESET}")
    except ValueError:
        print(f"{RED}[-] Veuillez entrer un nombre valide.{RESET}")
    pause()


def tool_horloge():
    print("\n--- [ Date et heure actuelles ] ---")
    maintenant = datetime.datetime.now()
    print(f"{GREEN}[+] {maintenant.strftime('%A %d %B %Y - %H:%M:%S')}{RESET}")
    pause()


def tool_temperature():
    print("\n--- [ Convertisseur de température ] ---")
    choix = input("1. Celsius -> Fahrenheit | 2. Fahrenheit -> Celsius -> ").strip()
    try:
        valeur = float(input("Valeur : "))
        if choix == "1":
            resultat = valeur * 9 / 5 + 32
            print(f"{GREEN}[+] {valeur}°C = {resultat:.2f}°F{RESET}")
        elif choix == "2":
            resultat = (valeur - 32) * 5 / 9
            print(f"{GREEN}[+] {valeur}°F = {resultat:.2f}°C{RESET}")
        else:
            print(f"{RED}[-] Choix invalide.{RESET}")
    except ValueError:
        print(f"{RED}[-] Veuillez entrer un nombre valide.{RESET}")
    pause()


def tool_palindrome():
    print("\n--- [ Vérificateur de palindrome ] ---")
    texte = input("Texte à vérifier : ").strip().lower().replace(" ", "")
    if texte != "" and texte == texte[::-1]:
        print(f"{GREEN}[+] '{texte}' est un palindrome.{RESET}")
    else:
        print(f"{YELLOW}[-] Ce n'est pas un palindrome.{RESET}")
    pause()


def tool_de():
    print("\n--- [ Lancer de dé ] ---")
    try:
        faces = input("Nombre de faces (défaut 6) : ").strip()
        faces = int(faces) if faces else 6
        resultat = random.randint(1, faces)
        print(f"{GREEN}[+] Résultat : {resultat}{RESET}")
    except ValueError:
        print(f"{RED}[-] Veuillez entrer un nombre valide.{RESET}")
    pause()


def tool_texte_inverse():
    print("\n--- [ Miroir de texte ] ---")
    texte = input("Texte : ")
    print(f"{GREEN}[+] Résultat : {texte[::-1]}{RESET}")
    pause()


def menu_principal():
    options = {
        "1": tool_ping,
        "2": tool_ip_public,
        "3": tool_local_ip,
        "4": tool_dns_lookup,
        "5": tool_port_scanner,
        "6": tool_http_headers,
        "7": outil_base64,
        "8": tool_hash_sha256,
        "9": tool_gen_key,
        "10": tool_sys_info,
        "11": conversion_octets,
        "12": password_safe,
        "13": tool_password_gen,
        "14": tool_weather,
        "15": tool_uuid_gen,
        "16": tool_text_to_binary,
        "17": tool_binary_to_text,
        "18": tool_minuteur,
        "19": tool_horloge,
        "20": tool_temperature,
        "21": tool_palindrome,
        "22": tool_de,
        "23": tool_texte_inverse,
    }

    while True:
        clear()
        afficher_banniere()
        print(f"{CYAN}--- Réseau ---{RESET}")
        print(" 1. Pinger une cible")
        print(" 2. Afficher mon IP publique")
        print(" 3. Afficher mon IP locale")
        print(" 4. Résolution DNS")
        print(" 5. Scanner de ports")
        print(" 6. Vérifier les en-têtes HTTP d'un site")
        print(f"\n{CYAN}--- Sécurité & Chiffrement ---{RESET}")
        print(" 7. Encodage / Décodage Base64")
        print(" 8. Hash SHA-256")
        print(" 9. Générateur de clé Hex")
        print("12. Vérifier la sécurité d'un mot de passe")
        print("13. Générer un mot de passe sécurisé")
        print(f"\n{CYAN}--- Système & Utilitaires ---{RESET}")
        print("10. Infos système")
        print("11. Convertisseur d'octets")
        print("15. Générateur UUID")
        print("16. Texte -> Binaire")
        print("17. Binaire -> Texte")
        print("18. Minuteur")
        print("19. Date et heure actuelles")
        print(f"\n{CYAN}--- Divers ---{RESET}")
        print("14. Météo")
        print("20. Convertisseur de température")
        print("21. Vérificateur de palindrome")
        print("22. Lancer de dé")
        print("23. Miroir de texte")
        print("\n 0. Quitter")

        choix = input("\nChoisissez une option : ").strip()

        if choix == "0":
            print(f"{YELLOW}Fermeture du CEM Multi-Tool...{RESET}")
            sys.exit(0)
        elif choix in options:
            options[choix]()
        else:
            print(f"{RED}[-] Option invalide.{RESET}")
            pause()


def scan_rapide_depuis_argument():
    if len(sys.argv) > 1:
        cible = sys.argv[1]
        print(f"{CYAN}[i] Cible détectée en argument de lancement : {cible}{RESET}")
        confirmation = input("Lancer un scan de ports rapide sur cette cible ? (y/n) : ").strip().lower()
        if confirmation == "y":
            resultats = scanner_ports(cible)
            proposer_export_json({cible: resultats}, "resultats_scan.json")
            pause()


if __name__ == "__main__":
    scan_rapide_depuis_argument()
    menu_principal()
