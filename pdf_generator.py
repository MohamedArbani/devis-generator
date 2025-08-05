from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime, timedelta
import os

class DevisGenerator:
    def __init__(self, template_path=None):
        self.template_path = template_path
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom styles for the PDF"""
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=20,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2c3e50')
        )
        
        # Header style
        self.header_style = ParagraphStyle(
            'CustomHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.HexColor('#34495e')
        )
        
        # Normal style
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6
        )
        
        # Bold style
        self.bold_style = ParagraphStyle(
            'CustomBold',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            fontName='Helvetica-Bold'
        )
    
    def generate_devis(self, data):
        """Generate a devis PDF from the provided data"""
        # Create output filename
        output_filename = f"devis_{data['quote_number']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        output_path = os.path.join("generated", output_filename)
        
        # Create generated directory if it doesn't exist
        os.makedirs("generated", exist_ok=True)
        
        # Create PDF document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # Build the story (content)
        story = []
        
        # Add title
        story.append(Paragraph("DEVIS", self.title_style))
        story.append(Spacer(1, 20))
        
        # Add company info and client info side by side
        company_client_data = [
            ['ENTREPRISE', 'CLIENT'],
            ['CAM Construction', data['client_name']],
            ['123 Rue Example', data.get('client_company', '')],
            ['Ville, Code Postal', data.get('client_address', '')],
            ['Tél: +212 xxx xxx xxx', f"Tél: {data.get('client_phone', '')}"],
            ['Email: contact@cam.ma', f"Email: {data.get('client_email', '')}"]
        ]
        
        company_client_table = Table(company_client_data, colWidths=[8*cm, 8*cm])
        company_client_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(company_client_table)
        story.append(Spacer(1, 20))
        
        # Add quote details
        validity_date = data['quote_date'] + timedelta(days=data['validity_period'])
        quote_details_data = [
            ['Numéro de devis:', data['quote_number']],
            ['Date:', data['quote_date'].strftime('%d/%m/%Y')],
            ['Validité:', f"{data['validity_period']} jours (jusqu'au {validity_date.strftime('%d/%m/%Y')})"],
            ['Lieu du projet:', data.get('project_location', 'N/A')]
        ]
        
        quote_details_table = Table(quote_details_data, colWidths=[4*cm, 12*cm])
        quote_details_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        
        story.append(quote_details_table)
        story.append(Spacer(1, 30))
        
        # Add items table
        story.append(Paragraph("DÉTAIL DES PRESTATIONS", self.header_style))
        
        # Prepare items data
        items_data = [['Description', 'Quantité', 'Prix unitaire (DH)', 'Total (DH)']]
        
        total_ht = 0
        for item in data['items']:
            items_data.append([
                item['description'],
                str(item['quantity']),
                f"{item['unit_price']:,.2f}",
                f"{item['total']:,.2f}"
            ])
            total_ht += item['total']
            items_data.append([
                item['description'],
                str(item['quantity']),
                f"{item['unit_price']:,.2f}",
                f"{item['total']:,.2f}"
            ])
            total_ht += item['total']
        
        # Calculate taxes
        tva_rate = data.get('tva_rate', 20.0)
        tva_amount = total_ht * (tva_rate / 100)
        total_ttc = total_ht + tva_amount
        
        # Add totals rows
        items_data.extend([
            ['', '', 'Total HT:', f"{total_ht:,.2f}"],
            ['', '', f'TVA ({tva_rate}%):', f"{tva_amount:,.2f}"],
            ['', '', 'Total TTC:', f"{total_ttc:,.2f}"]
        ])
        
        items_table = Table(items_data, colWidths=[8*cm, 2*cm, 3*cm, 3*cm])
        items_table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            
            # Data rows
            ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            # Totals rows (last 3 rows)
            ('FONTNAME', (0, -3), (-1, -1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#ecf0f1')),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(items_table)
        story.append(Spacer(1, 30))
        
        # Add payment terms
        story.append(Paragraph("CONDITIONS DE PAIEMENT", self.header_style))
        story.append(Paragraph(data['payment_terms'], self.normal_style))
        story.append(Spacer(1, 20))
        
        # Add notes if any
        if data.get('notes'):
            story.append(Paragraph("NOTES", self.header_style))
            story.append(Paragraph(data['notes'], self.normal_style))
            story.append(Spacer(1, 20))
        
        # Add special conditions if any
        if data.get('special_conditions'):
            story.append(Paragraph("CONDITIONS PARTICULIÈRES", self.header_style))
            story.append(Paragraph(data['special_conditions'], self.normal_style))
            story.append(Spacer(1, 20))
        
        # Add footer
        story.append(Spacer(1, 30))
        story.append(Paragraph(
            "Merci de votre confiance. Ce devis est valable pour la durée mentionnée ci-dessus.",
            self.normal_style
        ))
        
        # Build PDF
        doc.build(story)
        
        return output_path
