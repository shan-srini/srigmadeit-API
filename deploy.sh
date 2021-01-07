#!/bin/bash

docker build . --tag gcr.io/neural-vista-301000/srigmadeit_api:$1

docker push gcr.io/neural-vista-301000/srigmadeit_api:$1

gcloud run deploy --image gcr.io/neural-vista-301000/srigmadeit_api:$1 --platform managed --max-instances 20