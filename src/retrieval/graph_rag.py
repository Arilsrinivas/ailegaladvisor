import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

class GraphRAGEngine:
    """
    Implements real GraphRAG using Neo4j driver.
    """
    def __init__(self):
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = os.getenv("NEO4J_USER", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD", "password")
        self.driver = None
        try:
            driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            driver.verify_connectivity()
            self.driver = driver
        except Exception as e:
            print(f"[Warning] Failed to connect to Neo4j: {e}. GraphRAG will be disabled.")

    def close(self):
        if self.driver:
            self.driver.close()

    def query_relationships(self, entity_name):
        """
        Retrieves related legal concepts using Cypher.
        """
        if not self.driver: return []
        
        with self.driver.session() as session:
            result = session.run(
                "MATCH (e:LegalConcept {name: $name})-[:RELEVANT_TO|INTERPRETED_BY*1..2]-(related) "
                "RETURN related.name as name, labels(related)[0] as type",
                name=entity_name
            )
            return [record.data() for record in result]

    def verify_statute_mapping(self, article_id):
        """
        Verifies if an IPC section has been replaced by a BNS section.
        """
        if not self.driver: return None
        
        with self.driver.session() as session:
            result = session.run(
                "MATCH (a:Article {id: $id})-[:REPLACED_BY]->(s:Section) "
                "RETURN s.id as id, s.description as desc",
                id=article_id
            )
            record = result.single()
            return record.data() if record else None

    def get_precedent_chain(self, case_id):
        """
        Retrieves citations and precedents.
        """
        if not self.driver: return []
        
        with self.driver.session() as session:
            result = session.run(
                "MATCH (c:Case {id: $id})-[:CITES*1..2]->(p:Precedent) "
                "RETURN p.title as title, p.citation as citation",
                id=case_id
            )
            return [record.data() for record in result]
