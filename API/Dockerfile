# docker pull aerosimcontainerregistry.azurecr.io/ground-station-api:20220411
FROM python:alpine as base

FROM base as builder
# install dependencies
RUN mkdir /install
WORKDIR /install

COPY requirements.txt .
RUN pip install --root --install-option="--prefix=/install" -r requirements.txt

FROM base
# copy only the dependencies installation from the 1st stage image
COPY --from=builder /install /usr/local

COPY . /app
WORKDIR /app

CMD ["python", "api.py"]