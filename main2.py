import os
import shutil
import pandas as pd
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tqdm import tqdm

DESTINATION_FOLDER = 'destino'  # Pasta de destino para os arquivos copiados
LOG_FILE = 'log.txt'  # Arquivo de log para registrar origem e destino

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicação de Gerenciamento de Arquivos")

        self.file_label = Label(root, text="Selecione o arquivo:")
        self.file_label.pack()

        self.file_path_entry = Entry(root)
        self.file_path_entry.pack()

        self.browse_button = Button(root, text="Procurar", command=self.browse_file)
        self.browse_button.pack()

        self.process_button = Button(root, text="Processar", command=self.process_files)
        self.process_button.pack()

        self.copy_button = Button(root, text="Copiar", command=self.copy_files)
        self.copy_button.pack()

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV e XLSX files", "*.csv *.xlsx")])
        self.file_path_entry.delete(0, END)
        self.file_path_entry.insert(0, file_path)

    def copy_files(self):
        file_path = self.file_path_entry.get()
        if not file_path:
            messagebox.showerror("Erro", "Selecione um arquivo.")
            return

        df = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)
        files_to_copy = df.iloc[:, 2].tolist()  # Assumes the third column contains the paths

        for file in tqdm(files_to_copy, desc='Copying files', unit='file'):
            new_path = os.path.join(DESTINATION_FOLDER, os.path.basename(file))
            shutil.copy(file, new_path)
            self.log_copy(file, new_path)

        messagebox.showinfo("Concluído", "Cópia concluída com sucesso.")

    def log_copy(self, source, destination):
        with open(LOG_FILE, 'a') as log:
            log.write(f'Source: {source}\tDestination: {destination}\n')

    def process_files(self):
        file_path = self.file_path_entry.get()
        if not file_path:
            messagebox.showerror("Erro", "Selecione um arquivo.")
            return

        df = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)
        files_to_move = df.iloc[:, 2].tolist()  # Assumes the third column contains the paths

        self.move_files(files_to_move, DESTINATION_FOLDER)
        messagebox.showinfo("Concluído", "Processamento concluído com sucesso.")

if __name__ == '__main__':
    root = Tk()
    app = App(root)
    root.mainloop()
