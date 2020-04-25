#Get full client image name. Version default to value in info.json if not specified
export IMAGE_REPO=$(cat ./info.json | jq -r ".image_repo")
export INFO_VERSION=$(cat ./info.json | jq -r ".version")
export VERSION=${OVERTURE_CLIENT_VERSION:-$INFO_VERSION}
export OVERTURE_CLIENT_IMAGE=$IMAGE_REPO:$VERSION

#If version was specified to 'dev', build the image locally
if [ "$VERSION" = "dev" ]; then
    docker build -t $OVERTURE_CLIENT_IMAGE .;
fi

#If WORKSPACE variable is not set, create a local test workspace with the example provided in the repo
if [ -z "$WORKSPACE" ]; then
    export WORKSPACE=$(pwd)/workspace
    if [ ! -d "$WORKSPACE" ]; then 
        mkdir -p $WORKSPACE
        cp -r example $WORKSPACE/example
    fi
fi

#Define defaults based on implicit local environment values if parameters are not passed
export OVERTURE_NETWORK=${OVERTURE_NETWORK:-overture}
export SONG_URL=${SONG_URL:-http://song-reverse-proxy:8888}
export SCORE_URL=${SCORE_URL:-http://score-reverse-proxy:8888} 
export KEYCLOAK_URL=${KEYCLOAK_URL:-https://keycloak:8443}
export MAIN_STUDY=${MAIN_STUDY:-ET00011}
export SCORE_CLIENT_IMAGE=${SCORE_CLIENT_IMAGE:-chusj/score-client:0.3}
export CONTAINER_NAME=${CONTAINER_NAME:-overture-client}

docker create -it --rm \
              --network $OVERTURE_NETWORK \
              -e "SONG_URL=$SONG_URL" \
              -e "SCORE_URL=$SCORE_URL" \
              -e "KEYCLOAK_URL=$KEYCLOAK_URL" \
              -e "KEYCLOAK_USERNAME=test" \
              -e "KEYCLOAK_PASSWORD=testpassword99" \
              -e "KEYCLOAK_SECRET=01b99f28-1331-4fec-903b-c2e8043cec77" \
              -e "SCORE_CLIENT_IMAGE=$SCORE_CLIENT_IMAGE" \
              -e "CONTAINER_NAME=$CONTAINER_NAME" \
              -e "OVERTURE_NETWORK=$OVERTURE_NETWORK" \
              -e "MAIN_STUDY=$MAIN_STUDY" \
              -v $WORKSPACE:/opt/workspace \
              -v /var/run/docker.sock:/var/run/docker.sock \
              -w /opt/workspace \
              --name $CONTAINER_NAME \
              $OVERTURE_CLIENT_IMAGE bash;
docker network connect proxy $CONTAINER_NAME;
docker start $CONTAINER_NAME;
docker attach $CONTAINER_NAME;