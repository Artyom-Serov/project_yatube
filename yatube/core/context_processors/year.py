import datetime


def year(request):
    """Добавляет переменную с текущим годом."""
    now = datetime.datetime.now()
    year = now.year
    return {'year': year}
