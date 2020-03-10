docker build -t overture-clin-client:latest .;
docker run -it --rm \
           --network overture \
           -e "ELASTICSEARCH_URL=http://elasticsearch:9200" \
           -e "SONG_URL=http://song-reverse-proxy:8888" \
           -e "KEYCLOAK_URL=https://keycloak:8443" \
           -e "KEYCLOAK_USERNAME=test" \
           -e "KEYCLOAK_PASSWORD=testpassword99" \
           -e "KEYCLOAK_SECRET=01729864-1f9f-4d16-b728-2fa87767541c" \
           overture-clin-client:latest bash;