import argparse
import pandas as pd
from classes.bot import Bot
import configparser

def main():

    env_parser = configparser.ConfigParser()
    env_parser.read('conf.ini')

    parser = argparse.ArgumentParser(description="Processa um arquivo Excel e imprime um dicionário dos itens")
    parser.add_argument('operacao', type=str, help='Operação a ser realizada')
    args = parser.parse_args()
    operacao = args.operacao

    dados = pd.read_excel('data/sagah_2024_1.xlsx')
    bot = Bot(username=env_parser.get('account', 'username'),
            password=env_parser.get('account', 'password'))


    if operacao == 'cursos':
        cursos = processar_cursos(dados)
        bot.run_bot(operacao, cursos)
    elif operacao == 'disciplinas':
        disciplinas = processar_disciplinas(dados)
        bot.run_bot(operacao, disciplinas)


def processar_cursos(df: pd.DataFrame) -> list:
    cursos = set()  # Usamos um conjunto para garantir itens únicos
    
    df['cod_curso'] = df['cod_curso']
    df['nome_curso_mestre'] = df['nome_curso_mestre'].str.strip()
    
    for _, row in df.iterrows():
        cod_curso = row['cod_curso']
        nome_curso_mestre = row['nome_curso_mestre']
        
        # Adiciona o item ao conjunto no formato 'cod_curso - nome_curso_mestre'
        cursos.add(f"{cod_curso} - {nome_curso_mestre}")
    
    # Retorna a lista convertendo o conjunto para uma lista
    return list(cursos)

def processar_disciplinas(df: pd.DataFrame) -> dict:
    disciplinas = {}
    
    for _, row in df.iterrows():
        disciplina = row['nome_moodle'].strip()
        curso = row['cod_curso']
        
        if disciplina not in disciplinas:
            disciplinas[disciplina] = curso
            
    return disciplinas


if __name__ == '__main__':
    print('sagah.py: Executando como script')
    main()