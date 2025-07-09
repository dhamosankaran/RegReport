#!/usr/bin/env python3
"""
Create sample PDF files for testing Gemini Vector Service CLI
"""

import os
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def create_compliance_guide():
    """Create a sample compliance guide PDF"""
    
    filename = "Compliance_Guide.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1  # Center
    )
    
    story.append(Paragraph("Regulatory Compliance Guide", title_style))
    story.append(Spacer(1, 20))
    
    # Introduction
    story.append(Paragraph("Introduction", styles['Heading2']))
    intro_text = """
    This document outlines the essential compliance requirements for regulatory reporting. 
    All organizations must adhere to these standards to ensure proper governance and 
    risk management practices.
    
    The compliance framework consists of three main pillars: documentation, monitoring, 
    and reporting. Each pillar contains specific requirements that must be met on a 
    regular basis.
    """
    story.append(Paragraph(intro_text, styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Section 1
    story.append(Paragraph("1. Documentation Requirements", styles['Heading2']))
    doc_text = """
    All regulatory documents must be maintained in accordance with the following standards:
    
    • Document retention period: Minimum 7 years from date of creation
    • Version control: All documents must have proper version tracking
    • Access controls: Documents must be secured with appropriate access permissions
    • Regular reviews: Documents must be reviewed annually for accuracy and relevance
    
    Documentation should include risk assessments, policy statements, procedure manuals, 
    and training records. These documents form the foundation of the compliance program.
    """
    story.append(Paragraph(doc_text, styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Section 2
    story.append(Paragraph("2. Monitoring and Assessment", styles['Heading2']))
    monitor_text = """
    Continuous monitoring is essential for maintaining compliance. The monitoring program 
    should include:
    
    • Regular compliance assessments conducted quarterly
    • Key risk indicator (KRI) monitoring with defined thresholds
    • Internal audit programs covering all business areas
    • Exception reporting and remediation tracking
    
    Monitoring activities should be documented and reported to senior management and 
    the board of directors on a regular basis.
    """
    story.append(Paragraph(monitor_text, styles['Normal']))
    story.append(PageBreak())
    
    # Section 3
    story.append(Paragraph("3. Reporting Standards", styles['Heading2']))
    report_text = """
    Regulatory reporting must follow strict guidelines and timelines:
    
    • Monthly reports: Due by the 15th of the following month
    • Quarterly reports: Due within 45 days of quarter end
    • Annual reports: Due within 90 days of year end
    • Ad-hoc reports: As required by regulatory changes or incidents
    
    All reports must be accurate, complete, and submitted through approved channels. 
    Late submissions may result in regulatory penalties and should be avoided.
    """
    story.append(Paragraph(report_text, styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Section 4
    story.append(Paragraph("4. Training and Awareness", styles['Heading2']))
    training_text = """
    Staff training is crucial for maintaining compliance standards:
    
    • New employee orientation: Complete within 30 days of hire
    • Annual refresher training: Required for all staff
    • Specialized training: Role-specific compliance requirements
    • Training records: Maintain documentation of all completed training
    
    Training programs should be regularly updated to reflect regulatory changes and 
    emerging risks in the industry.
    """
    story.append(Paragraph(training_text, styles['Normal']))
    
    doc.build(story)
    print(f"✅ Created: {filename}")

def create_risk_management_policy():
    """Create a sample risk management policy PDF"""
    
    filename = "Risk_Management_Policy.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1
    )
    
    story.append(Paragraph("Risk Management Policy", title_style))
    story.append(Spacer(1, 20))
    
    # Purpose
    story.append(Paragraph("Purpose and Scope", styles['Heading2']))
    purpose_text = """
    This Risk Management Policy establishes the framework for identifying, assessing, 
    and managing risks across the organization. The policy applies to all business 
    units, subsidiaries, and operational activities.
    
    The primary objective is to ensure that risks are managed within acceptable 
    tolerance levels while supporting the achievement of strategic objectives.
    """
    story.append(Paragraph(purpose_text, styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Risk Framework
    story.append(Paragraph("Risk Management Framework", styles['Heading2']))
    framework_text = """
    The risk management framework consists of the following components:
    
    1. Risk Governance: Board oversight and management accountability
    2. Risk Identification: Systematic process for identifying potential risks
    3. Risk Assessment: Evaluation of likelihood and impact
    4. Risk Response: Development and implementation of mitigation strategies
    5. Risk Monitoring: Ongoing monitoring and reporting of risk metrics
    
    This framework ensures a consistent approach to risk management across all 
    business areas and provides clear accountability for risk-related decisions.
    """
    story.append(Paragraph(framework_text, styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Risk Categories
    story.append(Paragraph("Risk Categories", styles['Heading2']))
    categories_text = """
    The organization recognizes the following main risk categories:
    
    • Credit Risk: Risk of financial loss from counterparty default
    • Market Risk: Risk from changes in market prices and rates
    • Operational Risk: Risk from inadequate processes, systems, or human error
    • Liquidity Risk: Risk of inability to meet financial obligations
    • Compliance Risk: Risk of regulatory violations or sanctions
    • Reputational Risk: Risk of damage to organization's reputation
    
    Each category requires specific assessment methodologies and control measures 
    tailored to the nature of the risks involved.
    """
    story.append(Paragraph(categories_text, styles['Normal']))
    story.append(PageBreak())
    
    # Risk Appetite
    story.append(Paragraph("Risk Appetite Statement", styles['Heading2']))
    appetite_text = """
    The organization maintains a moderate risk appetite with the following principles:
    
    • Zero tolerance for compliance and regulatory violations
    • Low tolerance for reputational risks that could impact stakeholder confidence
    • Moderate tolerance for market and credit risks within defined limits
    • Balanced approach to operational risks with focus on process improvement
    
    Risk appetite is reviewed annually by the board and adjusted based on strategic 
    objectives and market conditions.
    """
    story.append(Paragraph(appetite_text, styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Responsibilities
    story.append(Paragraph("Roles and Responsibilities", styles['Heading2']))
    responsibilities_text = """
    Risk management responsibilities are distributed as follows:
    
    • Board of Directors: Overall risk governance and appetite setting
    • Senior Management: Implementation of risk strategy and policies
    • Risk Management Function: Independent risk oversight and reporting
    • Business Units: Day-to-day risk identification and management
    • Internal Audit: Independent assurance on risk management effectiveness
    
    Clear accountability ensures that risk management is embedded throughout the 
    organization and that all stakeholders understand their responsibilities.
    """
    story.append(Paragraph(responsibilities_text, styles['Normal']))
    
    doc.build(story)
    print(f"✅ Created: {filename}")

def create_data_governance_manual():
    """Create a sample data governance manual PDF"""
    
    filename = "Data_Governance_Manual.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1
    )
    
    story.append(Paragraph("Data Governance Manual", title_style))
    story.append(Spacer(1, 20))
    
    # Overview
    story.append(Paragraph("Data Governance Overview", styles['Heading2']))
    overview_text = """
    Data governance is the overall management of data availability, usability, integrity, 
    and security in an enterprise. This manual establishes the policies, procedures, 
    and standards for effective data management across the organization.
    
    The data governance program ensures that data is treated as a strategic asset and 
    that data-related decisions support business objectives while maintaining regulatory 
    compliance and data quality standards.
    """
    story.append(Paragraph(overview_text, styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Data Classification
    story.append(Paragraph("Data Classification Framework", styles['Heading2']))
    classification_text = """
    All organizational data is classified into the following categories:
    
    • Public: Information that can be freely shared without restriction
    • Internal: Information for internal use that should not be shared externally
    • Confidential: Sensitive information requiring special handling procedures
    • Restricted: Highly sensitive information with limited access requirements
    
    Data classification determines the appropriate security controls, access restrictions, 
    and handling procedures that must be applied to protect the information.
    """
    story.append(Paragraph(classification_text, styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Data Quality
    story.append(Paragraph("Data Quality Standards", styles['Heading2']))
    quality_text = """
    Data quality is measured across six key dimensions:
    
    1. Accuracy: Data correctly represents the real-world entity or event
    2. Completeness: All required data elements are present
    3. Consistency: Data is uniform across different systems and formats
    4. Timeliness: Data is current and available when needed
    5. Validity: Data conforms to defined formats and business rules
    6. Uniqueness: Data records are not duplicated inappropriately
    
    Regular data quality assessments are conducted to identify and remediate quality 
    issues that could impact business decisions or regulatory reporting.
    """
    story.append(Paragraph(quality_text, styles['Normal']))
    
    doc.build(story)
    print(f"✅ Created: {filename}")

def main():
    """Create all sample PDF files"""
    print("🚀 Creating Sample PDF Files for Gemini CLI Testing")
    print("=" * 50)
    
    try:
        create_compliance_guide()
        create_risk_management_policy()
        create_data_governance_manual()
        
        print("\n✅ All sample PDFs created successfully!")
        print("\n📋 Files created:")
        print("  • Compliance_Guide.pdf")
        print("  • Risk_Management_Policy.pdf")
        print("  • Data_Governance_Manual.pdf")
        
        print("\n🧪 Now you can test the CLI with these commands:")
        print("  python gemini_cli.py load *.pdf")
        print("  python gemini_cli.py query \"What are the compliance requirements?\"")
        print("  python gemini_cli.py interactive")
        
    except ImportError:
        print("❌ Error: reportlab library is required")
        print("Install it with: pip install reportlab")
    except Exception as e:
        print(f"❌ Error creating PDFs: {str(e)}")

if __name__ == "__main__":
    main() 