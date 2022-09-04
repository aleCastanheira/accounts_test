import csv
from pathlib import Path
from pprint import pprint
from datetime import datetime

# Mapeamento dos campos, para facilitar caso a ordem mude no futuro.
FIELD_DATE = 0
FIELD_DEPARTMENT = 1
FIELD_VALUE = 2
FIELD_RECIPIENT = 3
FIELD_CHECK = 4

# Constantes para garantir que a mesma str seja usada e facilita 
VALUE_FOUND = "FOUND"
VALUE_MISSING = "MISSING"

def add_column(item: list) -> list:
    '''
    Adiciona a coluna verificadora com um valor padrão.
    '''
    item.append(VALUE_MISSING)
    return item


def get_accounts_uk(item: list) -> str:
    '''
    Retorna uma str que representa um registro único.

    Caso a regra de negócio mude, é só alterar esta função.
    '''
    return f"{item[FIELD_DEPARTMENT]}-{item[FIELD_VALUE]}-{item[FIELD_RECIPIENT]}"


def normalize_transactions(transactions: list) -> list:
    '''
    Normalizo a lista  de transações para padronizar as listas. 
    
    Processos realizados:
        - Adiciono a nova coluna nas duas listas de transações.
        - Ordenação para garantir que a correspondêcia ocorra com
            a transação que ocorrer antes.
    '''
    transactions = [ add_column(item) for item in transactions ]
    transactions = sorted(transactions, key=lambda t: t[FIELD_DATE])
    return transactions


def is_valid_date_interval(date_a: str, date_b: str) -> bool:
    '''
    Valida o intervalo de datas, caso o intervalo seja de até um dia, 
    é um intervalo válido.
    '''
    date_a = datetime.strptime(date_a, '%Y-%m-%d')
    date_b = datetime.strptime(date_b, '%Y-%m-%d')
    delta = date_a - date_b
    return abs(delta.days) in (0, 1)


def reconcile_accounts(transactions_a: list, transactions_b: list):
    '''
    Função que realiza o batimento entre duas contas.
    '''
    transactions_a = normalize_transactions(transactions_a)
    transactions_b = normalize_transactions(transactions_b)

    for item_a in transactions_a:
        unique_key_a = get_accounts_uk(item_a)

        for item_b in transactions_b:
            unique_key_b = get_accounts_uk(item_b)

            if is_valid_date_interval(item_a[FIELD_DATE], item_b[FIELD_DATE]) \
                and unique_key_a == unique_key_b:
                
                item_a[FIELD_CHECK] = VALUE_FOUND
                item_b[FIELD_CHECK] = VALUE_FOUND
                
    return transactions_a, transactions_b


transactions1 = list(csv.reader(Path('transactions1.csv').open()))
transactions2 = list(csv.reader(Path('transactions2.csv').open()))

out1, out2 = reconcile_accounts(transactions1, transactions2)

pprint(out1)
pprint(out2)