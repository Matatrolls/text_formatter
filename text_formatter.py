import re

def format_text_to_concatenation(text, variable_name="texto"):
    """
    Convierte un texto en formato de concatenación de strings de Python
    
    Args:
        text (str): El texto a formatear
        variable_name (str): Nombre de la variable (por defecto 'texto')
    
    Returns:
        str: Texto formateado en estilo de concatenación
    """
    
    # Limpiar el texto de espacios extra y saltos de línea innecesarios
    text = re.sub(r'\n+', ' ', text)  # Reemplazar múltiples saltos de línea con espacio
    text = re.sub(r'\s+', ' ', text)  # Reemplazar múltiples espacios con uno solo
    text = text.strip()
    
    # Dividir en oraciones usando regex más sofisticado
    # Busca puntos, signos de exclamación, interrogación seguidos de espacio y mayúscula
    # o al final del texto
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
    
    # Limpiar oraciones vacías
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Comenzar la construcción del formato
    result = [f"{variable_name} = ("]
    
    # Procesar cada oración
    for i, sentence in enumerate(sentences):
        # Asegurar que la oración termine con espacio
        if not sentence.endswith(' '):
            sentence += ' '
        
        # Escapar comillas dobles si existen en el texto
        sentence = sentence.replace('"', '\\"')
        
        # Agregar la oración formateada
        if i == len(sentences) - 1:  # Última oración, sin coma
            result.append(f'    "{sentence}"')
        else:  # No es la última, agregar coma
            result.append(f'    "{sentence}"')
    
    # Cerrar la estructura
    result.append(")")
    
    return '\n'.join(result)

def format_text_from_file(file_path, variable_name="texto"):
    """
    Lee un archivo y aplica el formato de concatenación
    
    Args:
        file_path (str): Ruta del archivo a leer
        variable_name (str): Nombre de la variable
    
    Returns:
        str: Texto formateado
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return format_text_to_concatenation(content, variable_name)
    except FileNotFoundError:
        return f"Error: No se pudo encontrar el archivo {file_path}"
    except Exception as e:
        return f"Error al leer el archivo: {str(e)}"

# Función para usar desde PowerShell con argumentos de línea de comandos
def main():
    import sys
    import os
    
    if len(sys.argv) < 2:
        print("Uso: python text_formatter.py <archivo.txt> [nombre_variable]")
        print("Ejemplo: python text_formatter.py mi_texto.txt")
        print("Ejemplo: python text_formatter.py mi_texto.txt mi_variable")
        return
    
    file_path = sys.argv[1]
    variable_name = sys.argv[2] if len(sys.argv) > 2 else "texto"
    
    # Formatear el archivo
    result = format_text_from_file(file_path, variable_name)
    
    # Mostrar resultado en consola
    print("Texto formateado:")
    print(result)
    print("\n" + "="*60 + "\n")
    
    # Generar nombre del archivo de salida
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_file = f"{base_name}_formatted.txt"
    
    # Guardar resultado en archivo
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        
        print(f"✅ Archivo guardado exitosamente: {output_file}")
        print(f"📁 Ubicación: {os.path.abspath(output_file)}")
        
    except Exception as e:
        print(f"❌ Error al guardar el archivo: {str(e)}")
        print("El resultado se mostró en consola pero no se pudo guardar.")

def save_formatted_text(original_file_path, formatted_content):
    """
    Guarda el texto formateado en un nuevo archivo
    
    Args:
        original_file_path (str): Ruta del archivo original
        formatted_content (str): Contenido ya formateado
    
    Returns:
        str: Ruta del archivo guardado o mensaje de error
    """
    import os
    
    try:
        # Crear nombre del archivo de salida
        base_name = os.path.splitext(os.path.basename(original_file_path))[0]
        output_file = f"{base_name}_formatted.txt"
        
        # Guardar el contenido
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(formatted_content)
        
        return os.path.abspath(output_file)
    
    except Exception as e:
        return f"Error: {str(e)}"

# Ejemplo de uso con texto de muestra
if __name__ == "__main__":
    # Si se ejecuta desde línea de comandos con argumentos
    import sys
    if len(sys.argv) > 1:
        main()
    else:
        # Texto de ejemplo para pruebas
        sample_text = """Esta es una oración de ejemplo. ¡Esta es otra oración con exclamación! ¿Y esta es una pregunta? Finalmente, esta es la última oración del ejemplo."""
        
        # Aplicar el formato
        formatted_result = format_text_to_concatenation(sample_text)
        print("Resultado del formateo:")
        print(formatted_result)
        
        print("\n" + "="*50 + "\n")
        print("CÓMO USAR DESDE POWERSHELL:")
        print("1. Guarda este código como 'text_formatter.py'")
        print("2. Abre PowerShell en la carpeta donde está el archivo")
        print("3. Ejecuta: python text_formatter.py tu_archivo.txt")
        print("4. El resultado se guardará automáticamente como 'tu_archivo_formatted.txt'")
        print("\nEjemplos:")
        print("python text_formatter.py shrek_script.txt")
        print("→ Genera: shrek_script_formatted.txt")
        print()
        print("python text_formatter.py mi_texto.txt dialogo")
        print("→ Genera: mi_texto_formatted.txt")
        print()
        print("🔄 El archivo se guarda automáticamente después del procesamiento")
        print("📁 Se crea en la misma carpeta donde ejecutas el script")