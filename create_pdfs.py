"""
PDF Generator for creating sample documents for testing
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
from pathlib import Path


def create_sample_pdf_1(output_path: str):
    """Create first sample PDF about Artificial Intelligence"""
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='#1f77b4',
        spaceAfter=30,
        alignment=1
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor='#ff7f0e',
        spaceAfter=12,
        spaceBefore=12
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        alignment=4,
        spaceAfter=10
    )
    
    story.append(Paragraph("Artificial Intelligence: Transforming the Future", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("Introduction", heading_style))
    story.append(Paragraph(
        "Artificial Intelligence (AI) has emerged as one of the most transformative technologies of the 21st century. "
        "From healthcare to finance, education to entertainment, AI is revolutionizing virtually every aspect of human life. "
        "Machine learning algorithms, neural networks, and deep learning models are enabling computers to perform tasks that "
        "were once thought to be exclusively human domains.",
        body_style
    ))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Key Technologies", heading_style))
    story.append(Paragraph(
        "<b>Machine Learning:</b> A subset of AI that enables systems to learn and improve from experience without being explicitly programmed. "
        "Supervised learning, unsupervised learning, and reinforcement learning are the three primary paradigms. "
        "These techniques power recommendation systems, fraud detection, and predictive analytics.",
        body_style
    ))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        "<b>Deep Learning:</b> Deep neural networks with multiple layers that can automatically discover the representations needed for detection or classification. "
        "Convolutional Neural Networks (CNNs) excel at image processing, while Recurrent Neural Networks (RNNs) are ideal for sequential data.",
        body_style
    ))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Applications in Real World", heading_style))
    story.append(Paragraph(
        "AI applications span numerous industries: In healthcare, AI assists in disease diagnosis and drug discovery. "
        "In finance, it enables fraud detection and algorithmic trading. In transportation, autonomous vehicles are being developed. "
        "In retail, AI powers personalized recommendations and inventory management. The potential applications are limitless.",
        body_style
    ))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Challenges and Future Outlook", heading_style))
    story.append(Paragraph(
        "Despite tremendous progress, AI faces challenges including data privacy concerns, algorithmic bias, and the need for explainability. "
        "The future of AI lies in creating more robust, fair, and transparent systems. As AI continues to evolve, it will be crucial to ensure "
        "responsible development and deployment of these powerful technologies.",
        body_style
    ))
    
    doc.build(story)
    print(f"PDF created: {output_path}")


def create_sample_pdf_2(output_path: str):
    """Create second sample PDF about Cloud Computing"""
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='#2ca02c',
        spaceAfter=30,
        alignment=1
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor='#d62728',
        spaceAfter=12,
        spaceBefore=12
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        alignment=4,
        spaceAfter=10
    )
    
    story.append(Paragraph("Cloud Computing: The Digital Revolution", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("Overview", heading_style))
    story.append(Paragraph(
        "Cloud computing represents a fundamental shift in how we store, process, and access data and applications. "
        "Instead of relying on local servers or personal computers, users can access computing resources over the internet. "
        "This model offers flexibility, scalability, and cost-effectiveness that traditional infrastructure cannot match.",
        body_style
    ))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Service Models", heading_style))
    story.append(Paragraph(
        "<b>Infrastructure as a Service (IaaS):</b> Provides virtualized computing resources over the internet. "
        "Examples include AWS EC2, Azure VMs, and Google Compute Engine. Users manage applications and data while the provider handles infrastructure.",
        body_style
    ))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        "<b>Platform as a Service (PaaS):</b> Offers a development environment in the cloud. Developers can build, test, and deploy applications without managing underlying infrastructure. "
        "Examples include Heroku, Google App Engine, and Azure App Service.",
        body_style
    ))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        "<b>Software as a Service (SaaS):</b> Delivers applications over the internet. Users access software through web browsers without installation or maintenance. "
        "Examples include Salesforce, Microsoft 365, and Google Workspace.",
        body_style
    ))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Benefits", heading_style))
    story.append(Paragraph(
        "Cloud computing offers unprecedented scalability, allowing businesses to grow without infrastructure constraints. "
        "Cost savings through pay-as-you-go models, improved accessibility from anywhere, and automatic updates and maintenance are major advantages. "
        "Enhanced security features and disaster recovery capabilities provide peace of mind for organizations of all sizes.",
        body_style
    ))
    
    doc.build(story)
    print(f"PDF created: {output_path}")


if __name__ == "__main__":
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    create_sample_pdf_1(str(data_dir / "ai_guide.pdf"))
    create_sample_pdf_2(str(data_dir / "cloud_computing.pdf"))
    print("Sample PDFs created successfully!")
