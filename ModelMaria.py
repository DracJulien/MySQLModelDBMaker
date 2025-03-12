import mariadb
import sys
from graphviz import Digraph

DEBUG = True


def fetch_schema_from_mariadb(host, user, password, database, port=3306):
    """
    Récupère la structure des tables et les relations depuis une base MariaDB.
    Retrieves the structure of tables and relationships from a MariaDB database.
    """
    try:
        # Connexion à MariaDB
        conn = mariadb.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        cursor = conn.cursor()

        tables = {}
        relationships = []

        # Récupérer les tables et leurs colonnes
        cursor.execute("SHOW TABLES")
        for (table_name,) in cursor.fetchall():
            cursor.execute(f"DESCRIBE `{table_name}`")
            tables[table_name] = [row[0] for row in cursor.fetchall()]
            if DEBUG:
                print(f"Table: {table_name} -> Colonnes: {tables[table_name]}")

        # Récupérer les relations (clés étrangères)
        cursor.execute("""
            SELECT TABLE_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME 
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
            WHERE TABLE_SCHEMA = %s AND REFERENCED_TABLE_NAME IS NOT NULL
        """, (database,))
        
        for row in cursor.fetchall():
            table, column, ref_table, ref_column = row
            relationships.append((table, ref_table, f"{column} → {ref_column}"))
            if DEBUG:
                print(f"Relation: {table}.{column} -> {ref_table}.{ref_column}")

        cursor.close()
        conn.close()

        return tables, relationships

    except mariadb.Error as e:
        print(f"Erreur MariaDB: {e}")
        sys.exit(1)


def generate_db_schema(tables, relationships, output_path="database_schema"):
    """
    Génère un schéma de base de données sous forme de graphe à partir de la définition des tables et des relations.
    Generates a database schema as a graph from the definition of tables and relationships.
    """
    db_schema = Digraph("DB_Schema", format="png")

    # Ajouter les tables
    for table, columns in tables.items():
        db_schema.node(table, f"{table}\n({', '.join(columns)})")

    # Ajouter les relations
    for source, target, label in relationships:
        db_schema.edge(source, target, label=label)

    # Générer et sauvegarder le schéma
    db_schema.render(output_path, format="png", cleanup=True)
    print(f"Schéma généré: {output_path}.png")
    return output_path + ".png"


if __name__ == "__main__":
    # Connexion à la base MariaDB et extraction du schéma
    host = "localhost"
    user = "root"
    password = "MySup3R_p@ssw0rd"
    database = "my_database"
    port = 3306  # MariaDB default

    tables, relationships = fetch_schema_from_mariadb(host, user, password, database, port)

    generate_db_schema(tables, relationships)
