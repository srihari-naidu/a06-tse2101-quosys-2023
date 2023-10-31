def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def is_finance_officer(user):
    return user.groups.filter(name='Finance Officer').exists()

def is_salesman(user):
    return user.groups.filter(name='Salesman').exists()

def is_customer(user):
    return user.groups.filter(name='Customer').exists()