# 💈 Barbershop Manager 2025

**👩‍💻 Auteur : Havana Al-Ali — Projet académique | Module i164 | 2025**
Projet réalisé dans le cadre du Module 164.
Objectif : outil de gestion interne pour un barbershop familial.
---

## 📌 Description du projet

Application web de gestion d’un salon de coiffure (barbershop).  
Projet CRUD complet réalisé avec **Flask** et **Python**.

---

## ✂️ Fonctionnalités principales

- Gestion des employés (barbiers)
- Suivi des clients
- Services proposés (coupe, rasage, soins…)
- Rendez-vous et historique
- Liaison de tables via des modèles relationnels
- Interface HTML/CSS avec Bootstrap et WTForms

---

## 🛠️ Technologies utilisées

- Python
- Flask
- WTForms
- Bootstrap
- HeidiSQL

---

## 🚀 Lancer l'application

Dans un terminal :

bash
python run_mon_app.py
Ou avec Flask (si configuré) :
flask --app run_mon_app.py run

🔗 Accès local : http://127.0.0.1:5000/homepage


📦 Installation:

1.Cloner le dépôt :
git clone https://github.com/havamod164/AlAli_Havana_DEVA1A_BARBERSHOP_164_2025.git

2.Installer Python : https://www.python.org/downloads

3.Installer un IDE (ex. : PyCharm, VSCode)

4.Installer les dépendances :
pip install -r requirements.txt

🗄️ Base de données
Importer le fichier SQL :
APP_FILMS_164/database/alali_havana_deva1a_barbershop.sql

📂 Dépôt GitHub
🔗 https://github.com/havamod164/AlAli_Havana_DEVA1A_BARBERSHOP_164_2025


---

## 🧱 Structure du projet


```plaintext
AlAli_Havana_DEVA1A_BARBERSHOP_164_2025/
│
├── run_mon_app.py
├── .env
├── README.md
│
├── APP_FILMS_164/
│   ├── __init__.py
│
│   ├── database/
│   │   ├── __init__.py
│   │   ├── 1_ImportationDumpSql.py
│   │   └── alali_havana_deva1a_barbershop.sql
│
│   ├── models/
│   │   ├── clients
│   │   ├── employes
│   │   ├── evaluer
│   │   ├── services
│   │   └── rencontrer
│       └── executer
│
│   ├── views/
│   │   ├── gestion_clients_crud.py
│   │   ├── gestion_employes_crud.py
│   │   ├── gestion_evaluer_crud.py
│   │   ├── gestion_services_crud.py
│   │   ├── gestion_rencontrer_crud.py
│   │   ├── gestion_executer_crud.py
│   │   ├── gestion_clients_wtf_forms.py
│   │   ├── gestion_employes_wtf_forms.py
│   │   ├── gestion_evaluer_wtf_forms.py
│   │   ├── gestion_services_wtf_forms.py
│   │   ├── gestion_rencontrer_wtf_forms.py
│   │   └── gestion_executer_wtf_forms.py
│
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── readme.html
│   │
│   │   ├── clients/
│   │   │   ├── clients_delete_wtf.html
│   │   │   ├── client_update_wtf.html
│   │   │   ├── clients_afficher.html
│   │   │   └── clients_ajouter_wtf.html
│   │
│   │   ├── employes/
│   │   │   ├── employes_delete_wtf.html
│   │   │   ├── employes_update_wtf.html
│   │   │   ├── employes_afficher.html
│   │   │   └── employes_add_wtf.html
│   │       └── emp_rencontres_afficher.html
│   │
│   │   ├── services/
│   │       ├── services_delete_wtf.html
│   │       ├── services_update_wtf.html
│   │       ├── services_afficher.html
│   │       └── services_ajouter_wtf.html
│   │
│   │   ├── evaluer/
│   │   │   └── evaluer_afficher.html
│   │
│   │   ├── executer/
│   │   │   executer_afficher.html
│   │
│   │   └── zzz_essais_om_104/
│   │       ├── base.html
│   │       ├── home.html
│   │
│   │       ├── footer.html
│   │       ├── 404.html



