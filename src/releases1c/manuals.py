import platform

def howto_authentication():
    print()
    print('Check you provide authentication information:')
    print()
    if platform.system() == 'Windows':
        print('>','set RELEASES1C_USERNAME=<username>')
        print('>','set RELEASES1C_PASSWORD=<password>')
    else:
        print('>','export RELEASES1C_USERNAME=<username>')
        print('>','export RELEASES1C_PASSWORD=<password>')