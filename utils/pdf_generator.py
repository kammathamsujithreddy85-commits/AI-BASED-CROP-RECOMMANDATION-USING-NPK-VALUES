try:
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib import colors
    from reportlab.lib.units import inch, cm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from reportlab.pdfgen import canvas
except ImportError as e:
    raise ImportError("reportlab library not installed. Install with: pip install reportlab") from e
from io import BytesIO
from datetime import datetime
import os

def generate_calendar_pdf(season='all', months=None):
    """
    Generate PDF calendar for crops
    """
    buffer = BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # Container for PDF elements
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a5276'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#2e86de'),
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1a5276'),
        spaceAfter=10,
        fontName='Helvetica-Bold'
    )
    
    # Header
    elements.append(Paragraph("🌾 Crop Calendar 2024-25", title_style))
    elements.append(Paragraph("Ministry of Agriculture & Farmers Welfare | Government of India", subtitle_style))
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y')}", 
                             ParagraphStyle('Date', parent=styles['Normal'], fontSize=10, alignment=TA_CENTER)))
    elements.append(Spacer(1, 20))
    
    # Crop calendar data
    calendar_data = get_calendar_data(season, months)
    
    # Create tables for each month
    for month_info in calendar_data:
        elements.append(Paragraph(f"📅 {month_info['month']} - {month_info['season']}", heading_style))
        
        # Table data
        table_data = [['Crop', 'Activity', 'Key Points', 'Status']]
        
        for crop in month_info['crops']:
            table_data.append([
                crop['name'],
                crop['activity'],
                crop['points'],
                crop['status']
            ])
        
        # Create table
        table = Table(table_data, colWidths=[2*inch, 2.5*inch, 3.5*inch, 1.5*inch])
        
        # Table style
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5276')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
        
        # Add page break if needed
        if month_info != calendar_data[-1]:
            elements.append(PageBreak())
    
    # Add tips section
    elements.append(Paragraph("💡 Important Farming Tips", heading_style))
    tips_data = get_farming_tips()
    
    for tip in tips_data:
        elements.append(Paragraph(f"• {tip}", styles['Normal']))
    
    # Build PDF
    doc.build(elements, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    
    buffer.seek(0)
    return buffer

def get_calendar_data(season, months):
    """Get calendar data based on season filter"""
    
    all_months = [
        {
            'month': 'June',
            'season': 'Kharif Season - Monsoon Begins',
            'crops': [
                {'name': 'Rice (Paddy)', 'activity': 'Nursery preparation & sowing', 
                 'points': 'Land preparation, puddling, seed treatment', 'status': 'SOWING'},
                {'name': 'Maize', 'activity': 'Sowing with monsoon onset', 
                 'points': 'Use treated seeds, maintain spacing', 'status': 'SOWING'},
                {'name': 'Cotton', 'activity': 'Early sowing', 
                 'points': 'Bt cotton hybrids, proper spacing', 'status': 'SOWING'},
            ]
        },
        {
            'month': 'July',
            'season': 'Kharif Season - Peak Monsoon',
            'crops': [
                {'name': 'Rice', 'activity': 'Transplanting', 
                 'points': '2-3 seedlings/hill, 20x15cm spacing', 'status': 'TRANSPLANTING'},
                {'name': 'Groundnut', 'activity': 'Sowing continues', 
                 'points': 'Seed treatment, gypsum application', 'status': 'SOWING'},
                {'name': 'Soybean', 'activity': 'Sowing (first fortnight)', 
                 'points': 'Rhizobium treatment, row spacing', 'status': 'SOWING'},
            ]
        },
        {
            'month': 'August',
            'season': 'Kharif Season - Active Growth',
            'crops': [
                {'name': 'Rice', 'activity': 'Top dressing & pest control', 
                 'points': 'Urea application, monitor stem borer', 'status': 'FERTILIZER'},
                {'name': 'Maize', 'activity': 'Weeding & earthing up', 
                 'points': '2nd weeding, earthing for support', 'status': 'INTERCULTURE'},
                {'name': 'Sugarcane', 'activity': 'Earthing up', 
                 'points': 'Final earthing, trash mulching', 'status': 'MAINTENANCE'},
            ]
        },
        {
            'month': 'September',
            'season': 'Kharif Season - Maturing',
            'crops': [
                {'name': 'Rice (Early)', 'activity': 'Harvesting early varieties', 
                 'points': 'Drain water 7-10 days before', 'status': 'HARVESTING'},
                {'name': 'Cotton', 'activity': 'First picking', 
                 'points': 'Pick when bolls open, avoid dew', 'status': 'HARVESTING'},
                {'name': 'Groundnut', 'activity': 'Pod development', 
                 'points': 'Maintain moisture, pest watch', 'status': 'GROWTH'},
            ]
        },
        {
            'month': 'October',
            'season': 'Post-Monsoon / Rabi Prep',
            'crops': [
                {'name': 'Rice (Late)', 'activity': 'Main harvesting', 
                 'points': 'Threshing, drying to 14% moisture', 'status': 'HARVESTING'},
                {'name': 'Wheat', 'activity': 'Early sowing (some regions)', 
                 'points': 'Land preparation, seed treatment', 'status': 'EARLY SOWING'},
                {'name': 'Vegetables', 'activity': 'Nursery for tomato, cabbage', 
                 'points': 'Raised beds, shade net', 'status': 'NURSERY'},
            ]
        },
        {
            'month': 'November',
            'season': 'Rabi Season Begins',
            'crops': [
                {'name': 'Wheat', 'activity': 'Optimal sowing time', 
                 'points': 'Certified seeds, seed rate 40-50kg/acre', 'status': 'SOWING'},
                {'name': 'Mustard', 'activity': 'Sowing (first fortnight)', 
                 'points': 'Treated seeds, 30-45cm spacing', 'status': 'SOWING'},
                {'name': 'Chickpea', 'activity': 'Sowing (mid-November)', 
                 'points': 'Rhizobium culture, deep sowing', 'status': 'SOWING'},
            ]
        },
        {
            'month': 'December',
            'season': 'Rabi Season - Winter',
            'crops': [
                {'name': 'Wheat', 'activity': 'First irrigation (Crown root)', 
                 'points': '21 days after sowing, critical stage', 'status': 'IRRIGATION'},
                {'name': 'Potato', 'activity': 'Earthing up', 
                 'points': 'For tuber development, weed control', 'status': 'MAINTENANCE'},
                {'name': 'Vegetables', 'activity': 'Harvesting winter crops', 
                 'points': 'Tomato, cabbage, cauliflower', 'status': 'HARVESTING'},
            ]
        },
        {
            'month': 'January',
            'season': 'Rabi Season - Peak Winter',
            'crops': [
                {'name': 'Wheat', 'activity': 'Second irrigation (Tillering)', 
                 'points': 'Frost protection, mulching', 'status': 'IRRIGATION'},
                {'name': 'Mustard', 'activity': 'Flowering stage', 
                 'points': 'Bee pollination, aphid control', 'status': 'FLOWERING'},
                {'name': 'Potato', 'activity': 'Tuber bulking', 
                 'points': 'Adequate moisture, blight control', 'status': 'GROWTH'},
            ]
        },
        {
            'month': 'February',
            'season': 'Rabi Season - Late Winter',
            'crops': [
                {'name': 'Wheat', 'activity': 'Third irrigation & top dressing', 
                 'points': 'Urea application, jointing stage', 'status': 'FERTILIZER'},
                {'name': 'Potato', 'activity': 'Early harvesting', 
                 'points': 'Vine cutting, careful digging', 'status': 'HARVESTING'},
                {'name': 'Watermelon', 'activity': 'Nursery preparation', 
                 'points': 'Raised beds, seed treatment', 'status': 'PREPARATION'},
            ]
        },
        {
            'month': 'March',
            'season': 'Rabi Season - Harvesting',
            'crops': [
                {'name': 'Wheat', 'activity': 'Last irrigation & pest watch', 
                 'points': 'Milk stage, monitor aphids & rust', 'status': 'MAINTENANCE'},
                {'name': 'Mustard', 'activity': 'Harvesting', 
                 'points': 'When pods turn yellow-brown', 'status': 'HARVESTING'},
                {'name': 'Mango', 'activity': 'Flowering season', 
                 'points': 'Pollination, pest management', 'status': 'FLOWERING'},
            ]
        },
        {
            'month': 'April',
            'season': 'Summer / Pre-Monsoon',
            'crops': [
                {'name': 'Wheat', 'activity': 'Harvesting & threshing', 
                 'points': 'Grain moisture 20-25%, drying', 'status': 'HARVESTING'},
                {'name': 'Muskmelon', 'activity': 'Direct sowing', 
                 'points': 'Pits preparation, organic manure', 'status': 'SOWING'},
                {'name': 'Vegetables', 'activity': 'Summer crops - Okra, Gourds', 
                 'points': 'Irrigation management, mulching', 'status': 'SUMMER CROPS'},
            ]
        },
        {
            'month': 'May',
            'season': 'Summer / Pre-Monsoon Prep',
            'crops': [
                {'name': 'Rice', 'activity': 'Land preparation', 
                 'points': 'Summer ploughing, puddling', 'status': 'PREPARATION'},
                {'name': 'Maize', 'activity': 'Spring maize harvesting', 
                 'points': 'Cob maturity, drying', 'status': 'HARVESTING'},
                {'name': 'Mango', 'activity': 'Fruit maturity & harvesting', 
                 'points': 'Mature green stage, careful handling', 'status': 'HARVESTING'},
            ]
        },
    ]
    
    # Filter based on season
    if season == 'all':
        filtered = all_months
    else:
        season_map = {
            'kharif': ['June', 'July', 'August', 'September', 'October'],
            'rabi': ['November', 'December', 'January', 'February', 'March'],
            'summer': ['April', 'May']
        }
        filtered = [m for m in all_months if m['month'] in season_map.get(season, [])]
    
    # Filter specific months if provided
    if months:
        filtered = [m for m in filtered if m['month'] in months]
    
    return filtered

def get_farming_tips():
    """Get general farming tips for PDF"""
    return [
        "Test soil every 2 years and follow Soil Health Card recommendations",
        "Use certified seeds of high-yielding, disease-resistant varieties",
        "Practice crop rotation to maintain soil health and break pest cycles",
        "Apply organic manure @ 5-10 tonnes/ha along with chemical fertilizers",
        "Adopt drip/sprinkler irrigation to save 30-60% water",
        "Monitor fields weekly for early pest and disease detection",
        "Harvest at proper maturity stage for maximum yield and quality",
        "Dry grains to safe moisture content (12-14%) before storage",
        "Store produce in clean, dry, pest-proof structures",
        "Maintain farm records for better planning and scheme benefits",
        "Register for PM-KISAN, crop insurance, and other government schemes",
        "Join Farmer Producer Organization (FPO) for better market access"
    ]

def add_header_footer(canvas, doc):
    """Add header and footer to PDF pages"""
    canvas.saveState()
    
    # Header
    canvas.setFont('Helvetica-Bold', 10)
    canvas.setFillColor(colors.HexColor('#1a5276'))
    canvas.drawString(inch, doc.pagesize[1] - inch, "Crop Calendar 2024-25 | Ministry of Agriculture")
    
    # Footer
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(colors.grey)
    canvas.drawString(inch, inch, f"Page {doc.page}")
    canvas.drawString(doc.pagesize[0] - 200, inch, "Helpline: 1800-180-1551")
    
    canvas.restoreState()