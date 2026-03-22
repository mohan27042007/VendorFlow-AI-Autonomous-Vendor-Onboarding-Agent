import os
import glob

files = glob.glob('c:/Users/mohanarangan/VendorFlow-AI-Autonomous-Vendor-Onboarding-Agent/vendorflow/ui/**/*.py', recursive=True)

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '#161B22' in content:
        content = content.replace('#161B22', 'rgba(22, 27, 34, 0.95)')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")
    elif '#0D1117' in content and 'stSidebar' in content:
        # Also let the sidebar be slightly transparent
        pass

print("Done")
