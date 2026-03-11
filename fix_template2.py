"""Fix broken meta tag lines 5-8 in product_detail.html by line number"""
path = r'c:\Users\Pc Fechamento\Documents\NGDSITE\templates\catalog\product_detail.html'

with open(path, encoding='utf-8') as f:
    lines = f.readlines()

print("BEFORE:")
for i, line in enumerate(lines[4:8], start=5):
    print(f"  L{i}: {repr(line)}")

# Overwrite lines 5-8 (index 4-7) with the correct single-line versions
lines[4] = "{% block meta_title %}{% if product.meta_title %}{{ product.meta_title }}{% else %}{{ product.name }} - NGD Site{% endif %}{% endblock %}\n"
lines[5] = "{% block meta_description %}{% if product.meta_description %}{{ product.meta_description }}{% else %}{{ product.short_description|truncatechars:160 }}{% endif %}{% endblock %}\n"

# Remove the now-orphan lines 6 and 7 (old continuation lines)
# Lines are now: 4=meta_title(fixed), 5=meta_desc(fixed), 6=old "%}{% endblock %}", 7=old meta_desc broken, 8=old continuation
# After our writes, lines 4 and 5 are fixed. Lines 5 (old index 5) is now "meta_description" and the old lines 6,7 are orphans.
# We need to delete the original lines at index 5,6,7 which were the continuation parts.
# Actually, we replaced index 4 & 5. The old lines 6 (index 5) = "%}{% endblock %}\n" and old line 7 (index 6) which had broken meta_desc opening
# and old line 8 (index 7) = "product.short_description..."
# So now we need to delete original indices 5 (old "%}...") and 6-7 (old meta_desc continuation)
del lines[6]  # delete "product.short_description..." continuation
del lines[5]  # delete "%}{% endblock %}" orphan

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\nAFTER:")
with open(path, encoding='utf-8') as f:
    corrected = f.readlines()
for i, line in enumerate(corrected[4:9], start=5):
    print(f"  L{i}: {repr(line)}")
print("\nDone!")
