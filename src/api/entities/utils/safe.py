def toSafeInt(integer, default):
    try:
        return int(integer)
    except:
        return default
