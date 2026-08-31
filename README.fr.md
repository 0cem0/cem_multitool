# CEM Multi-Tool

Petit outil en ligne de commande écrit en Python, qui regroupe une vingtaine de fonctions utiles : réseau, chiffrement/hash, système, et quelques utilitaires divers.

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

```
pip install requests
```

## Utilisation

```
python cem_multitool.py
```

Un menu s'affiche, il suffit de rentrer le numéro de l'option voulue.

Une cible peut aussi être passée en argument pour lancer directement un scan de ports rapide :

```
python cem_multitool.py 192.168.1.1
```

Les résultats du scanner de ports et de la vérification des en-têtes HTTP peuvent être exportés en JSON.

## Notes

Le scanner de ports ne teste qu'une liste fixe de ports courants (21, 22, 80, 443, 3306, 8080). À utiliser sur ses propres machines et réseaux.

