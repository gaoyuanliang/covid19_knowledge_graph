# Covid 19 Knowledge Graph
Knowledge graph of covid19

<img src="https://github.com/gaoyuanliang/covid_knowledge_graph/raw/master/WX20200819-180451%402x.png" width="800">

## installation 

### installation of noe4j

```bash
wget http://neo4j.com/artifact.php?name=neo4j-community-3.5.12-unix.tar.gz
tar -xf 'artifact.php?name=neo4j-community-3.5.12-unix.tar.gz'
cd neo4j-community-3.5.12
bin/neo4j start
```

go to url 
```bash
http://localhost:7474/

bolt://localhost:7687
user name:neo4j
password neo4j
```

reset new password to 
```bash
neo4j1
```

### installation of pyspark and neo4j package

```bash
pip3 install pyspark
pip3 install neo4j
```

# data collection 

collect the entities and relationships of covid 19 from wikibase by sparql  at https://query.wikidata.org/

# building knowledge graph at neo4j 

convert them to nodes and edges of noe4j

ingest them to noe4j

build use cases from no4j 
