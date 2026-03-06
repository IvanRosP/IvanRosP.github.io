import fitz
import re
import json

doc = fitz.open(r'c:\Users\vanch\Documents\Antigravity\IvanRosP.github.io\html\RHOF\act08-Equipo2.pdf')
text = "\n".join(page.get_text() for page in doc)

# Find all occurrences of "Nivel: " and the title preceding it.
# The labs all have "Nivel:" and "Tipo de SQLi:"
labs = []
pattern = re.compile(r'\n(\d{1,2})\.\s+(.*?)\n.*?Nivel:\s*([^\n]+).*?Tipo de SQLi:\s*([^\n]+)', re.DOTALL)

# A safer approach:
# Split by "\nNivel:"
blocks = text.split("Nivel:")
for i in range(1, len(blocks)):
    prev_block = blocks[i-1]
    curr_block = blocks[i]
    
    # 1. Extract the Lab Number and Title from the END of prev_block
    # We look for \n [digits] . [Title] \n • \n (or similar)
    title_match = re.search(r'\n(\d{1,2})\.\s+(.*?)$', prev_block.strip() + "\n", re.DOTALL)
    if not title_match:
        # try without strict ending
        title_match = re.search(r'\n(\d{1,2})\.\s+(.*?)(?:\n\s*•\s*)?$', prev_block, re.DOTALL)
        
    if title_match:
        num = title_match.group(1).strip()
        title = title_match.group(2).strip()
        title = re.sub(r'•\s*$', '', title).strip() # remove bullet if matched
        title = re.sub(r'\s+', ' ', title)
        
        # 2. Extract Nivel from START of curr_block
        nivel_match = re.search(r'^\s*([^\n]+)', curr_block)
        nivel = nivel_match.group(1).strip() if nivel_match else "Desconocido"
        
        # 3. Extract Tipo from curr_block
        tipo_match = re.search(r'Tipo de SQLi:\s*([^\n]+)', curr_block)
        tipo = tipo_match.group(1).strip() if tipo_match else "Desconocido"
        
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
