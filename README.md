# Générateur de Devis Automatique

Une application Streamlit pour générer automatiquement des devis (estimates/quotes) à partir de templates PDF.

## Fonctionnalités

- 📝 Interface utilisateur intuitive avec Streamlit
- 📄 Génération de PDF professionnels
- 💼 Gestion complète des informations client
- 🛠️ Ajout dynamique d'articles/services
- 💰 Calcul automatique des totaux (HT, TVA, TTC)
- ⬇️ Téléchargement direct des devis générés
- 📱 Interface responsive

## Installation

1. Clonez ou téléchargez ce projet
2. Installez les dépendances :

```bash
pip install -r requirements.txt
```

## Utilisation

1. Lancez l'application Streamlit :

```bash
streamlit run app.py
```

2. Ouvrez votre navigateur et accédez à `http://localhost:8501`

3. Remplissez le formulaire avec :
   - Les informations du client
   - Les détails du devis
   - Les articles/services
   - Les conditions de paiement

4. Cliquez sur "Générer le Devis PDF" pour créer et télécharger votre devis

## Structure du Projet

```
devis-generator/
├── app.py                 # Application Streamlit principale
├── pdf_generator.py       # Logique de génération PDF
├── utils.py              # Fonctions utilitaires
├── requirements.txt       # Dépendances Python
├── template/             # Templates PDF (placez vos templates ici)
├── generated/            # Devis générés (créé automatiquement)
└── README.md            # Ce fichier
```

## Personnalisation

### Ajouter de nouveaux templates
Placez vos fichiers PDF templates dans le dossier `template/`. L'application les détectera automatiquement.

### Modifier les styles PDF
Modifiez la classe `DevisGenerator` dans `pdf_generator.py` pour personnaliser :
- Les couleurs
- Les polices
- La mise en page
- Les logos d'entreprise

### Ajouter de nouveaux champs
Modifiez `app.py` pour ajouter de nouveaux champs au formulaire et `pdf_generator.py` pour les inclure dans le PDF.

## Configuration

### Informations de l'entreprise
Modifiez les informations de votre entreprise dans `pdf_generator.py` :

```python
company_client_data = [
    ['ENTREPRISE', 'CLIENT'],
    ['Votre Entreprise', data['client_name']],
    ['Votre Adresse', data.get('client_company', '')],
    # ...
]
```

### TVA par défaut
Modifiez le taux de TVA par défaut dans `app.py` :

```python
tva_rate = st.number_input("TVA (%)", min_value=0.0, max_value=100.0, value=20.0, step=0.1)
```

## Dépendances

- `streamlit` : Interface utilisateur web
- `reportlab` : Génération de PDF
- `pandas` : Manipulation de données
- `PyPDF2` : Manipulation de PDF
- `Pillow` : Traitement d'images

## Licence

Ce projet est open source. Vous pouvez l'utiliser et le modifier selon vos besoins.

## Support

Pour toute question ou suggestion, n'hésitez pas à créer une issue ou à contribuer au projet.
