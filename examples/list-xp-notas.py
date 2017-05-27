from ibapi import xp
from getpass import getpass

def print_passwd_menu(numbers):
    print('Password buttons:')
    for i, num in enumerate(numbers):
        print('  {}. {}'.format(i + 1, num))

def passwd_cb(numbers):
    order = []
    for i in range(6):
        print_passwd_menu(numbers)
        k = int(input('Choice: ')) - 1
        order.append(k)
    print(order)
    return order

def main():
    account = input('Account: ')
    #passwd = getpass()
    #with xp.Session(account, passwd) as sess:
    with xp.Session(account, passwd_cb=passwd_cb) as sess:
        sess.start()
        dates = sess.list_notas()
        for date in dates:
            print(sess.get_nota(date))

if __name__ == '__main__':
    main()
