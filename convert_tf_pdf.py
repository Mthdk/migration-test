import os
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def tif_to_pdf(input_path, output_path):
    image = Image.open(input_path)
    pdf_path = os.path.join(output_path, os.path.basename(input_path)[:-4] + '.pdf')
    
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    c.drawImage(input_path, 0, 0, width, height)
    c.save()

def convert_images_in_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.tif'):
            input_path = os.path.join(input_dir, filename)
            tif_to_pdf(input_path, output_dir)

def convert_images_in_directories(input_dirs, output_dir):
    for input_dir in input_dirs:
        convert_images_in_directory(input_dir, output_dir)

if __name__ == "__main__":
    input_dirs = ["/caminho/do/diretorio1", "/caminho/do/diretorio2"]  # Substitua pelos caminhos dos diretórios
    output_dir = "/caminho/do/diretorio_de_saida"  # Substitua pelo caminho do diretório de saída

    convert_images_in_directories(input_dirs, output_dir)
    print("Conversão concluída. As imagens TIF foram convertidas para PDF.")
