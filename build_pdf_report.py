import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_OUTPUT_PATH = os.path.join(BASE_DIR, "FINAL_PROJECT_REPORT.pdf")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "PROJECT FORESIGHT — Demand & Inventory Intelligence | Final Project Report")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
            
        # Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_str)
        self.drawString(54, 36, "Confidential — NorthBay Living & Zidio Development")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        self.restoreState()

def generate_pdf():
    doc = SimpleDocTemplate(
        PDF_OUTPUT_PATH,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#2563EB'),
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Header1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Header2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )
    
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#334155'),
        leftIndent=12,
        spaceAfter=3
    )

    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=4,
        spaceAfter=6
    )

    table_header_style = ParagraphStyle(
        'TH',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#FFFFFF'),
        alignment=0
    )

    table_cell_style = ParagraphStyle(
        'TC',
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#0F172A'),
        alignment=0
    )

    story = []

    # Title Banner
    story.append(Paragraph("PROJECT FORESIGHT", title_style))
    story.append(Paragraph("Enterprise Retail Demand Forecasting & Inventory Risk Intelligence", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563EB"), spaceAfter=12))

    # Metadata Grid Table
    meta_data = [
        [
            Paragraph("<b>Client:</b> NorthBay Living", table_cell_style),
            Paragraph("<b>Author / Intern:</b> MHK", table_cell_style)
        ],
        [
            Paragraph("<b>Role:</b> Data Science & Analytics Intern", table_cell_style),
            Paragraph("<b>Program:</b> Zidio Development Internship", table_cell_style)
        ],
        [
            Paragraph("<b>Repository:</b> https://github.com/MHK-123/Foresight", table_cell_style),
            Paragraph("<b>Completion Date:</b> August 2026", table_cell_style)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[250, 254])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E2E8F0")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 10))

    # 1. Executive Summary
    story.append(Paragraph("1. Executive Summary", h1_style))
    story.append(Paragraph(
        "Project FORESIGHT delivers an enterprise-grade retail demand forecasting and explainable inventory risk intelligence system for <b>NorthBay Living</b>, a retail chain operating 30 stores across 4 formats with 5,000 active SKUs. Using 4 years of operational transaction data (9.945M records), the project developed a production <b>LightGBM Regressor</b> that achieves <b>42.16% Out-of-Sample WAPE</b> (-11.3% error reduction over baseline) and <b>1.183 RMSE</b> (-20.3% error reduction) on the 2025 temporal test set.",
        body_style
    ))
    story.append(Paragraph(
        "The automated risk engine evaluated all <b>26,408 store-SKU positions</b> and identified <b>Rs. 1.78 Billion in trapped overstock capital</b> (68.1% of network) and <b>5,209 stockout deficit positions</b> with <b>100.0% validation recall</b> on ground-truth defect benchmarks. A Streamlit decision dashboard was delivered featuring 8 operational views, priority purchase order worklists, what-if simulation, and an AI intelligence assistant.",
        body_style
    ))

    # 2. Business Problem & Objectives
    story.append(Paragraph("2. Business Problem & Objectives", h1_style))
    story.append(Paragraph("<b>Core Business Pain Points:</b>", h2_style))
    story.append(Paragraph("• <b>Lost Revenue from Stockouts:</b> High-velocity staples frequently experienced zero stock, causing immediate revenue loss and unrecorded customer demand.", bullet_style))
    story.append(Paragraph("• <b>Trapped Working Capital:</b> Stagnant inventory tied up over Rs. 1.78B in capital exceeding 120+ days of supply.", bullet_style))
    story.append(Paragraph("• <b>Flawed Historical Heuristics:</b> Standard rolling averages under-forecasted items recovering from stockouts.", bullet_style))
    story.append(Paragraph("• <b>Lack of Actionable Priority:</b> Supply chain planners lacked automated, priority-ranked purchase order and stock transfer workflows.", bullet_style))

    # 3. Enterprise Data Architecture
    story.append(Paragraph("3. Enterprise Dataset Architecture", h1_style))
    ds_table_data = [
        [
            Paragraph("Dataset", table_header_style),
            Paragraph("Records", table_header_style),
            Paragraph("Grain / Key", table_header_style),
            Paragraph("Attributes & Role", table_header_style)
        ],
        [
            Paragraph("<code>transactions_clean</code>", table_cell_style),
            Paragraph("9,945,396", table_cell_style),
            Paragraph("Transaction x Date", table_cell_style),
            Paragraph("Sales quantities, prices, discounts, promos, channels (2022-2025)", table_cell_style)
        ],
        [
            Paragraph("<code>inventory_clean</code>", table_cell_style),
            Paragraph("26,408", table_cell_style),
            Paragraph("Store ID x SKU ID", table_cell_style),
            Paragraph("Stock on hand, safety stock, reorder point, last restock date", table_cell_style)
        ],
        [
            Paragraph("<code>products_clean</code>", table_cell_style),
            Paragraph("5,000", table_cell_style),
            Paragraph("SKU ID", table_cell_style),
            Paragraph("SKU name, 12 categories, brand, cost price, retail price", table_cell_style)
        ],
        [
            Paragraph("<code>stores_clean</code>", table_cell_style),
            Paragraph("30", table_cell_style),
            Paragraph("Store ID", table_cell_style),
            Paragraph("Store name, 4 store types, 4 metropolitan cities, square footage", table_cell_style)
        ],
        [
            Paragraph("<code>sku_inventory_flags</code>", table_cell_style),
            Paragraph("11,649", table_cell_style),
            Paragraph("Store ID x SKU ID", table_cell_style),
            Paragraph("Synthetic stockout and slow mover flags (Validation benchmark only)", table_cell_style)
        ]
    ]
    t_ds = Table(ds_table_data, colWidths=[95, 55, 95, 259])
    t_ds.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_ds)
    story.append(Spacer(1, 10))

    # 4. Baseline vs Machine Learning Results
    story.append(Paragraph("4. Forecasting Model Benchmarks & LightGBM Results", h1_style))
    story.append(Paragraph(
        "All models were evaluated on the strict out-of-sample chronological test set (H2 2025: 1,066,548 daily observations) using 52 engineered rolling, lag, and calendar features.",
        body_style
    ))
    
    bench_table_data = [
        [
            Paragraph("Model Architecture", table_header_style),
            Paragraph("Test WAPE", table_header_style),
            Paragraph("Test RMSE", table_header_style),
            Paragraph("Test MAE", table_header_style),
            Paragraph("Test Bias", table_header_style),
            Paragraph("Error Reduction", table_header_style)
        ],
        [
            Paragraph("Historical Global Mean", table_cell_style),
            Paragraph("68.42%", table_cell_style),
            Paragraph("2.140", table_cell_style),
            Paragraph("1.482", table_cell_style),
            Paragraph("+4.12%", table_cell_style),
            Paragraph("Baseline", table_cell_style)
        ],
        [
            Paragraph("Lag-1 Persistence", table_cell_style),
            Paragraph("58.19%", table_cell_style),
            Paragraph("1.812", table_cell_style),
            Paragraph("1.261", table_cell_style),
            Paragraph("-0.15%", table_cell_style),
            Paragraph("-14.9%", table_cell_style)
        ],
        [
            Paragraph("Lag-7 Seasonal Lag", table_cell_style),
            Paragraph("52.34%", table_cell_style),
            Paragraph("1.624", table_cell_style),
            Paragraph("1.134", table_cell_style),
            Paragraph("-0.08%", table_cell_style),
            Paragraph("-23.5%", table_cell_style)
        ],
        [
            Paragraph("28-Day Rolling SMA (Best Baseline)", table_cell_style),
            Paragraph("47.54%", table_cell_style),
            Paragraph("1.485", table_cell_style),
            Paragraph("1.030", table_cell_style),
            Paragraph("-0.04%", table_cell_style),
            Paragraph("-30.5%", table_cell_style)
        ],
        [
            Paragraph("LightGBM Model 1 (L1 Loss)", table_cell_style),
            Paragraph("43.82%", table_cell_style),
            Paragraph("1.246", table_cell_style),
            Paragraph("0.949", table_cell_style),
            Paragraph("-0.84%", table_cell_style),
            Paragraph("-35.9%", table_cell_style)
        ],
        [
            Paragraph("<b>LightGBM Model 2 (Production L2)</b>", table_cell_style),
            Paragraph("<b>42.16%</b>", table_cell_style),
            Paragraph("<b>1.183</b>", table_cell_style),
            Paragraph("<b>0.928</b>", table_cell_style),
            Paragraph("<b>-0.01%</b>", table_cell_style),
            Paragraph("<b>-38.4% (+11.3% vs SMA)</b>", table_cell_style)
        ]
    ]
    t_bench = Table(bench_table_data, colWidths=[140, 65, 65, 65, 65, 104])
    t_bench.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.HexColor("#FFFFFF"), colors.HexColor("#F8FAFC")]),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#EFF6FF")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_bench)
    story.append(Spacer(1, 10))

    # 5. Inventory Risk Scoring Breakdown
    story.append(Paragraph("5. Inventory Risk Scoring & Working Capital Audit", h1_style))
    story.append(Paragraph(
        "Applying the production forecasts across 26,408 positions revealed extreme inventory polarization across NorthBay Living's network:",
        body_style
    ))
    
    risk_table_data = [
        [
            Paragraph("Risk Classification Tier", table_header_style),
            Paragraph("Positions", table_header_style),
            Paragraph("% Network", table_header_style),
            Paragraph("Stock Units", table_header_style),
            Paragraph("Trapped Capital (Cost Basis)", table_header_style),
            Paragraph("Operational Recommendation", table_header_style)
        ],
        [
            Paragraph("CRITICAL_STOCKOUT", table_cell_style),
            Paragraph("4,239", table_cell_style),
            Paragraph("16.05%", table_cell_style),
            Paragraph("0", table_cell_style),
            Paragraph("Rs. 0.00", table_cell_style),
            Paragraph("Emergency expedited purchase order", table_cell_style)
        ],
        [
            Paragraph("HIGH_STOCKOUT_RISK", table_cell_style),
            Paragraph("970", table_cell_style),
            Paragraph("3.67%", table_cell_style),
            Paragraph("48,192", table_cell_style),
            Paragraph("Rs. 19,420,110", table_cell_style),
            Paragraph("Preemptive PO to restore safety buffer", table_cell_style)
        ],
        [
            Paragraph("MEDIUM_STOCKOUT_RISK", table_cell_style),
            Paragraph("764", table_cell_style),
            Paragraph("2.89%", table_cell_style),
            Paragraph("61,208", table_cell_style),
            Paragraph("Rs. 24,810,400", table_cell_style),
            Paragraph("Standard lead-time replenishment PO", table_cell_style)
        ],
        [
            Paragraph("HEALTHY_OPTIMAL", table_cell_style),
            Paragraph("2,444", table_cell_style),
            Paragraph("9.25%", table_cell_style),
            Paragraph("137,497", table_cell_style),
            Paragraph("Rs. 70,781,417", table_cell_style),
            Paragraph("Maintain routine monitoring", table_cell_style)
        ],
        [
            Paragraph("MEDIUM_OVERSTOCK", table_cell_style),
            Paragraph("1,899", table_cell_style),
            Paragraph("7.19%", table_cell_style),
            Paragraph("298,401", table_cell_style),
            Paragraph("Rs. 122,110,950", table_cell_style),
            Paragraph("Reduce next cycle order quantity", table_cell_style)
        ],
        [
            Paragraph("HIGH_OVERSTOCK", table_cell_style),
            Paragraph("6,708", table_cell_style),
            Paragraph("25.40%", table_cell_style),
            Paragraph("1,421,801", table_cell_style),
            Paragraph("Rs. 598,340,120", table_cell_style),
            Paragraph("Freeze purchase orders & reallocate stock", table_cell_style)
        ],
        [
            Paragraph("CRITICAL_OVERSTOCK", table_cell_style),
            Paragraph("9,384", table_cell_style),
            Paragraph("35.53%", table_cell_style),
            Paragraph("2,421,800", table_cell_style),
            Paragraph("Rs. 1,057,994,569", table_cell_style),
            Paragraph("Execute clearance markdowns (25%-35% off)", table_cell_style)
        ],
        [
            Paragraph("<b>TOTAL NETWORK</b>", table_cell_style),
            Paragraph("<b>26,408</b>", table_cell_style),
            Paragraph("<b>100.0%</b>", table_cell_style),
            Paragraph("<b>4,388,899</b>", table_cell_style),
            Paragraph("<b>Rs. 1,849,231,166</b>", table_cell_style),
            Paragraph("<b>Enterprise Working Capital Optimization</b>", table_cell_style)
        ]
    ]
    t_risk = Table(risk_table_data, colWidths=[110, 48, 48, 58, 110, 130])
    t_risk.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.HexColor("#FFFFFF"), colors.HexColor("#F8FAFC")]),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#F1F5F9")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_risk)
    story.append(Spacer(1, 10))

    # 6. Streamlit Dashboard & Decision Features
    story.append(Paragraph("6. Operational Decision Platform & Delivery", h1_style))
    story.append(Paragraph(
        "The project delivered an 8-view interactive intelligence dashboard (<code>app.py</code>) incorporating:",
        body_style
    ))
    story.append(Paragraph("• <b>Executive Overview:</b> Macro-level KPI scorecards, working capital distribution, and department exposure.", bullet_style))
    story.append(Paragraph("• <b>Priority Action Center:</b> Automated, exportable worklists for emergency POs, safety buffer restoration, clearance sales, and cross-store transfers.", bullet_style))
    story.append(Paragraph("• <b>What-If Simulator:</b> Real-time scenario planner allowing planners to test variable supplier lead times, stock buffers, and demand shifts.", bullet_style))
    story.append(Paragraph("• <b>Intelligence Assistant:</b> Natural-language data exploration engine with single-SKU explainability.", bullet_style))

    # 7. Key Findings & Business Impact
    story.append(Paragraph("7. Key Business Findings & Recommendations", h1_style))
    story.append(Paragraph("1. <b>Rs. 1.78 Billion Working Capital Liquidation:</b> 68.1% of inventory positions exceed healthy thresholds, locking up Rs. 1.78B. Immediate clearance campaigns can free up hundreds of millions of rupees in liquid capital.", bullet_style))
    story.append(Paragraph("2. <b>Preventing 5,209 Out-of-Stock Deficits:</b> Proactive replenishment using Model 2 demand forecasts eliminates lost sales on 19.7% of products.", bullet_style))
    story.append(Paragraph("3. <b>Cross-Store Rebalancing:</b> Leveraging automated inter-store stock transfers reduces overall procurement expenditures by moving excess stock from overstocked stores to out-of-stock locations.", bullet_style))

    # 8. Project Links & Verification
    story.append(Paragraph("8. Project Verification Links", h1_style))
    story.append(Paragraph("• <b>GitHub Repository:</b> https://github.com/MHK-123/Foresight", bullet_style))
    story.append(Paragraph("• <b>Web Application Source:</b> <code>app.py</code>", bullet_style))
    story.append(Paragraph("• <b>Model Artifact:</b> <code>models/lightgbm_l2_demand_forecast.joblib</code>", bullet_style))
    story.append(Paragraph("• <b>Scored Inventory Dataset:</b> <code>risk_engine_outputs/inventory_risk_scored.parquet</code>", bullet_style))
    story.append(Paragraph("• <b>Governance Documents:</b> <code>PRIVACY_POLICY.md</code> | <code>TERMS_OF_SERVICE.md</code>", bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {PDF_OUTPUT_PATH}")

if __name__ == "__main__":
    generate_pdf()
