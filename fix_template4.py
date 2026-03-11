"""Final: Ensure both meta_title and meta_description are clean single lines."""
path = r'c:\Users\Pc Fechamento\Documents\NGDSITE\templates\catalog\product_detail.html'

with open(path, encoding='utf-8') as f:
    lines = f.readlines()

print("CURRENT lines 3-8:")
for i, line in enumerate(lines[2:8], start=3):
    print(f"  L{i}: {repr(line[:120])}")

# After all the edits, the file should now have:
# Line 3: {% block title %}...{% endblock %}
# Line 4: (blank)
# Line 5: {% block meta_title %}...{% endblock %}
# Line 6: (blank)  <- need to insert meta_description here
# Line 7: {% block content %}

# Check if meta_description is missing
has_meta_desc = any('block meta_description' in l for l in lines[:15])
print(f"\nmeta_description present? {has_meta_desc}")

if not has_meta_desc:
    # Insert it after line 5 (index 5)
    meta_desc_line = "{% block meta_description %}{% if product.meta_description %}{{ product.meta_description }}{% else %}{{ product.short_description|truncatechars:160 }}{% endif %}{% endblock %}\n"
    lines.insert(5, meta_desc_line)
    print("Inserted meta_description block at line 6")

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\nFINAL lines 1-10:")
with open(path, encoding='utf-8') as f:
    corrected = f.readlines()
for i, line in enumerate(corrected[:10], start=1):
    print(f"  L{i}: {repr(line[:120])}")
