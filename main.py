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

    df = pd.read_excel('data/sagah_2024_1.xlsx')
    bot = Bot(username=env_parser.get('account', 'username'),
            password=env_parser.get('account', 'password'))
    
    df = df.fillna('')

    if operacao == 'cursos':
        cursos = processar_cursos(df)
        bot.run_bot(operacao, cursos)
    elif operacao == 'disciplinas':
        disciplinas = processar_disciplinas(df)
        bot.run_bot(operacao, disciplinas)
    
    elif operacao == 'professores':
        associacoes = processar_professores(df)
        bot.run_bot(operacao, associacoes)
        


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

def associar_professor_email(df: pd.DataFrame) -> dict:
    professor_email = {}
    
    for _, row in df.iterrows():
        professor = row['professor'].strip()
        email = row['email'].strip()
        
        if professor == 'Sem professor':
            continue
        
        if professor not in professor_email:
            professor_email[professor] = email
            
    return professor_email

def associar_disciplina_professor(df: pd.DataFrame) -> dict:
    disciplina_professor = {}
    
    for _, row in df.iterrows():
        disciplina = row['nome_moodle'].strip()
        professor = row['professor'].strip()
        if professor == 'Sem professor':
            continue
        
        if disciplina not in disciplina_professor:
            disciplina_professor[disciplina] = professor
            
    return disciplina_professor

def processar_professores( df: pd.DataFrame )->dict:
    associacoes = {}
    associacoes['disciplina_professor'] = associar_disciplina_professor(df)
    associacoes['professor_email'] =associar_professor_email(df)
    
    return associacoes

if __name__ == '__main__':
    print('sagah.py: Executando como script')
    main()