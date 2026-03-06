import fitz
import re
import json

doc = fitz.open(r'c:\Users\vanch\Documents\Antigravity\IvanRosP.github.io\html\RHOF\act08-Equipo2.pdf')
text = "\n".join(page.get_text() for page in doc)

# Pattern to capture:
# 1. 2. etc followed by arbitrary text until we see "• Nivel:" or "•\nNivel:"
# then we capture Nivel
# then we capture Tipo de SQLi
# Because the title can span multiple lines, we can use a regex that matches the number, 
# then non-greedy matches everything until Nivel

pattern = re.compile(r'\n(\d{1,2})\.\s+(.*?)\n\s*•\s*\n*Nivel:\s*([^\n]+).*?Tipo de SQLi:\s*([^\n]+)', re.DOTALL)

matches = pattern.finditer(text)

labs = []
for m in matches:
    num = m.group(1).strip()
    title = m.group(2).strip().replace('\n', ' ')
    nivel = m.group(3).strip()
    tipo = m.group(4).strip()
    
    # Optional: clean up extra spaces in title
    title = re.sub(r'\s+', ' ', title)
    
    labs.append({
        "num": num,
        "title": title,
        "nivel": nivel,
        "tipo": tipo
    })

print(f"Encontrados {len(labs)} laboratorios.")
for l in labs:
    print(l)

with open(r'c:\Users\vanch\Documents\Antigravity\IvanRosP.github.io\html\RHOF\labs.json', 'w', encoding='utf-8') as f:
    json.dump(labs, f, indent=4, ensure_ascii=False)
