class InsuffincientSharesError(Exception):
    """Wyjątek rzucany, gdy uzytkownik chce sprzedac wiecej akcji niz posiada"""
    pass

class InsufficientCashError(Exception):
    """Wyjątek rzucany, gdy uzytkownik nie posiada odpowiedniej ilości gotówki do sfinalizowania transakcji"""
    pass
