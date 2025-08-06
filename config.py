# Configuration pour l'application Streamlit de génération de devis

# Valeurs par défaut pour les prix unitaires (en DH)
DEFAULT_PRICES = {
    'certificat_copropriete': 50.0,
    'plan_copropriete': 75.0,
    'tableau_contenance': 60.0,
    'note_renseignements': 40.0,
    'evaluation_local': 2500.0
}

# Taux de TVA
TVA_RATE = 0.20

# Délai de réalisation par défaut
DEFAULT_DEADLINE = "10 jours ouvrables"

# Modalité de paiement par défaut
DEFAULT_PAYMENT_TERMS = "100% à la livraison"

# Format de la référence par défaut
DEFAULT_REFERENCE_FORMAT = "CAM-{year}-{number:03d}"

# Format du numéro de devis par défaut
DEFAULT_DEVIS_FORMAT = "DEV-{number:03d}"
