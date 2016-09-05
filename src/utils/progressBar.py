import sys


def progress(count, total, title=''):
    """
    Barra de progreso para mostrar en la consola.
    :param count: Int
        Cuanto lleva el progreso
    :param total: Int
        Cuanto es el total.
    :param title: String
        Valor opcional para ponerle un titulo a la barra
    """

    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stderr.write('[%s] %s%s ...%s\r' % (bar, percents, '%', title))

if __name__ == "__main__":
    import time
    total = 1000
    i = 0

    while i < total:
        progress(i, total, "Example")
        time.sleep(0.5)
        i += 1
