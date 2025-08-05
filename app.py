import streamlit as st
import pandas as pd
from datetime import datetime
import os
from pdf_generator import DevisGenerator
from utils import validate_form_data, format_currency

# Page configuration
st.set_page_config(
    page_title="Générateur de Devis",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2c3e50;
        padding: 1rem 0;
        border-bottom: 2px solid #3498db;
        margin-bottom: 2rem;
    }
    .form-section {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #28a745;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-header">🏗️ Générateur de Devis Automatique</h1>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'items' not in st.session_state:
        st.session_state.items = []
    
    # Sidebar for template selection
    with st.sidebar:
        st.header("📁 Configuration")
        template_files = [f for f in os.listdir("template") if f.endswith('.pdf')]
        selected_template = st.selectbox("Sélectionner un template:", template_files)
        
        if st.button("🔄 Réinitialiser le formulaire"):
            st.session_state.items = []
            st.rerun()
    
    # Main form
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Client Information Section
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.subheader("👤 Informations Client")
        
        col_client1, col_client2 = st.columns(2)
        with col_client1:
            client_name = st.text_input("Nom du client *")
            client_address = st.text_area("Adresse du client")
            client_phone = st.text_input("Téléphone")
        
        with col_client2:
            client_company = st.text_input("Entreprise")
            client_email = st.text_input("Email")
            project_location = st.text_input("Lieu du projet")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quote Information Section
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.subheader("📋 Informations Devis")
        
        col_quote1, col_quote2 = st.columns(2)
        with col_quote1:
            quote_number = st.text_input("Numéro de devis *", value=f"DEV-{datetime.now().strftime('%Y%m%d')}-001")
            quote_date = st.date_input("Date du devis", value=datetime.now().date())
        
        with col_quote2:
            validity_period = st.number_input("Validité (jours)", min_value=1, value=30)
            payment_terms = st.selectbox("Conditions de paiement", 
                                       ["30% à la commande, solde à la livraison",
                                        "50% à la commande, 50% à la livraison",
                                        "Paiement comptant",
                                        "30 jours net"])
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Items Section
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.subheader("🛠️ Articles/Services")
        
        # Add new item form
        with st.expander("➕ Ajouter un article", expanded=True):
            col_item1, col_item2, col_item3, col_item4 = st.columns([3, 1, 1, 1])
            
            with col_item1:
                item_description = st.text_input("Description de l'article")
            with col_item2:
                item_quantity = st.number_input("Quantité", min_value=1, value=1)
            with col_item3:
                item_unit_price = st.number_input("Prix unitaire (DH)", min_value=0.0, step=0.01)
            with col_item4:
                st.write("")  # Spacing
                if st.button("Ajouter"):
                    if item_description and item_unit_price > 0:
                        new_item = {
                            "description": item_description,
                            "quantity": item_quantity,
                            "unit_price": item_unit_price,
                            "total": item_quantity * item_unit_price
                        }
                        st.session_state.items.append(new_item)
                        st.success("Article ajouté!")
                        st.rerun()
        
        # Display current items
        if st.session_state.items:
            st.write("**Articles ajoutés:**")
            items_df = pd.DataFrame(st.session_state.items)
            items_df['Prix unitaire'] = items_df['unit_price'].apply(lambda x: f"{x:,.2f} DH")
            items_df['Total'] = items_df['total'].apply(lambda x: f"{x:,.2f} DH")
            
            display_df = items_df[['description', 'quantity', 'Prix unitaire', 'Total']].copy()
            display_df.columns = ['Description', 'Quantité', 'Prix unitaire', 'Total']
            
            edited_df = st.data_editor(
                display_df,
                num_rows="dynamic",
                use_container_width=True,
                key="items_editor"
            )
            
            # Calculate totals
            total_ht = sum(item['total'] for item in st.session_state.items)
            tva_rate = st.number_input("TVA (%)", min_value=0.0, max_value=100.0, value=20.0, step=0.1)
            tva_amount = total_ht * (tva_rate / 100)
            total_ttc = total_ht + tva_amount
            
            # Display totals
            col_total1, col_total2 = st.columns([3, 1])
            with col_total2:
                st.write(f"**Total HT:** {total_ht:,.2f} DH")
                st.write(f"**TVA ({tva_rate}%):** {tva_amount:,.2f} DH")
                st.write(f"**Total TTC:** {total_ttc:,.2f} DH")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Additional Information
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.subheader("📝 Informations Complémentaires")
        notes = st.text_area("Notes/Observations", height=100)
        special_conditions = st.text_area("Conditions particulières", height=100)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.subheader("📊 Résumé")
        
        if client_name and quote_number and st.session_state.items:
            # Form is valid, show summary
            st.success("✅ Formulaire complet")
            
            st.write("**Client:**", client_name)
            st.write("**Devis N°:**", quote_number)
            st.write("**Date:**", quote_date.strftime("%d/%m/%Y"))
            st.write("**Nombre d'articles:**", len(st.session_state.items))
            
            if st.session_state.items:
                total_ht = sum(item['total'] for item in st.session_state.items)
                st.write("**Total HT:**", f"{total_ht:,.2f} DH")
            
            # Generate PDF button
            if st.button("📄 Générer le Devis PDF", type="primary", use_container_width=True):
                try:
                    # Prepare data for PDF generation
                    devis_data = {
                        'client_name': client_name,
                        'client_company': client_company,
                        'client_address': client_address,
                        'client_phone': client_phone,
                        'client_email': client_email,
                        'project_location': project_location,
                        'quote_number': quote_number,
                        'quote_date': quote_date,
                        'validity_period': validity_period,
                        'payment_terms': payment_terms,
                        'items': st.session_state.items,
                        'tva_rate': tva_rate if 'tva_rate' in locals() else 20.0,
                        'notes': notes,
                        'special_conditions': special_conditions
                    }
                    
                    # Generate PDF
                    generator = DevisGenerator(f"template/{selected_template}")
                    pdf_path = generator.generate_devis(devis_data)
                    
                    # Provide download
                    with open(pdf_path, "rb") as pdf_file:
                        st.download_button(
                            label="⬇️ Télécharger le Devis",
                            data=pdf_file.read(),
                            file_name=f"Devis_{quote_number}_{client_name.replace(' ', '_')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    
                    st.success("Devis généré avec succès!")
                    
                except Exception as e:
                    st.error(f"Erreur lors de la génération: {str(e)}")
        
        else:
            # Show what's missing
            st.warning("⚠️ Informations manquantes:")
            if not client_name:
                st.write("- Nom du client")
            if not quote_number:
                st.write("- Numéro de devis")
            if not st.session_state.items:
                st.write("- Articles/Services")
    
    # Footer
    st.markdown("---")
    st.markdown("*Générateur de Devis - Créé avec Streamlit*")

if __name__ == "__main__":
    main()
