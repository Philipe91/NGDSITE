"""Final fix: remove the orphan line 6 in product_detail.html"""
path = r'c:\Users\Pc Fechamento\Documents\NGDSITE\templates\catalog\product_detail.html'

with open(path, encoding='utf-8') as f:
    lines = f.readlines()

print("BEFORE:")
for i, line in enumerate(lines[4:9], start=5):
    print(f"  L{i}: {repr(line[:80])}")

# Line 5 (index 4): correct meta_title  ✓
# Line 6 (index 5): ORPHAN "product.short_description..." <- DELETE
# Line 7 (index 6): empty line keeping
# Lines 8+ are the rest of the template

# Verify line 6 is the orphan before deleting
if lines[5].startswith('product.short_description'):
    del lines[5]
    print("\nOrphan line 6 deleted!")
else:
    print(f"\nlinha 6 nao e orphan: {repr(lines[5])}")

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\nAFTER (lines 4-8):")
with open(path, encoding='utf-8') as f:
    corrected = f.readlines()
for i, line in enumerate(corrected[3:9], start=4):
    print(f"  L{i}: {repr(line[:100])}")
print("\nAll done!")
