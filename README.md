# accounts_test

## Enunciado

Escreva uma função que faça a conciliação (ou batimento) entre dois grupos de transações financeiras.

Sua função, reconcile_accounts, deve receber duas listas de listas (representando as linhas dos dados financeiros) e deve devolver cópias dessas duas listas de listas com uma nova coluna acrescentada à direita das demais, que designará se a transação pôde ser encontrada (FOUND) naoutra lista ou não (MISSING).

As listas de listas representarão os dados em quatro colunas:
- Data (em formato YYYY-MM-DD)
- Departamento
- Valor
- Beneficiário

Todas as colunas serão representadas como strings.

Dados o arquivo transactions1.csv
```
2020-12-04,Tecnologia,16.00,Bitbucket
2020-12-04,Jurídico,60.00,LinkSquares
2020-12-05,Tecnologia,50.00,AWS
```

e o arquivo transactions2.csv:

```
2020-12-04,Tecnologia,16.00,Bitbucket
2020-12-05,Tecnologia,49.99,AWS
2020-12-04,Jurídico,60.00,LinkSquares
```

sua função reconcile_accounts deve funcionar do seguinte modo:
```
import csv
from pathlib import Path
from pprint import pprint
transactions1 = list(csv.reader(Path('transactions1.csv').open()))
transactions2 = list(csv.reader(Path('transactions2.csv').open()))
out1, out2 = reconcile_accounts(transactions1, transactions2)
pprint(out1)
pprint(out2)

[['2020-12-04', 'Tecnologia', '16.00', 'Bitbucket', 'FOUND'], ['2020-12-04', 'Jurídico', '60.00', 'LinkSquares', 'FOUND'], ['2020-12-05', 'Tecnologia', '50.00', 'AWS', 'MISSING']]

[['2020-12-04', 'Tecnologia', '16.00', 'Bitbucket', 'FOUND'], ['2020-12-05', 'Tecnologia', '49.99', 'AWS', 'MISSING'], ['2020-12-04', 'Jurídico', '60.00', 'LinkSquares', 'FOUND']]
```

Sua função deve levar em conta que em cada arquivo pode haver transações duplicadas. Nesse caso, a cada transação de um arquivo deve corresponder uma única outra transação do outro.

Cada transação pode corresponder a outra cuja data seja do dia anterior ou posterior, desde que as demais colunas contenham os mesmos valores. Quando houver mais de uma possibilidade decorrespondência para uma dada transação, ela deve ser feita com a transação que ocorrer mais cedo. Por exemplo, uma transação na primeira lista com data 2020-12-25 deve corresponder auma da segunda lista, ainda sem correspondência, de data 2020-12-24 antes de corresponder a outras equivalentes (a menos da data) com datas 2020-12-25 ou 2020-12-26

## Comentários sobre a implementação

- A ordem dos outputs do exemplo e do script estão diferentes, mas ele retorna os valores esperados.
- Isso se dá por causa da ordenação aplicada para termos a correspondência com a primeira data.
- Criei diversas funções para assim isolar as diferentes etapas do processo. Dessa forma, reduzo a complexidade ciclomática do fluxo principal, documento adequadamente cada etapa, facilita a criação dos testes e as funções podem ser reutilizadas. 
- Para melhorar a legibilidade, optei por
