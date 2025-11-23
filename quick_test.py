#!/usr/bin/env python3
"""
Quick validation of scoring logic
"""
import sys
sys.path.insert(0, '.')

try:
    from content_scoring import score_content_structure, extract_keywords
    
    sample = """Hello everyone, myself Muskan, studying in class 8th B section from Christ Public School. 
I am 13 years old. I live with my family. There are 3 people in my family, me, my mother and my father.
One special thing about my family is that they are very kind hearted to everyone and soft spoken. One thing I really enjoy is play, playing cricket and taking wickets.
A fun fact about me is that I see in mirror and talk by myself. One thing people don't know about me is that I once stole a toy from one of my cousin.
 My favorite subject is science because it is very interesting. Through science I can explore the whole world and make the discoveries and improve the lives of others. 
Thank you for listening."""
    
    print("Testing Content Scoring...")
    result = score_content_structure(sample)
    print(f"✓ Content Score: {result['total']}/40")
    
    keywords = extract_keywords(sample)
    print(f"✓ Keywords Found - Must Have: {len(keywords['must_have'])}, Good to Have: {len(keywords['good_to_have'])}")
    
    print("\n✓ All modules working correctly!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
