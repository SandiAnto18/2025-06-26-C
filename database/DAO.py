from database.DB_connect import DBConnect
from model.constructor import Constructor
from model.driver import Driver


class DAO():
    @staticmethod
    def getAllYears():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select year 
from seasons s  
order by year
"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row["year"])

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllConstructors():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select c.*
from constructors c 
    """
        cursor.execute(query)

     # NOSTRA INTERPRETAZIONE:
     # PRENDO SOLO I COSTRUTTORI PRESENTI IN RESULTS
     # PERCHÉ "HANNO DISPUTATO ALMENO UN GRAN PREMIO" (c.csontructorid=r.construcotrid)

     # SOLUZIONE DEL PROF: TUTTI I COSTRUTTORI DEL DATABASE

        res = []
        for row in cursor:
            res.append(Constructor(**row))

        cursor.close()
        cnx.close()
        return res
#NOTA: qua non stiamo aggiungendo i tre attributi ai nodi,
# ma stiamo creando degli oggetti Driver da ASSOCIARE a ciascun nodo Constructor( constructorid,nodo creato in precedenza)
    @staticmethod
    def getInfoConstructors(year1,year2,constructorId):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        # RECUPERO I RISULTATI DEL COSTRUTTORE SELEZIONATO NEL RANGE DI ANNI SELEZIONATO
        query = """select r.driverId,r.position,rc.raceId 
from constructors c ,results r,races rc
where c.constructorId =r.constructorId 
and rc.year between %s and %s
and r.raceId = rc.raceId 
and c.constructorId = %s
        """
        cursor.execute(query,(year1,year2,constructorId))

        res = []
        for row in cursor:
            res.append(Driver(**row))
        # POSSO RECUPERARE COLONNE DA TABELLE DIVERSE NELLA STESSA SELECT(results e races)
        # LA CLASSE DRIVER NON DEVE NECESSARIAMENTE CORRISPONDERE
        # A UNA SINGOLA TABELLA DEL DATABASE.
        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getEdges(year1, year2):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        # RECUPERO LE COPPIE DI COSTRUTTORI E IL PESO DEGLI ARCHI

        # NON USO count(distinct r.raceId) PERCHE' DEVO CONTARE LE GARE COMPLETATE
        # DA CIASCUN PILOTA: SE DUE PILOTI DELLO STESSO TEAM
        # COMPLETANO LA STESSA GARA, DEVONO ESSERE CONTATI ENTRAMBI.
        query = """
            select t1.c1 as c1,t2.c2 as c2, t1.garetot + t2.garetot2 as peso
from (select c.constructorId  as c1, count(r.raceId) as gareTot
from constructors c , results r,races rc
where c.constructorId =r.constructorId 
and rc.raceId =r.raceId 
and rc.year between %s and %s
and r.position is not null
group by c1 ) as t1,
(select c.constructorId as c2, count(r.raceId) as gareTot2
from constructors c , results r,races rc
where c.constructorId =r.constructorId 
and rc.raceId =r.raceId 
and rc.year between %s and %s
and r.position is not null
group by c2 ) as t2
where c1 < c2

        """

        cursor.execute(query, (year1, year2, year1, year2))

        res = []
        for row in cursor:
            res.append((row["c1"], row["c2"], row["peso"]))

        cursor.close()
        cnx.close()
        return res



