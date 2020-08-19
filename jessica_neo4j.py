#######jessica_neo4j.py#######
'''
https://neo4j.com/docs/cypher-manual/current/clauses/create/#create-create-a-node-with-a-label
'''
import re
import os
import time
from neo4j import *
from pyspark import *
from pyspark.sql import *
from pyspark.sql.types import *
from pyspark.sql.functions import *

def ingest_node_json2neo4j(bolt_url,
	bolt_username,
	bolt_password,
	input_json,
	sqlContext = None,
	delect_neo4j = True):
	print("connecting to the neo4j server")
	neo4j_instance = GraphDatabase.driver(bolt_url, auth=(bolt_username, bolt_password))
	#neo4j_session = neo4j_instance.session()
	print("loading node data from "+input_json)
	sqlContext.read.json(input_json).registerTempTable('input')
	input = sqlContext.sql(u"""
		SELECT DISTINCT * FROM input
		""")
	n = input.collect()
	print("loaded "+str(len(n))+' nodes from '+input_json)
	with neo4j_instance.session() as neo4j_session:
		if delect_neo4j is True:
			print("deleting data of neo4j")
			neo4j_session.run(u"""
			MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r;
			""")
	print('inserting nodes to neo4j')
	for r in n:
		try:
			with neo4j_instance.session() as neo4j_session:
				#node_id = re.sub(r'\'',r'\'', r.node_id)
				'''
				content = re.sub(r'\'',r'\'', r.node_content)
				content = re.sub(u"[^\u0000-\u007e]",r'', content)
				node_type = re.sub(r'[^A-z\d]+',r'_', r.node_type)
				re.sub(r'\'',r'\'', r.node_id)
				'''
				node_cmd = u"""
					CREATE (n:%s { id: '%s', content: '%s' });
					"""%(r.node_type, r.node_id, r.node_content)
				neo4j_session.run(node_cmd)
				#print(neo4j_cmd)
		except Exception as e: 
			print(e)
			#print(node_cmd)
			pass
	return None

def ingest_relation_json2neo4j(bolt_url,
	bolt_username,
	bolt_password,
	input_json,
	sqlContext = None,
	delect_neo4j = False):
	print("connecting to the neo4j server")
	neo4j_instance = GraphDatabase.driver(bolt_url, auth=(bolt_username, bolt_password))
	#neo4j_session = neo4j_instance.session()
	print("loading relation data from "+input_json)
	sqlContext.read.json(input_json).registerTempTable('input')
	input = sqlContext.sql(u"""
		SELECT DISTINCT * FROM input
		""")
	t = input.collect()
	print("loaded "+str(len(t))+' tripletes from '+input_json)
	with neo4j_instance.session() as neo4j_session:
		if delect_neo4j is True:
			print("deleting data of neo4j")
			neo4j_session.run(u"""
			MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r;
			""")
	print('inserting edges to neo4j')
	for r in t:
		try:
			with neo4j_instance.session() as neo4j_session:
				'''
				re.sub(r'[^A-z\d]+',r'_', r.subject_type)
				re.sub(r'[^A-z\d]+',r'_', r.object_type)
				re.sub(r'\'',r'\'', r.subject_id)
				re.sub(r'\'',r'\'', r.object_id),									
				re.sub(r'[^A-z]+',r'_', )
				'''
				neo4j_cmd = u"""
					MATCH (a:%s),(b:%s) WHERE a.id = '%s' AND b.id = '%s' 
					CREATE (a)-[r:%s]->(b);
					"""%(r.subject_type,r.object_type,
						r.subject_id,r.object_id,	
						r.relation)
				neo4j_session.run(neo4j_cmd)
		except Exception as e: 
			print(e)
			#print(neo4j_cmd)
	return None

#######jessica_neo4j.py#######
