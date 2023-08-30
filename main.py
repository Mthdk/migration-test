import os
import pandas as pd
from openpyxl import load_workbook
from sqlalchemy import create_engine
from tqdm import tqdm

DB_URL = 'sqlite:///database.db'  # Modifique para o seu banco de dados
DESTINATION_FOLDER = 'destino'  # Pasta de destino para os arquivos movidos

def insert_data_to_db(file_path, db_engine):
    df = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)
    df.to_sql('data', db_engine, if_exists='append', index=False)

def move_files(files, destination_folder):
    os.makedirs(destination_folder, exist_ok=True)
    for file in tqdm(files, desc='Moving files', unit='file'):
        new_path = os.path.join(destination_folder, os.path.basename(file))
        os.rename(file, new_path)

def main():
    db_engine = create_engine(DB_URL)
    file_path_column = 'path'  # Coluna que contém os caminhos no arquivo

    with db_engine.connect() as connection:
        result = connection.execute(f'SELECT DISTINCT {file_path_column} FROM data')
        files_to_move = [row[0] for row in result]

    insert_data_to_db('arquivo.csv', db_engine)  # Modifique para o seu arquivo
    move_files(files_to_move, DESTINATION_FOLDER)

if __name__ == '__main__':
    main()
