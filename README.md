# Générateur de Devis CAM

Application Streamlit pour générer automatiquement des devis d'expertise immobilière au format PDF.

## Installation

1. Assurez-vous d'avoir Python installé sur votre système
2. Installez les dépendances :
```bash
pip install streamlit python-docx reportlab pandas
```

## Utilisation

1. Lancez l'application :
```bash
streamlit run app.py
```

2. Ouvrez votre navigateur à l'adresse indiquée (généralement http://localhost:8501)

3. Remplissez le formulaire avec les informations du devis :
   - **Informations générales** : référence, numéro, date, objet
   - **Consultation administrative** : documents nécessaires et leurs quantités
   - **Évaluation immobilière** : nombre de locaux à évaluer
   - **Montant en lettres** : pour l'arrêté du devis

4. Vérifiez le récapitulatif des montants dans la colonne de droite

5. Cliquez sur "Générer le PDF" pour créer et télécharger votre devis

## Fonctionnalités

- ✅ Interface utilisateur intuitive avec Streamlit
- ✅ Calcul automatique des totaux HT, TVA et TTC
- ✅ Génération de PDF professionnel avec ReportLab
- ✅ Téléchargement direct du devis généré
- ✅ Mise en page conforme au template Word original

## Structure des prix

Les prix unitaires par défaut sont configurables dans `config.py` :
- Certificat de copropriété : 50 DH
- Plan de copropriété : 75 DH
- Tableau de contenance : 60 DH
- Note de renseignements : 40 DH
- Évaluation par local : 2500 DH

## Personnalisation

Vous pouvez modifier les valeurs par défaut dans le fichier `config.py` :
- Prix unitaires
- Taux de TVA (actuellement 20%)
- Formats de référence et numéro de devis
- Délais et modalités de paiement

## Exemple de devis généré

Le PDF généré comprend :
- En-tête avec référence, numéro et date
- Objet du devis
- Tableau détaillé des prestations
- Calculs des montants HT, TVA et TTC
- Conditions de réalisation et paiement

## Support

Pour toute question ou problème, vérifiez que toutes les dépendances sont correctement installées.
