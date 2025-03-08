import mysql.connector
from graphviz import Digraph

def fetch_schema_from_mysql(host, user, password, database):
    """
    Récupère la structure des tables et les relations depuis une base MySQL.
    Retrieves the structure of tables and relationships from a MySQL database.
    """
    connection = mysql.connector.connect(host=host, user=user, password=password, database=database)
    cursor = connection.cursor()
    
    tables = {}
    relationships = []
    
    # Récupérer les tables et leurs colonnes
    # Retrieve tables and their columns
    cursor.execute("SHOW TABLES")
    for (table_name,) in cursor.fetchall():
        cursor.execute(f"DESCRIBE {table_name}")
        tables[table_name] = [row[0] for row in cursor.fetchall()]
    
    # Récupérer les relations (clés étrangères)
    # Retrieve relationships (foreign keys)
    cursor.execute("""
        SELECT TABLE_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME 
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
        WHERE TABLE_SCHEMA = %s AND REFERENCED_TABLE_NAME IS NOT NULL
    """, (database,))
    
    for row in cursor.fetchall():
        table, column, ref_table, ref_column = row
        relationships.append((table, ref_table, f"{column} → {ref_column}"))
    
    cursor.close()
    connection.close()
    return tables, relationships

def generate_db_schema(tables, relationships, output_path="database_schema"):
    """
    Génère un schéma de base de données sous forme de graphe à partir de la définition des tables et des relations.
    Generates a database schema as a graph from the definition of tables and relationships.
    """
    db_schema = Digraph("DB_Schema", format="png")
    
    # Ajouter les tables
    # Add tables
    for table, columns in tables.items():
        db_schema.node(table, f"{table}\n({', '.join(columns)})")
    
    # Ajouter les relations
    # Add relationships
    for source, target, label in relationships:
        db_schema.edge(source, target, label=label)
    
    # Générer et sauvegarder le schéma
    # Generate and save the schema
    db_schema.render(output_path, format="png", cleanup=True)
    print(f"Schéma généré: {output_path}.png")
    print(f"Schema generated: {output_path}.png")
    return output_path + ".png"

if __name__ == "__main__":
    # Connexion à la base MySQL et extraction du schéma
    # Connect to MySQL database and extract schema
    host = "localhost"
    user = "root"
    password = "MySup3R_p@ssw0rd"
    database = "my_database"

    tables, relationships = fetch_schema_from_mysql(host, user, password, database)

    generate_db_schema(tables, relationships)
