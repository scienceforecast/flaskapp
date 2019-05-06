

def pretty_domain_name(domain_name):
    """
    Функция преобразует строку из health_life в Health Life
    """
    words = domain_name.split('_')
    out = []
    for word in words:
        if word == 'and':
            out.append(word)
            continue
        out.append(word.capitalize())
    print(' '.join(out))
    return ' '.join(out)
