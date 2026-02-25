import yaml
import sys
import os
from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright

def deep_merge(base, override):
    """Recursively merge override dictionary into base dictionary."""
    for key, value in override.items():
        if isinstance(value, dict) and key in base and isinstance(base[key], dict):
            deep_merge(base[key], value)
        else:
            base[key] = value
    return base

def main(variant_file=None):
    print("[1/5] Loading base.yaml...")
    with open('data/base.yaml', 'r') as f:
        data = yaml.safe_load(f)

    if variant_file and os.path.exists(variant_file):
        print(f"[2/5] Loading and merging variant: {variant_file}...")
        with open(variant_file, 'r') as f:
            variant_data = yaml.safe_load(f)
            # Failsafe in case the variant YAML is empty
            if variant_data: 
                data = deep_merge(data, variant_data)
        out_name = os.path.basename(variant_file).replace('.yaml', '.pdf')
    else:
        print("[2/5] No variant provided. Building base resume...")
        out_name = 'resume_base.pdf'

    print("[3/5] Rendering HTML with Jinja2...")
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('resume.html')
    html_out = template.render(data)
    
    with open('output.html', 'w') as f:
        f.write(html_out)

    print("[4/5] Launching Playwright to generate PDF...")
    output_dir = 'dist'
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, out_name)

    with sync_playwright() as p:
        # Added Linux-friendly arguments to prevent silent hangs
        browser = p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])
        page = browser.new_page()
        
        print("[4.5/5] Loading HTML content into browser...")
        # domcontentloaded prevents hanging on phantom network requests
        page.set_content(html_out, wait_until="domcontentloaded") 
        
        print("[5/5] Printing to PDF...")
        page.pdf(path=pdf_path, format="A4", print_background=True, margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
        browser.close()

    print(f"✅ Successfully generated {pdf_path}")

if __name__ == "__main__":
    variant = sys.argv[1] if len(sys.argv) > 1 else None
    main(variant)
