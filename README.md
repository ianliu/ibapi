Internet Banking API
====================

Este módulo de python provê uma API para alguns *Internet Bankings*
brasileiros.

# Instalação

Para instalar faça o clone deste repositório e execute o comando abaixo
na pasta do projeto:

    pip install .

# Exêmplos de uso

``` python
from ibapi import xp
from getpass import getpass

account = input('Account: ')
passwd = getpass()
with xp.Session(account, passwd) as sess:
    sess.start()
    dates = sess.list_notas()
    for date in dates:
        print(sess.get_nota(date))
```

# Objetivos

## XP Investimentos

 - [x] Sessão de login
 - [x] Listar datas em que houveram negociações no *homebroker*
 - [x] Recuperar notas de corretagem em JSON
 - [ ] Recuperar extratos da conta corrente

## Santander

 - [ ] Sessão de login
 - [ ] Recuperar extratos da conta corrente
 - [ ] Recuperar extratos da conta poupança
 - [ ] Recuperar faturas de cartão de crédito

<!-- vim:tw=72:sw=2:et:sta
-->
