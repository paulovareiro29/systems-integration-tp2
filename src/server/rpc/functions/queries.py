from utils.database import Database


def fetchAirbnbs():
    """Returns all the airbnbs"""
    database = Database()

    results = []
    for e in database.selectAll(
            "SELECT  unnest(xpath('//Airbnbs/Airbnb/Name/text()', xml)) as output FROM imported_documents WHERE deleted_on IS NULL"):
        results.append(e[0])

    database.disconnect()
    return results


def fetchAreas():
    """Returns all the areas in each file"""
    database = Database()

    results = []
    for e in database.selectAll(
            "SELECT unnest(xpath('//Areas/Area/@name', xml)) as output FROM imported_documents WHERE deleted_on IS NULL"):
        results.append(e[0])

    database.disconnect()
    return results


def fetchTypes():
    """Returns all the types in each file"""
    database = Database()

    results = []
    for e in database.selectAll(
            "SELECT  unnest(xpath('//Types/Type/@name', xml)) as output FROM imported_documents WHERE deleted_on IS NULL"):
        results.append(e[0])

    database.disconnect()
    return results


def countAirbnbs():
    """Returns the number of airbnbs per file in database"""
    database = Database()

    results = []
    for e in database.selectAll(
            "SELECT file_name, unnest(xpath('count(//Airbnbs/Airbnb)', xml)) as output FROM imported_documents WHERE deleted_on IS NULL"):
        results.append([e[0], e[1]])

    database.disconnect()
    return results


def fetchByArea(area):
    """Returns how many airbnbs exists by area in each file"""
    database = Database()

    results = []
    for e in database.selectAll(
            f"SELECT unnest(xpath('//Airbnbs/Airbnb/Address[@area_ref=/Root/Areas/Area[@name=\"{area}\"]/@id]/../Name/text()', xml)) as output FROM imported_documents WHERE deleted_on IS NULL"):
        results.append(e[0])

    database.disconnect()
    return results


def fetchByType(type):
    """Returns how many airbnbs exists by type in each file"""
    database = Database()

    results = []
    for e in database.selectAll(
            f"SELECT unnest(xpath('//Airbnbs/Airbnb[@type_ref=/Root/Types/Type[@name=\"{type}\"]/@id]/Name/text()', xml)) as output FROM imported_documents WHERE deleted_on IS NULL"):
        results.append(e[0])

    database.disconnect()
    return results


def fetchByPriceLowerThen(price):
    """Returns all the airbnbs which price is lower then"""
    database = Database()

    results = []
    for e in database.selectAll(
            f"SELECT unnest(xpath('//Airbnbs/Airbnb[Price < {price}]/Name/text()', xml)) as output FROM imported_documents WHERE deleted_on IS NULL"):
        results.append(e[0])

    database.disconnect()
    return results


def fetchByPriceHigherThen(price):
    """Returns all the airbnbs which price is higher then"""
    database = Database()

    results = []
    for e in database.selectAll(
            f"SELECT  unnest(xpath('//Airbnbs/Airbnb[Price > {price}]/Name/text()', xml)) as output FROM imported_documents WHERE deleted_on IS NULL"):
        results.append(e[0])

    database.disconnect()
    return results
