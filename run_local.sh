docker build -t overture-clin-client:latest .;

WORKSPACE=$(pwd)/workspace
if [ ! -d "$WORKING_DIR" ]; then 
    mkdir -p $WORKSPACE
    cp -r example $WORKSPACE/example
fi

docker run -it --rm \
           --network overture \
           -e "ELASTICSEARCH_URL=http://elasticsearch:9200" \
           -e "SONG_URL=http://song-reverse-proxy:8888" \
           -e "KEYCLOAK_URL=https://keycloak:8443" \
           -e "KEYCLOAK_USERNAME=test" \
           -e "KEYCLOAK_PASSWORD=testpassword99" \
           -e "KEYCLOAK_SECRET=8c06ee4d-461b-45a9-b50f-1ed176699c1b" \
           -v $WORKSPACE:/opt/workspace \
           -w /opt/workspace \
           overture-clin-client:latest bash;