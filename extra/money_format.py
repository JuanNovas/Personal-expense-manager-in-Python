def in_money(amount) -> int:  
    """
    Format the amount to be load into the database
    """ 
    return round(float(amount),2) * 100

    
def out_money(amount) -> float:
    """
    Format the amount gotten from the database to be displayed into the correct format
    """
    return round((float(amount) / 100),2)

