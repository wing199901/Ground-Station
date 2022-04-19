# docker pull aerosimcontainerregistry.azurecr.io/ground-station-api:20220411
FROM python:alpine as base

FROM base as builder
# install dependencies
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM base
# copy only the dependencies installation from the 1st stage image
COPY --from=builder /root/.local /root/.local

COPY . /app
WORKDIR /app

# update PATH environment variable
ENV PATH=/home/app/.local/bin:$PATH

CMD ["python", "api.py"]