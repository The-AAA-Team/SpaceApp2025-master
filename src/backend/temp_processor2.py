#!/usr/bin/env python3
import json
import re
from pathlib import Path
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO, 
                   format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

def extract_sections(text):
    """Extract sections from the text using bullet points."""
    if not text:
        return []
    
    # Split on bullet points (both * and -)
    bullet_pattern = r'\n\s*[*-]\s*'
    sections = re.split(bullet_pattern, text)
    
    # Remove empty sections and clean up
    sections = [s.strip() for s in sections if s.strip()]
    return sections

def infer_title(text):
    """Try to infer a title from the first few lines."""
    if not text:
        return ""
    
    # Look for research purpose or first section
    lines = text.split('\n')
    for line in lines[:10]:  # Check first 10 lines
        # Look for sections about research purpose
        if 'research purpose' in line.lower():
            # Clean up markdown and extra whitespace
            title = re.sub(r'[*_#]', '', line)
            title = re.sub(r'research purpose:?\s*', '', title, flags=re.I)
            return title.strip()
            
    # Fallback: return first non-empty line
    for line in lines:
        if line.strip():
            # Clean up markdown and extra whitespace
            title = re.sub(r'[*_#]', '', line)
            return title.strip()
            
    return ""

def extract_author(text):
    """Look for author mentions in the text."""
    if not text:
        return ""
        
    # Common patterns for author mentions
    patterns = [
        r'by\s+([^,.]+)',
        r'authors?:?\s+([^,.]+)',
        r'researchers?:?\s+([^,.]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.I)
        if match:
            return match.group(1).strip()
            
    return ""

def enrich_data(summary_data):
    """Extract structured information from a summary."""
    # Handle both string and object formats
    if isinstance(summary_data, dict):
        text = summary_data.get('summary', '')
        url = summary_data.get('url', '')
    else:
        text = summary_data
        url = ''
        
    if not isinstance(text, str):
        logger.error(f"Expected string for summary, got {type(text)}")
        return None
        
    if not text.strip():
        logger.warn(f"Empty summary")
        return None

    # Extract information
    return {
        'title': infer_title(text),
        'author': extract_author(text),
        'sections': extract_sections(text),
        'url': url,
        'original_summary': text
    }

def main():
    """Process the data file and generate enriched data."""
    logger.debug("Starting data enrichment...")
    
    # File paths
    script_dir = Path(__file__).parent.absolute()
    input_path = script_dir / 'data.json'
    output_path = script_dir / 'processed_data.json'
    
    logger.debug(f"Reading from {input_path}")
    
    # Read data
    with open(input_path, 'r') as f:
        data = json.load(f)
        
    logger.debug(f"Loaded {len(data)} records")
    if data:
        logger.debug(f"First record type: {type(data[0])}")
        if isinstance(data[0], str):
            logger.debug(f"First string length: {len(data[0])}")

    # Process records
    enriched_data = []
    processed_count = 0
    
    for i, record in enumerate(data):
        # Process every 10th record
        if i > 0 and i % 10 == 0:
            logger.info(f"Processed {i}/{len(data)} records...")
            
        # Enrich the data
        enriched = enrich_data(record)
        if enriched:
            enriched_data.append(enriched)
            processed_count += 1

    # Save results
    with open(output_path, 'w') as f:
        json.dump(enriched_data, f, indent=2)
        
    logger.info(f"✅ Enriched {processed_count} summaries → {output_path}")

if __name__ == '__main__':
    main()
