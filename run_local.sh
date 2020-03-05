docker build -t overture-clin-client:latest .;
docker run -it --rm \
           --network overture \
           -e "ELASTICSEARCH_URL=http://elasticsearch:9200" \
           overture-clin-client:latest bash;