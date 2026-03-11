"""Final definitive fix: rewrite the exact broken line 5 for meta_title."""
path = r'c:\Users\Pc Fechamento\Documents\NGDSITE\templates\catalog\product_detail.html'

with open(path, encoding='utf-8') as f:
    lines = f.readlines()

# Check line 5 (index 4)
print("Line 5:", repr(lines[4]))

# It ends with {% endif\n -- the %} is missing, fix it
if lines[4].rstrip('\n').endswith('{% endif'):
    lines[4] = lines[4].rstrip('\n').rstrip('{% endif') + '{% endif %}{% endblock %}\n'
    print("Fixed line 5!")
elif '{% endif %}{% endblock %}' not in lines[4]:
    # Brutal replacement: just write the correct line
    lines[4] = "{% block meta_title %}{% if product.meta_title %}{{ product.meta_title }}{% else %}{{ product.name }} - NGD Site{% endif %}{% endblock %}\n"
    print("Replaced line 5 completely!")
else:
    print("Line 5 already looks correct:")

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\nFINAL lines 1-9:")
with open(path, encoding='utf-8') as f:
    corrected = f.readlines()
for i, line in enumerate(corrected[:9], start=1):
    print(f"  L{i}: {repr(line[:130])}")

# Django template check
import subprocess, sys
result = subprocess.run([sys.executable, 'manage.py', 'check'], capture_output=True, text=True, cwd=r'c:\Users\Pc Fechamento\Documents\NGDSITE')
print("\nDjango check output:")
print(result.stdout or result.stderr)
