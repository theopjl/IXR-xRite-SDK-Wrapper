"""
Example script for ColorChecker template generation

This script generates a PDF template with ArUco markers for ColorChecker detection.
"""

import sys
import os

# Add src directory to path for importing xRite package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from xRite import create_pdf_template, COLORCHECKER_SPECS


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate ColorChecker detection template with ArUco markers')
    parser.add_argument('--type', '-t', 
                       choices=['classic', 'digitalsg'],
                       default='classic',
                       help='Type of ColorChecker (classic or digitalsg)')
    parser.add_argument('--output', '-o',
                       default='colorchecker_template.pdf',
                       help='Output PDF file path')
    
    args = parser.parse_args()
    
    print(f"Generating template for {COLORCHECKER_SPECS[args.type]['name']}...")
    create_pdf_template(args.type, args.output)
    print(f"Template saved to: {args.output}")


if __name__ == '__main__':
    main()
