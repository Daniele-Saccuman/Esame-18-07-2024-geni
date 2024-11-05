from database.DB_connect import DBConnect
from model.Gene import Genes


class DAO():

    @staticmethod
    def get_all_genes(crMin, crMax):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select g.*
                        from genes g 
                        where g.Chromosome >= %s
                        and g.Chromosome <= %s"""

            cursor.execute(query, (crMin, crMax))

            for row in cursor:
                result.append(Genes(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllChromosome():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct g.Chromosome as chr
                           from genes g 
                           order by g.Chromosome asc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["chr"])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllConnectedGenes(crMin, crMax):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select g1.GeneID as gene1, g1.Function as f1, g1.Chromosome as c1, g2.GeneID as  gene2, g2.Function as f2, g2.Chromosome as c2, i.Expression_Corr as peso 
                    from genes g1, genes g2,  classification c1, classification c2, interactions i 
                    where g1.GeneID <> g2.GeneID
                    and c1.GeneID = g1.GeneID  
                    and c2.GeneID  = g2.GeneID
                    and c1.Localization = c2.Localization 
                    and i.GeneID1 = g1.GeneID
                    and i.GeneID2 = g2.GeneID 
                    and g1.Chromosome>=%s
                    and g1.Chromosome<=%s
                    and g2.Chromosome>=%s
                    and g2.Chromosome<=%s"""

        cursor.execute(query, (crMin, crMax, crMin, crMax))


        for row in cursor:
            result.append((row["gene1"], row["f1"], row["c1"], row["gene2"], row["f2"], row["c2"], row["peso"]))

        cursor.close()
        conn.close()
        return result


