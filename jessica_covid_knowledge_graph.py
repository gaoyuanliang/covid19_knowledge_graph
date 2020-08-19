import re
from jessica_neo4j import *
from jessica_local_spark_building import *

'''
?s ?sLabel ?sAltLabel ?st ?stLabel ?rp ?rpLabel 
'''

def extract_wiki_id(input):
	return re.search(r'\/(?P<entity>[A-Z\d]+)$', input).group('entity')

udf_extract_wiki_id = udf(extract_wiki_id, StringType())

def conver_entity_type_to_neo4j_format(input):
	input = input.strip()
	input = re.sub(r'^[^a-z]+', '', input)
	input = re.sub(r'[^a-z]+$', '', input)
	return re.sub(r'[^a-z]+', '_', input)

udf_conver_entity_type_to_neo4j_format = udf(conver_entity_type_to_neo4j_format, StringType())

def conver_entity_name_to_neo4j_format(input):
	input = input.strip()
	return re.sub(r'\'', '\\\'', input)

udf_conver_entity_name_to_neo4j_format = udf(conver_entity_name_to_neo4j_format, StringType())

'''
'''

sqlContext.read.format('csv').option('header', 'true').load('query_country.csv').registerTempTable('query_country')
sqlContext.read.format('csv').option('header', 'true').load('query_country_1.csv').registerTempTable('query_country_1')

sqlContext.sql(u"""
	SELECT DISTINCT s AS node_id, sLabel AS node_content, stLabel AS node_type
	FROM query_country
	UNION ALL 
	SELECT DISTINCT s AS node_id, sLabel AS node_content, stLabel AS node_type
	FROM query_country_1
	UNION ALL 
	SELECT DISTINCT o AS node_id, oLabel AS node_content, otLabel AS node_type
	FROM query_country
	UNION ALL 
	SELECT DISTINCT o AS node_id, oLabel AS node_content, otLabel AS node_type
	FROM query_country_1
	""").write.mode('Overwrite').json('temp')

sqlContext.read.json('temp').registerTempTable('temp')

sqlContext.sql(u"""
	SELECT node_id, 
	COLLECT_SET(node_content)[0] AS node_content,
	COLLECT_SET(node_type)[0] AS node_type
	FROM temp
	WHERE node_id IS NOT NULL
	GROUP BY node_id
	""")\
.withColumn('node_id', udf_extract_wiki_id('node_id'))\
.withColumn('node_type', udf_conver_entity_type_to_neo4j_format('node_type'))\
.withColumn('node_content', udf_conver_entity_name_to_neo4j_format('node_content'))\
.write.mode('Overwrite').json('node.json')

ingest_node_json2neo4j(
	bolt_url = 'bolt://localhost:7687',
	bolt_username = 'neo4j',
	bolt_password = 'neo4j1',
	input_json = 'node.json',
	sqlContext = sqlContext,
	delect_neo4j = True)

'''
?s ?sLabel ?sAltLabel ?st ?stLabel 
?rp ?rpLabel 
?o ?oLabel ?oAltLabel ?ot ?otLabel 
'''

sqlContext.sql(u"""
	SELECT DISTINCT s AS subject_id,
	stLabel AS subject_type,
	o AS object_id,
	otLabel AS object_type,
	rpLabel AS relation
	FROM query_country
	WHERE s IS NOT NULL 
	AND o IS NOT NULL 
	AND stLabel IS NOT NULL
	AND otLabel IS NOT NULL
	AND rpLabel IS NOT NULL
	""")\
.withColumn('subject_id', udf_extract_wiki_id('subject_id'))\
.withColumn('object_id', udf_extract_wiki_id('object_id'))\
.withColumn('subject_type', udf_conver_entity_type_to_neo4j_format('subject_type'))\
.withColumn('object_type', udf_conver_entity_type_to_neo4j_format('object_type'))\
.withColumn('relation', udf_conver_entity_type_to_neo4j_format('relation'))\
.write.mode('Overwrite').json('relation.json')

ingest_relation_json2neo4j(
	bolt_url = 'bolt://localhost:7687',
	bolt_username = 'neo4j',
	bolt_password = 'neo4j1',
	input_json = 'relation.json',
	sqlContext = sqlContext,
	delect_neo4j = False)