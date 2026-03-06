import fitz
import json
import re

doc = fitz.open(r'c:\Users\vanch\Documents\Antigravity\IvanRosP.github.io\html\RHOF\act08-Equipo2.pdf')
text = "\n".join(page.get_text() for page in doc)

lines = text.split('\n')

labs = []
current_lab = None

for i in range(len(lines)):
    line = lines[i].strip()
    match = re.match(r'^(\d{1,2})\.\s+(.*)', line)
    
    if match and ("SQL" in line or "injection" in line or "attack" in line or "vulnerability" in line):
        num = match.group(1)
        title = match.group(2)
        if i + 1 < len(lines):
            next_line = lines[i+1].strip()
            if next_line and not next_line.startswith('•') and not next_line.startswith('Nivel:'):
                title += " " + next_line
                
        if current_lab:
            labs.append(current_lab)
            
        current_lab = {
            "num": num,
            "title": title,
            "nivel": "Desconocido",
            "tipo": "Desconocido",
            "content": []
        }
        continue
        
    if current_lab:
        if "Road To Hall of Fame" in line or line.isdigit() or "Capturas de pantalla" in line:
            continue
        if line.startswith('Nivel:'):
            current_lab['nivel'] = line.replace('Nivel:', '').strip()
            continue
        if line.startswith('Tipo de SQLi:'):
            current_lab['tipo'] = line.replace('Tipo de SQLi:', '').strip()
            continue
        if line.lower().startswith('conclusiones'):
            labs.append(current_lab)
            current_lab = None
            continue
        if line:
            current_lab["content"].append(line)

if current_lab and current_lab not in labs:
    labs.append(current_lab)

final_labs = []
seen_nums = set()
for l in labs:
    if l['num'] not in seen_nums:
        full_text = " ".join(l["content"]).replace('• Nivel', '').replace('• Tipo', '').replace('• Objetivo', '<br><br><strong>Objetivo:</strong>').replace('Explicación técnica', '<br><br><strong>Explicación técnica:</strong>').replace('Procedimiento paso a paso:', '<br><br><strong>Procedimiento paso a paso:</strong>').replace('Explicación del payload:', '<br><br><strong>Explicación del payload:</strong>').replace('Mitigación recomendada:', '<br><br><strong>Mitigación recomendada:</strong>').replace('•', '<br>•')
        l["full_content"] = full_text.strip()
        final_labs.append(l)
        seen_nums.add(l['num'])

html_content = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Road To Hall Of Fame (SQL Injection)</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../../estilo/actividades.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f8fafc;
        }
        
        .labs-container {
            max-width: 900px;
            margin: 40px auto;
            padding: 0 20px;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .lab-card {
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            overflow: hidden;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            border: 1px solid #e2e8f0;
        }
        
        .lab-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            border-color: #cbd5e1;
        }

        .lab-header {
            padding: 24px;
            border-bottom: 1px solid #f1f5f9;
            background: linear-gradient(to right, #ffffff, #f8fafc);
        }

        .lab-title-wrapper {
            display: flex;
            align-items: flex-start;
            gap: 16px;
            margin-bottom: 16px;
        }

        .lab-badge {
            flex-shrink: 0;
            background: #2563eb;
            color: white;
            padding: 6px 14px;
            border-radius: 999px;
            font-weight: 600;
            font-size: 0.9rem;
            box-shadow: 0 2px 4px rgba(37, 99, 235, 0.2);
        }

        .lab-card h3 {
            margin: 0;
            color: #1e293b;
            font-size: 1.25rem;
            line-height: 1.4;
            font-weight: 700;
        }

        .lab-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            font-size: 0.9rem;
        }
        
        .meta-tag {
            display: inline-flex;
            align-items: center;
            background-color: #f1f5f9;
            color: #475569;
            padding: 4px 12px;
            border-radius: 6px;
            font-weight: 500;
            border-left: 3px solid #f59e0b;
        }
        
        .meta-tag strong {
            margin-right: 6px;
            color: #334155;
        }

        /* Modern Accordion */
        details {
            background: #ffffff;
        }

        summary {
            padding: 16px 24px;
            font-weight: 600;
            color: #3b82f6;
            cursor: pointer;
            list-style: none; /* Hide default arrow */
            user-select: none;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.2s ease;
        }
        
        summary:hover {
            background-color: #f8fafc;
            color: #2563eb;
        }

        summary::-webkit-details-marker {
            display: none;
        }

        summary::after {
            content: '';
            width: 12px;
            height: 12px;
            border-right: 2px solid currentColor;
            border-bottom: 2px solid currentColor;
            transform: translateY(-2px) rotate(45deg);
            transition: transform 0.3s ease;
        }

        details[open] summary::after {
            transform: translateY(2px) rotate(-135deg);
        }
        
        details[open] summary {
            border-bottom: 1px solid #e2e8f0;
            background-color: #f8fafc;
        }

        .details-content {
            padding: 24px;
            font-size: 0.95rem;
            line-height: 1.7;
            color: #475569;
            background: #ffffff;
        }
        
        .details-content strong {
            color: #1e293b;
            font-size: 1rem;
            display: inline-block;
            margin-top: 8px;
        }

        .download-section {
            text-align: center;
            margin: 60px auto 40px auto;
            max-width: 800px;
            padding: 40px;
            background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
            border-radius: 16px;
            color: white;
            box-shadow: 0 20px 25px -5px rgba(37, 99, 235, 0.2), 0 10px 10px -5px rgba(37, 99, 235, 0.1);
        }
        
        .download-section h2 {
            border: none;
            color: white;
            margin-top: 0;
            font-size: 1.8rem;
            margin-bottom: 16px;
        }
        
        .download-section p {
            font-size: 1.1rem;
            opacity: 0.9;
            margin-bottom: 30px;
        }
        
        .btn-download {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            background-color: #f59e0b;
            color: #fff;
            padding: 16px 32px;
            text-decoration: none;
            border-radius: 999px;
            font-weight: 700;
            font-size: 1.1rem;
            transition: all 0.3s ease;
            box-shadow: 0 10px 15px -3px rgba(245, 158, 11, 0.4);
        }
        
        .btn-download:hover {
            background-color: #d97706;
            transform: translateY(-3px);
            box-shadow: 0 20px 25px -5px rgba(245, 158, 11, 0.5);
        }
        
        .header-subtitle {
            font-size: 1.25rem;
            opacity: 0.9;
            margin-bottom: 24px;
        }
    </style>
</head>
<body>

<header>
    <h1>ROAD TO HALL OF FAME</h1>
    <p class="header-subtitle">SQL Injection (PortSwigger Web Security Academy)</p>
    <p><strong>Seguridad Informática II - Equipo 2</strong></p>
</header>

<div class="container" style="background: transparent; box-shadow: none; padding: 20px 0;">
    
    <div style="text-align: center; margin-bottom: 40px;">
        <h2 style="border: none; text-align: center; margin-bottom: 16px; font-size: 2.5rem; color: #1e293b; font-weight: 800;">Laboratorios Completados</h2>
        <p style="font-size: 1.15rem; color: #64748b; max-width: 700px; margin: 0 auto; line-height: 1.6;">
            Documentación estructurada de los 16 laboratorios sobre inyección SQL,
            abarcando desde las técnicas fundamentales (In-band) hasta vulnerabilidades avanzadas (Blind y OAST). 
        </p>
    </div>

    <div class="labs-container">
"""

def sanitize_html(text):
    text = text.replace('Nivel:  Apprentice', '').replace('Nivel:  Practitioner', '')
    text = text.replace('Tipo de SQLi:  In-band (Basada en lógica booleana)', '')
    # Convert newlines to br if not already
    text = text.replace('  ', ' ')
    return text

for lab in final_labs:
    content_html = sanitize_html(lab.get('full_content', 'Contenido no disponible.'))
    
    html_content += f"""
        <article class="lab-card">
            <div class="lab-header">
                <div class="lab-title-wrapper">
                    <span class="lab-badge">Lab {lab['num']}</span>
                    <h3>{lab['title']}</h3>
                </div>
                <div class="lab-meta">
                    <span class="meta-tag"><strong>Nivel:</strong> {lab['nivel']}</span>
                    <span class="meta-tag"><strong>Tipo:</strong> {lab['tipo']}</span>
                </div>
            </div>
            
            <details>
                <summary>Detalles técnicos y procedimiento</summary>
                <div class="details-content">
                    {content_html}
                </div>
            </details>
        </article>
"""

html_content += """
    </div>

    <div class="download-section">
        <h2>Reporte Completo</h2>
        <p>Descarga el documento oficial en formato PDF para visualizar el reporte extenso, incluyendo capturas de pantalla, evidencias del sistema y la justificación técnica completa.</p>
        <a href="act08-Equipo2.pdf" class="btn-download" download>
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
            Descargar Documento PDF
        </a>
    </div>

</div>

<footer>
    Universidad Politécnica de San Luis Potosí | Seguridad Informática
</footer>

</body>
</html>
"""

with open(r'c:\Users\vanch\Documents\Antigravity\IvanRosP.github.io\html\RHOF\actividad08.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
