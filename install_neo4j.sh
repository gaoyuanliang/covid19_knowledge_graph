download from 

http://neo4j.com/artifact.php?name=neo4j-community-3.5.12-unix.tar.gz

unzip it 

tar -xf 'artifact.php?name=neo4j-community-3.5.12-unix.tar.gz'

cd neo4j-community-3.5.12

echo "dbms.security.auth_enabled=false" > neo4j.conf

bin/neo4j stop
bin/neo4j start

http://localhost:7474/

bolt://localhost:7687
neo4j
neo4j

reset new password to 
neo4j1


try the cypher code:
MATCH (n) RETURN n LIMIT 1