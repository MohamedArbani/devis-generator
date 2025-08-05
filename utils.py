import re
from typing import Dict, List, Any

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """Validate phone number format (Moroccan format)"""
    if not phone:
        return True  # Phone is optional
    # Basic validation for Moroccan phone numbers
    pattern = r'^(\+212|0)[0-9]{9}$'
    return re.match(pattern, phone.replace(' ', '').replace('-', '')) is not None

def validate_form_data(data: Dict[str, Any]) -> List[str]:
    """Validate form data and return list of errors"""
    errors = []
    
    # Required fields
    if not data.get('client_name', '').strip():
        errors.append("Le nom du client est requis")
    
    if not data.get('quote_number', '').strip():
        errors.append("Le numéro de devis est requis")
    
    if not data.get('items') or len(data['items']) == 0:
        errors.append("Au moins un article doit être ajouté")
    
    # Email validation
    if data.get('client_email') and not validate_email(data['client_email']):
        errors.append("Format d'email invalide")
    
    # Phone validation
    if data.get('client_phone') and not validate_phone(data['client_phone']):
        errors.append("Format de téléphone invalide")
    
    # Items validation
    if data.get('items'):
        for i, item in enumerate(data['items']):
            if not item.get('description', '').strip():
                errors.append(f"Description manquante pour l'article {i+1}")
            if item.get('quantity', 0) <= 0:
                errors.append(f"Quantité invalide pour l'article {i+1}")
            if item.get('unit_price', 0) <= 0:
                errors.append(f"Prix unitaire invalide pour l'article {i+1}")
    
    return errors

def format_currency(amount: float, currency: str = "DH") -> str:
    """Format currency with proper formatting"""
    return f"{amount:,.2f} {currency}"

def generate_quote_number(prefix: str = "DEV") -> str:
    """Generate a quote number with timestamp"""
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d")
    return f"{prefix}-{timestamp}-001"

def calculate_totals(items: List[Dict], tva_rate: float = 20.0) -> Dict[str, float]:
    """Calculate totals for a list of items"""
    total_ht = sum(item['total'] for item in items)
    tva_amount = total_ht * (tva_rate / 100)
    total_ttc = total_ht + tva_amount
    
    return {
        'total_ht': total_ht,
        'tva_amount': tva_amount,
        'total_ttc': total_ttc,
        'tva_rate': tva_rate
    }

def clean_filename(filename: str) -> str:
    """Clean filename for safe file creation"""
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove extra spaces and periods
    filename = re.sub(r'\s+', '_', filename.strip())
    filename = re.sub(r'\.+', '.', filename)
    
    return filename
