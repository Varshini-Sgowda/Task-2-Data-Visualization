"""
SUPERSCOPE Visual Report PDF Compiler
Compiles all high-resolution storyboard dashboards into a single multi-page executive PDF report.
Elevate Labs Data Analyst Internship - Task 2: Data Visualization and Storytelling
"""

import os
from PIL import Image

def compile_pdf():
    img_paths = [
        'dashboard/dashboard_screenshots/01_executive_overview.png',
        'dashboard/dashboard_screenshots/02_sales_profit_story.png',
        'dashboard/dashboard_screenshots/03_category_product_drivers.png',
        'dashboard/dashboard_screenshots/04_geographic_expansion.png',
        'dashboard/dashboard_screenshots/05_customer_deep_dive.png',
        'dashboard/dashboard_screenshots/06_opportunity_radar.png'
    ]
    
    images = []
    for p in img_paths:
        if os.path.exists(p):
            img = Image.open(p).convert('RGB')
            images.append(img)
        else:
            print(f"Warning: {p} not found.")

    if images:
        os.makedirs('dashboard/exported_report', exist_ok=True)
        out_pdf = 'dashboard/exported_report/Superscope_Visual_Report.pdf'
        images[0].save(out_pdf, save_all=True, append_images=images[1:], quality=95)
        print(f"Successfully generated multi-page PDF report: {out_pdf} ({os.path.getsize(out_pdf):,} bytes)")
    else:
        print("No images found to compile.")

if __name__ == '__main__':
    compile_pdf()
