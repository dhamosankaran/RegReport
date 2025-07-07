#!/usr/bin/env python3
"""
Test script for PDF loader functionality
Creates sample PDF files and tests the loading process
"""

import os
import sys
import asyncio
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from load_pdfs_to_vector_db import PDFLoader
from app.utils.logging_config import setup_logging, get_logger

# Setup logging
setup_logging(log_level="INFO", log_dir="logs")
logger = get_logger("pdf_loader_test")

def create_sample_pdf(filename: str, content: str, title: str = "Sample Document"):
    """Create a sample PDF file with given content"""
    try:
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Add title
        title_style = styles['Title']
        story.append(Paragraph(title, title_style))
        story.append(Spacer(1, 12))
        
        # Add content paragraphs
        normal_style = styles['Normal']
        paragraphs = content.split('\n\n')
        
        for paragraph in paragraphs:
            if paragraph.strip():
                story.append(Paragraph(paragraph.strip(), normal_style))
                story.append(Spacer(1, 12))
        
        doc.build(story)
        logger.info(f"Created sample PDF: {filename}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to create PDF {filename}: {str(e)}")
        return False

async def test_pdf_loader():
    """Test the PDF loader functionality"""
    try:
        # Create sample PDF files
        project_root = Path(__file__).parent.parent
        
        # Sample content for Instructions.pdf
        instructions_content = """
        REGULATORY COMPLIANCE INSTRUCTIONS
        
        Section 1: General Requirements
        All organizations must comply with the following regulatory requirements:
        
        1.1 Data Protection Requirements
        Personal data must be protected according to established privacy regulations.
        Organizations shall implement appropriate technical and organizational measures.
        
        1.2 Security Procedures
        Security procedures must be documented and regularly reviewed.
        Access controls shall be implemented for all systems handling sensitive data.
        
        Section 2: Compliance Monitoring
        Regular compliance audits must be conducted to ensure ongoing adherence.
        
        2.1 Audit Schedule
        Compliance audits shall be performed at least annually.
        Additional audits may be required based on risk assessment.
        
        2.2 Reporting Requirements
        All compliance violations must be reported within 24 hours of discovery.
        Corrective actions must be documented and implemented promptly.
        
        Section 3: Training and Awareness
        All personnel must receive appropriate training on compliance requirements.
        Training records must be maintained and updated regularly.
        """
        
        # Sample content for Rules.pdf
        rules_content = """
        REGULATORY COMPLIANCE RULES
        
        Rule 1: Data Handling
        All data must be classified according to sensitivity levels.
        Confidential data requires encryption both in transit and at rest.
        
        Rule 2: Access Control
        User access must be granted on a need-to-know basis.
        Multi-factor authentication is required for administrative access.
        
        Rule 3: Incident Response
        Security incidents must be contained within 1 hour of detection.
        Affected parties must be notified within 72 hours.
        
        Rule 4: Documentation
        All procedures must be documented and approved by management.
        Documentation must be reviewed and updated annually.
        
        Rule 5: Third-Party Management
        Third-party vendors must undergo security assessments.
        Contracts must include appropriate security requirements.
        
        Rule 6: Monitoring and Logging
        All system access must be logged and monitored.
        Log retention period is minimum 12 months.
        """
        
        # Create PDF files
        instructions_pdf = project_root / "Instructions.pdf"
        rules_pdf = project_root / "Rules.pdf"
        
        logger.info("Creating sample PDF files...")
        
        success1 = create_sample_pdf(
            str(instructions_pdf), 
            instructions_content, 
            "Regulatory Compliance Instructions"
        )
        
        success2 = create_sample_pdf(
            str(rules_pdf), 
            rules_content, 
            "Regulatory Compliance Rules"
        )
        
        if not (success1 and success2):
            logger.error("Failed to create sample PDF files")
            return False
        
        # Test the PDF loader
        logger.info("Testing PDF loader...")
        
        loader = PDFLoader()
        await loader.initialize()
        
        # Test loading default PDFs
        logger.info("Loading default PDF files...")
        await loader.load_default_pdfs()
        
        # Check status
        logger.info("Checking document status...")
        await loader.get_status()
        
        # Test reload functionality
        logger.info("Testing reload functionality...")
        await loader.reload_all_documents()
        
        # Final status check
        logger.info("Final status check...")
        await loader.get_status()
        
        await loader.close()
        
        logger.info("🎉 PDF loader test completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        return False

async def cleanup_test_files():
    """Clean up test PDF files"""
    try:
        project_root = Path(__file__).parent.parent
        test_files = [
            project_root / "Instructions.pdf",
            project_root / "Rules.pdf"
        ]
        
        for file_path in test_files:
            if file_path.exists():
                file_path.unlink()
                logger.info(f"Removed test file: {file_path}")
        
        logger.info("Test cleanup completed")
        
    except Exception as e:
        logger.error(f"Cleanup failed: {str(e)}")

async def main():
    """Main test function"""
    print("🧪 PDF Loader Test Suite")
    print("=" * 50)
    
    try:
        # Run the test
        success = await test_pdf_loader()
        
        if success:
            print("\n✅ All tests passed!")
            
            # Ask if user wants to keep the test files
            response = input("\nKeep the sample PDF files? (y/n): ").lower().strip()
            if response != 'y':
                await cleanup_test_files()
        else:
            print("\n❌ Tests failed!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
        await cleanup_test_files()
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test suite failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 