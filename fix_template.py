"""Fix the broken meta tag lines in product_detail.html"""
path = r'c:\Users\Pc Fechamento\Documents\NGDSITE\templates\catalog\product_detail.html'

with open(path, encoding='utf-8') as f:
    content = f.read()

# The broken version (with \r\n inside the tags)
broken_meta_title = (
    "{% block meta_title %}{% if product.meta_title %}{{ product.meta_title }}"
    "{% else %}{{ product.name }} - NGD Site{% endif\r\n"
    "%}{% endblock %}"
)
fixed_meta_title = (
    "{% block meta_title %}{% if product.meta_title %}{{ product.meta_title }}"
    "{% else %}{{ product.name }} - NGD Site{% endif %}{% endblock %}"
)

broken_meta_desc = (
    "{% block meta_description %}{% if product.meta_description %}{{ product.meta_description }}"
    "{% else %}{{\r\nproduct.short_description|truncatechars:160 }}{% endif %}{% endblock %}"
)
fixed_meta_desc = (
    "{% block meta_description %}{% if product.meta_description %}{{ product.meta_description }}"
    "{% else %}{{ product.short_description|truncatechars:160 }}{% endif %}{% endblock %}"
)

if broken_meta_title in content:
    content = content.replace(broken_meta_title, fixed_meta_title)
    print("Fixed meta_title block!")
else:
    print("ERROR: meta_title pattern not found — check the file manually")

if broken_meta_desc in content:
    content = content.replace(broken_meta_desc, fixed_meta_desc)
    print("Fixed meta_description block!")
else:
    print("ERROR: meta_description pattern not found — check the file manually")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
with open(path, encoding='utf-8') as f:
    lines = f.readlines()

print("\nLines 5-8 after fix:")
for i, line in enumerate(lines[4:8], start=5):
    print(f"  L{i}: {repr(line)}")
