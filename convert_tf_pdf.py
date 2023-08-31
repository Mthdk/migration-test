import os
from PIL import Image
from fpdf import FPDF

def convert_tif_to_pdf(input_path, output_path):
    # Abre a imagem TIF usando a biblioteca Pillow
    img = Image.open(input_path)
    
    # Cria um novo PDF usando a biblioteca FPDF
    pdf = FPDF()
    pdf.add_page()
    
    # Converte a imagem TIF para um arquivo PDF
    pdf.image(input_path, x = 10, y = 10, w = 190)
    
    # Salva o PDF no local especificado
    pdf.output(output_path, "F")

def batch_convert_tif_to_pdf(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.tif'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename[:-4] + '.pdf')
            convert_tif_to_pdf(input_path, output_path)

if __name__ == "__main__":
    input_folder = "/caminho/do/diretorio_com_tifs"  # Substitua pelo caminho do diretório com as imagens TIF
    output_folder = "/caminho/do/diretorio_de_saida"  # Substitua pelo caminho do diretório de saída

    batch_convert_tif_to_pdf(input_folder, output_folder)
    print("Conversão concluída. As imagens TIF foram convertidas para PDF.")
