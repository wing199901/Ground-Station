
az login
az acr login --name aerosimcontainerregistry.azurecr.io
cd API
docker build --pull --rm -f Dockerfile -t aerosimcontainerregistry.azurecr.io/ground-station-api:[date] .
