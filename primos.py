


def e_divisivel(dividendo: int, divisor: int)->bool:
    '''Retorna True ou False

    True se dividendo / divisor não tiver resto
    False se tiver resto ou divisor == 0
    '''
    if divisor == 0:
        return False
    quociente = dividendo / divisor
    resto = quociente - int(quociente)
    return resto == 0


def e_primo(numero: int)-> bool:
    '''Testa se numero é primo e retorna True ou False.'''
    if numero == 1:
        return False

    for divisor in range(2, (numero // 2) + 1):
        print('Dividindo %d  por %d ' % (numero, divisor))
        if e_divisivel(numero, divisor):
            print('%d  é divisível por %d!!! Não é primo!' % (numero, divisor))
            return False
    print('%d é primo!' % numero)
    return True




if __name__ == '__main__':
    # Testa e_divisivel
    assert e_divisivel(2, 1) is True  # True
    assert e_divisivel(4, 2) is True  # True
    assert e_divisivel(5, 2) is False  # False
    assert e_divisivel(1, 0) is False  # False

    # Testa alguns números primos
    assert e_primo(1) is False
    assert e_primo(2) is True
    assert e_primo(3) is True
    assert e_primo(4) is False
    assert e_primo(5) is True
    assert e_primo(6) is False
    assert e_primo(7) is True
    assert e_primo(8) is False
    assert e_primo(9) is False
    assert e_primo(10) is False
    assert e_primo(11) is True
    assert e_primo(13) is True
    assert e_primo(15) is False
    assert e_primo(17) is True
    assert e_primo(19) is True
    assert e_primo(30) is False
    assert e_primo(41) is True
    assert e_primo(45) is False
    assert e_primo(53) is True

    queroserprimo = int(input('Entre com um numero para testar:'))
    print(e_primo(queroserprimo))
