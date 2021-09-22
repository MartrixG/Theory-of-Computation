import re

pattern = re.compile(r'(([0-9])|([1-9][0-9])|(1[0-9][0-9])|(2[0-4][0-9])|(25[0-5]))\.'
                     r'(([0-9])|([1-9][0-9])|(1[0-9][0-9])|(2[0-4][0-9])|(25[0-5]))\.'
                     r'(([0-9])|([1-9][0-9])|(1[0-9][0-9])|(2[0-4][0-9])|(25[0-5]))\.'
                     r'(([0-9])|([1-9][0-9])|(1[0-9][0-9])|(2[0-4][0-9])|(25[0-5]))$')


def ipaddress_check(address):
    match = pattern.match(address)
    if match:
        print('yes')
    else:
        print('no')


if __name__ == '__main__':
    ipaddress_check('255.255.255.255')
    ipaddress_check('192.168.1.1')
    ipaddress_check('192.168.1.0')
    ipaddress_check('192.168.1.01')
    ipaddress_check('192.168.1.256')
    ipaddress_check('192.168.1.2555')
