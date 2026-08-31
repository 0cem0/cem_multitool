> *For the English version of the README, click [here](README.md).*

# CEM Multi-Tool

Petit outil en ligne de commande écrit en Python, qui regroupe une vingtaine de fonctions utiles : réseau, chiffrement/hash, système et quelques utilitaires divers.

## Fonctionnalités

### Réseau
- Ping d'une cible
- IP publique / IP locale
- Résolution DNS
- Scanner de ports (21, 22, 80, 443, 3306, 8080)
- Vérification des en-têtes HTTP d'un site

### Sécurité & chiffrement
- Encodage / décodage Base64
- Hash SHA-256
- Générateur de clé hexadécimale
- Vérificateur de sécurité de mot de passe
- Générateur de mot de passe

### Système & utilitaires
- Infos système
- Convertisseur d'octets (Ko/Mo/Go)
- Générateur UUID
- Texte <-> Binaire
- Minuteur
- Date et heure actuelles

### Divers
- Météo (via wttr.in)
- Convertisseur de température
- Vérificateur de palindrome
- Lancer de dé
- Miroir de texte

## Prérequis

- Python 3
- Le module `requests`

```bash
pip install requests
