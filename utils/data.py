from calendar import monthrange
from datetime import datetime


def get_days_of_month(ano, mes):
    """Retorna os dias do mês e os dias da semana."""
    dias_no_mes = monthrange(ano, mes)[1]
    dias = []
    for i in range(dias_no_mes):
        dia = i + 1
        data = datetime(ano, mes, dia)
        dias.append((data.strftime('%d/%m/%Y'), get_weekday_name(data)))
    return dias


def get_weekday_name(data):
    """Converte o nome do dia da semana para português."""
    dias_em_portugues = {
        "Monday": "Segunda-feira",
        "Tuesday": "Terça-feira",
        "Wednesday": "Quarta-feira",
        "Thursday": "Quinta-feira",
        "Friday": "Sexta-feira",
        "Saturday": "Sábado",
        "Sunday": "Domingo"
    }
    return dias_em_portugues[data.strftime('%A')]


def get_month_name(mes):
    """Retorna o nome do mês em formato amigável."""
    meses = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    return meses[mes - 1]
