#!/bin/bash
# Don't run this script unless virtualenv is activated

if [ $# -ne 1 ]; then
    echo "USAGE: ./deploy TAG_NAME (latest, v1.0, etc)"
    exit 1
fi

docker build . --tag gcr.io/neural-vista-301000/srigmadeit_api:$1

docker push gcr.io/neural-vista-301000/srigmadeit_api:$1

# will set env variable using this.
RAND_SECRET=$(openssl rand -base64 32)

gcloud run deploy srigmadeit-api \
--image gcr.io/neural-vista-301000/srigmadeit_api:$1 \
--platform managed \
--max-instances 50 \
--concurrency 10 \
--set-env-vars "JWT_RANDOM_SECRET=$RAND_SECRET" \
--set-env-vars "B2_COS_ACCESS_KEY_ID=$B2_COS_ACCESS_KEY_ID" \
--set-env-vars "B2_COS_ENDPOINT=$B2_COS_ENDPOINT" \
--set-env-vars "B2_COS_SECRET_ACCESS_KEY=$B2_COS_SECRET_ACCESS_KEY" \
--set-env-vars "DB_NAME=$DB_NAME" \
--set-env-vars "MONGO_DB_CONNECT=$MONGO_DB_CONNECT" \
--set-env-vars "ORACLE_COS_ACCESS_KEY_ID=$ORACLE_COS_ACCESS_KEY_ID" \
--set-env-vars "ORACLE_COS_ENDPOINT=$ORACLE_COS_ENDPOINT" \
--set-env-vars "ORACLE_COS_SECRET_ACCESS_KEY=$ORACLE_COS_SECRET_ACCESS_KEY" \
--set-env-vars "SRIG_PASS=$SRIG_PASS" \
--set-env-vars "SRIG_USER=$SRIG_USER";

# Need to delete all untagged images, since overriding a tag like latest
# Will cause the previous image to be untagged, and is therefore trash
# Below command lists all container images and their tags, can use this to iterate and delete as necessary
#gcloud container images list-tags gcr.io/neural-vista-301000/srigmadeit_api --format=json --limit=unlimited
