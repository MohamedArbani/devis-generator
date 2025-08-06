import streamlit as st
from docx import Document
import docxedit
from docx2pdf import convert
from datetime import datetime
import os
import tempfile
import shutil

# Configuration de la page
st.set_page_config(page_title="Générateur de Devis CAM", page_icon="🏗️", layout="wide")

st.title("🏗️ Générateur de Devis CAM")
st.markdown("---")


# Fonction pour calculer les totaux
def calculate_totals(
    cc_qty, pc_qty, tc_qty, nr_qty, local_qty, pu_cc, pu_pc, pu_tc, pu_nr, pu_local
):
    pt_cc = cc_qty * pu_cc if cc_qty and pu_cc else 0
    pt_pc = pc_qty * pu_pc if pc_qty and pu_pc else 0
    pt_tc = tc_qty * pu_tc if tc_qty and pu_tc else 0
    pt_nr = nr_qty * pu_nr if nr_qty and pu_nr else 0
    pt_local = local_qty * pu_local if local_qty and pu_local else 0

    m_ht = pt_cc + pt_pc + pt_tc + pt_nr + pt_local
    tva = m_ht * 0.20
    m_ttc = m_ht + tva

    return pt_cc, pt_pc, pt_tc, pt_nr, pt_local, m_ht, tva, m_ttc


# Fonction pour convertir un nombre en lettres (français)
def number_to_french_words(number):
    """Convertit un nombre en mots français (version simplifiée)"""
    if number == 0:
        return "ZÉRO"

    units = ["", "UN", "DEUX", "TROIS", "QUATRE", "CINQ", "SIX", "SEPT", "HUIT", "NEUF"]
    tens = [
        "",
        "",
        "VINGT",
        "TRENTE",
        "QUARANTE",
        "CINQUANTE",
        "SOIXANTE",
        "SOIXANTE",
        "QUATRE-VINGT",
        "QUATRE-VINGT",
    ]

    def convert_hundreds(n):
        result = ""
        if n >= 100:
            hundreds = n // 100
            if hundreds == 1:
                result += "CENT "
            else:
                result += units[hundreds] + " CENT "
            n %= 100

        if n >= 80:
            if n == 80:
                result += "QUATRE-VINGTS"
            else:
                result += "QUATRE-VINGT-" + units[n - 80]
        elif n >= 70:
            if n == 70:
                result += "SOIXANTE-DIX"
            else:
                result += "SOIXANTE-" + units[n - 60]
        elif n >= 60:
            if n == 60:
                result += "SOIXANTE"
            else:
                result += "SOIXANTE-" + units[n - 60]
        elif n >= 20:
            tens_digit = n // 10
            units_digit = n % 10
            result += tens[tens_digit]
            if units_digit > 0:
                result += "-" + units[units_digit]
        elif n >= 10:
            if n == 10:
                result += "DIX"
            elif n == 11:
                result += "ONZE"
            elif n == 12:
                result += "DOUZE"
            elif n == 13:
                result += "TREIZE"
            elif n == 14:
                result += "QUATORZE"
            elif n == 15:
                result += "QUINZE"
            elif n == 16:
                result += "SEIZE"
            elif n == 17:
                result += "DIX-SEPT"
            elif n == 18:
                result += "DIX-HUIT"
            elif n == 19:
                result += "DIX-NEUF"
        else:
            result += units[n]

        return result.strip()

    if number < 1000:
        return convert_hundreds(number)
    elif number < 1000000:
        thousands = number // 1000
        remainder = number % 1000
        result = ""
        if thousands == 1:
            result += "MILLE "
        else:
            result += convert_hundreds(thousands) + " MILLE "
        if remainder > 0:
            result += convert_hundreds(remainder)
        return result.strip()
    else:
        return "NOMBRE TROP GRAND"


# Fonction pour créer le document Word modifié
def create_word_document(data, template_path):
    # Créer une copie temporaire du template
    temp_dir = tempfile.mkdtemp()
    temp_template_path = os.path.join(temp_dir, "temp_template.docx")
    shutil.copy2(template_path, temp_template_path)

    # Ouvrir le document
    document = Document(temp_template_path)

    # Remplacer les placeholders avec les données
    replacements = {
        "{REFERENCE}": data["reference"],
        "{DEVIS_NUMBER}": data["devis_number"],
        "{DATE}": data["date"],
        "{OBJECTIF}": data["objectif"],
        "{GERANT}": data["gerant"],
        "{CC}": str(data["cc_qty"]) if data["cc_qty"] > 0 else "",
        "{PC}": str(data["pc_qty"]) if data["pc_qty"] > 0 else "",
        "{TC}": str(data["tc_qty"]) if data["tc_qty"] > 0 else "",
        "{NR}": str(data["nr_qty"]) if data["nr_qty"] > 0 else "",
        "{LOCAL}": str(data["local_qty"]) if data["local_qty"] > 0 else "",
        "{PU_CC}": f"{data['pu_cc']:.2f}" if data["cc_qty"] > 0 else "",
        "{PU_PC}": f"{data['pu_pc']:.2f}" if data["pc_qty"] > 0 else "",
        "{PU_TC}": f"{data['pu_tc']:.2f}" if data["tc_qty"] > 0 else "",
        "{PU_NR}": f"{data['pu_nr']:.2f}" if data["nr_qty"] > 0 else "",
        "{PU_L}": f"{data['pu_local']:.2f}" if data["local_qty"] > 0 else "",
        "{PT_CC}": f"{data['pt_cc']:.2f}" if data["cc_qty"] > 0 else "",
        "{PT_PC}": f"{data['pt_pc']:.2f}" if data["pc_qty"] > 0 else "",
        "{PT_TC}": f"{data['pt_tc']:.2f}" if data["tc_qty"] > 0 else "",
        "{PT_NR}": f"{data['pt_nr']:.2f}" if data["nr_qty"] > 0 else "",
        "{PT_L}": f"{data['pt_local']:.2f}" if data["local_qty"] > 0 else "",
        "{REP}": str(data["rep_qty"]),
        "{M_HT}": f"{data['m_ht']:.2f}",
        "{TVA}": f"{data['tva']:.2f}",
        "{M_TTC}": f"{data['m_ttc']:.2f}",
    }

    # Effectuer les remplacements
    for old_string, new_string in replacements.items():
        if new_string:  # Seulement si la nouvelle chaîne n'est pas vide
            docxedit.replace_string(
                document, old_string=old_string, new_string=new_string
            )

    # Sauvegarder le document modifié
    output_path = os.path.join(
        temp_dir, f"Devis_{data['devis_number']}_{data['date'].replace('/', '')}.docx"
    )
    document.save(output_path)

    return output_path, temp_dir


# Fonction pour convertir Word en PDF
def convert_to_pdf(docx_path, temp_dir):
    try:
        # Convertir en PDF
        pdf_path = docx_path.replace(".docx", ".pdf")
        convert(docx_path, pdf_path)
        return pdf_path
    except Exception as e:
        st.error(f"Erreur lors de la conversion en PDF: {str(e)}")
        return None


# Interface utilisateur
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📋 Informations du Devis")

    # Vérification du template
    template_path = (
        "./template/Devis_Num_CAM_Local-LOCAL.docx"
    )
    if not os.path.exists(template_path):
        st.error(f"⚠️ Template Word non trouvé à l'emplacement : {template_path}")
        st.info(
            "Assurez-vous que votre fichier template 'Devis_Num_CAM_Local-LOCAL.docx' existe dans le dossier 'template'."
        )
        st.stop()
    else:
        st.success("✅ Template Word original trouvé")

    # Informations générales
    st.subheader("Informations générales")
    reference = st.text_input("Référence", value="CAM-2025-001")
    devis_number = st.text_input("Numéro de devis", value="DEV-001")
    date = st.date_input("Date", value=datetime.now())
    objectif = st.text_area("Objet", value="Expertise immobilière")
    gerant = st.text_input("Gérant", value="")

    st.markdown("---")

    # Consultation administrative
    st.subheader("Consultation administrative")

    col_ca1, col_ca2, col_ca3 = st.columns(3)

    with col_ca1:
        st.markdown("**Certificat de copropriété**")
        cc_qty = st.number_input("Quantité CC", min_value=0, value=1, key="cc_qty")
        pu_cc = st.number_input("P.U. CC (DH)", min_value=0.0, value=50.0, key="pu_cc")

    with col_ca2:
        st.markdown("**Plan de copropriété**")
        pc_qty = st.number_input("Quantité PC", min_value=0, value=1, key="pc_qty")
        pu_pc = st.number_input("P.U. PC (DH)", min_value=0.0, value=75.0, key="pu_pc")

    with col_ca3:
        st.markdown("**Tableau de Contenance**")
        tc_qty = st.number_input("Quantité TC", min_value=0, value=1, key="tc_qty")
        pu_tc = st.number_input("P.U. TC (DH)", min_value=0.0, value=60.0, key="pu_tc")

    col_ca4, col_ca5 = st.columns(2)

    with col_ca4:
        st.markdown("**Note de renseignements**")
        nr_qty = st.number_input("Quantité NR", min_value=0, value=1, key="nr_qty")
        pu_nr = st.number_input("P.U. NR (DH)", min_value=0.0, value=40.0, key="pu_nr")

    st.markdown("---")

    # Évaluation immobilière
    st.subheader("Évaluation immobilière")

    col_ei1, col_ei2 = st.columns(2)

    with col_ei1:
        local_qty = st.number_input(
            "Nombre de locaux", min_value=0, value=1, key="local_qty"
        )
        pu_local = st.number_input(
            "P.U. Local (DH)", min_value=0.0, value=2500.0, key="pu_local"
        )

    # Livrables
    st.subheader("Livrables")
    rep_qty = st.number_input("Nombre de rapports", min_value=1, value=1, key="rep_qty")

with col2:
    st.header("💰 Récapitulatif")

    # Calcul des totaux
    pt_cc, pt_pc, pt_tc, pt_nr, pt_local, m_ht, tva, m_ttc = calculate_totals(
        cc_qty, pc_qty, tc_qty, nr_qty, local_qty, pu_cc, pu_pc, pu_tc, pu_nr, pu_local
    )

    # Affichage des totaux partiels
    if cc_qty > 0:
        st.metric("Total CC", f"{pt_cc:.2f} DH")
    if pc_qty > 0:
        st.metric("Total PC", f"{pt_pc:.2f} DH")
    if tc_qty > 0:
        st.metric("Total TC", f"{pt_tc:.2f} DH")
    if nr_qty > 0:
        st.metric("Total NR", f"{pt_nr:.2f} DH")
    if local_qty > 0:
        st.metric("Total Local", f"{pt_local:.2f} DH")

    st.markdown("---")

    # Totaux finaux
    st.metric("Montant HT", f"{m_ht:.2f} DH")
    st.metric("TVA (20%)", f"{tva:.2f} DH")
    st.metric("**Montant TTC**", f"{m_ttc:.2f} DH")

    # Conversion automatique en lettres
    montant_lettres = number_to_french_words(int(m_ttc))
    st.info(f"**Montant en lettres:** {montant_lettres}")

    st.markdown("---")

    # Options de génération
    st.subheader("📁 Options de génération")
    format_choice = st.radio(
        "Format de sortie:", ["PDF", "Word (.docx)", "Les deux"], index=0
    )

    # Génération du document
    if st.button("📄 Générer le Document", type="primary", use_container_width=True):
        # Préparer les données
        data = {
            "reference": reference,
            "devis_number": devis_number,
            "date": date.strftime("%d/%m/%Y"),
            "objectif": objectif,
            "gerant": gerant,
            "cc_qty": cc_qty,
            "pc_qty": pc_qty,
            "tc_qty": tc_qty,
            "nr_qty": nr_qty,
            "local_qty": local_qty,
            "rep_qty": rep_qty,
            "pu_cc": pu_cc,
            "pu_pc": pu_pc,
            "pu_tc": pu_tc,
            "pu_nr": pu_nr,
            "pu_local": pu_local,
            "pt_cc": pt_cc,
            "pt_pc": pt_pc,
            "pt_tc": pt_tc,
            "pt_nr": pt_nr,
            "pt_local": pt_local,
            "m_ht": m_ht,
            "tva": tva,
            "m_ttc": m_ttc,
            "montant_lettres": montant_lettres,
        }

        try:
            # Créer le document Word
            with st.spinner("🔄 Génération du document en cours..."):
                docx_path, temp_dir = create_word_document(data, template_path)

                # Lire le fichier Word
                with open(docx_path, "rb") as file:
                    docx_data = file.read()

                col_dl1, col_dl2 = st.columns(2)

                # Téléchargement Word
                if format_choice in ["Word (.docx)", "Les deux"]:
                    with col_dl1:
                        st.download_button(
                            label="📄 Télécharger Word",
                            data=docx_data,
                            file_name=f"Devis_{devis_number}_{date.strftime('%Y%m%d')}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            use_container_width=True,
                        )

                # Conversion et téléchargement PDF
                if format_choice in ["PDF", "Les deux"]:
                    pdf_path = convert_to_pdf(docx_path, temp_dir)
                    if pdf_path and os.path.exists(pdf_path):
                        with open(pdf_path, "rb") as file:
                            pdf_data = file.read()

                        with col_dl2:
                            st.download_button(
                                label="📋 Télécharger PDF",
                                data=pdf_data,
                                file_name=f"Devis_{devis_number}_{date.strftime('%Y%m%d')}.pdf",
                                mime="application/pdf",
                                use_container_width=True,
                            )

                # Nettoyage des fichiers temporaires
                shutil.rmtree(temp_dir)

                st.success("✅ Document généré avec succès!")

        except Exception as e:
            st.error(f"❌ Erreur lors de la génération: {str(e)}")
            st.info(
                "Vérifiez que Microsoft Word est installé sur votre système pour la conversion PDF."
            )

# Instructions
st.markdown("---")
st.markdown("""
### 📝 Instructions d'utilisation

1. **Remplissez les informations générales** : référence, numéro de devis, date et objet
2. **Configurez la consultation administrative** : sélectionnez les documents nécessaires et leurs quantités
3. **Paramétrez l'évaluation immobilière** : nombre de locaux à évaluer
4. **Vérifiez le récapitulatif** des montants dans la colonne de droite
5. **Choisissez le format de sortie** : PDF, Word ou les deux
6. **Cliquez sur "Générer le Document"** pour créer et télécharger votre devis

### ✨ Avantages de cette nouvelle version

- **🎨 Préserve la mise en forme originale** du template Word
- **📄 Génération directe en Word et/ou PDF**
- **🤖 Conversion automatique** du montant en lettres
- **⚡ Plus rapide et plus fidèle** au template original

Le calcul de la TVA se fait automatiquement à 20% sur le montant HT.
Le montant en lettres est généré automatiquement en français.
""")
