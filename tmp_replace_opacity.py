import glob
for f in glob.glob('c:/Users/mohanarangan/VendorFlow-AI-Autonomous-Vendor-Onboarding-Agent/vendorflow/ui/pages/*.py'):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    content = content.replace('inject_css()', 'inject_css(overlay_opacity="0.94")')
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
print("Opacity updated in subpages.")
