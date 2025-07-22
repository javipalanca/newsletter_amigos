#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simplificado para preview rápido con plantilla actualizada
"""

import sys
import tempfile
import webbrowser
import os

def quick_preview(newsletter_file):
    """Previsualización rápida sin argumentos complejos"""
    
    # Leer newsletter
    try:
        with open(newsletter_file, 'r', encoding='utf-8') as f:
            newsletter = f.read()
    except:
        print(f"❌ Error leyendo {newsletter_file}")
        return
    
    # Leer plantilla
    try:
        with open('plantilla.html', 'r', encoding='utf-8') as f:
            template = f.read()
    except:
        print("❌ Error leyendo plantilla.html")
        return
    
    # Extraer contenido del newsletter
    start = newsletter.find('<table class="main-table">')
    end = newsletter.rfind('</table>') + 8
    
    if start == -1 or end == 7:
        print("❌ No se pudo extraer el contenido del newsletter")
        return
    
    content = newsletter[start:end]
    
    # Inyectar en plantilla (marcador actualizado)
    marker = "{{ template \"content\" . }}"
    if marker not in template:
        print("❌ Marcador no encontrado en plantilla")
        print(f"Buscando: {marker}")
        return
    
    final_html = template.replace(marker, content)
    
    # Limpiar variables de template para preview
    template_vars = {
        "{{ .Campaign.Subject }}": "Newsletter Amigos del Museo - Preview",
        "{{ UnsubscribeURL }}": "#unsubscribe",
        "{{ MessageURL }}": "#view-in-browser", 
        "{{ L.T \"email.unsub\" }}": "Darse de baja",
        "{{ L.T \"email.viewInBrowser\" }}": "Ver en navegador",
        "{{ TrackView }}": ""
    }
    
    for var, replacement in template_vars.items():
        final_html = final_html.replace(var, replacement)
    
    # Crear archivo temporal y abrir
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
        f.write(final_html)
        temp_path = f.name
    
    webbrowser.open(f'file://{os.path.abspath(temp_path)}')
    print(f"🌐 Newsletter abierto en navegador")
    print(f"📁 Archivo temporal: {temp_path}")
    
    input("Presiona Enter para eliminar archivo temporal...")
    try:
        os.unlink(temp_path)
        print("🗑️ Archivo temporal eliminado")
    except:
        print("⚠️ No se pudo eliminar el archivo temporal")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python preview_simple.py july24.html")
        sys.exit(1)
    
    quick_preview(sys.argv[1])