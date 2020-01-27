# DocumentReader - Django
This app takes a random URL id an returns a pdf or png or json error.

Variables to be substituted are denoted by: `<>`

### General Dependencies
- [Dummy-PDF-or-PNG:](https://github.com/e-conomic/hiring-assigments/tree/master/sre/dummy-pdf-or-png)

### Local Dependencies
- Docker or MiniKube

### Cloud Dependencies
- GCP Project
- GKE
- CloudBuild
- Cloud Source Repository
- Gcloud SDK


## Running Locally:

1. Clone Dummy-PDF-or-PNG project into current repo
```
git clone https://github.com/e-conomic/hiring-assigments.git
```
Note:
- Possible issue:  `missing git-lfs`

- Solution: install git-lfs package either from `brew`, `apt`, `yum` or your system package manager.

2. Build Docker Image for Dummy-PDF-or-PNG:

Subtitute dummy-image-name for preferred docker image name.
```
docker build -f hiring-assigments/sre/dummy-pdf-or-png/Dockerfile -t <dummy-image-name> ./hiring-assigments/sre/dummy-pdf-or-png/
```

3. Build Docker Image for DocumentReader:
```
docker build -t <reader-image-name .>
```

4. Run the Backend (Dummy-PDF-or-PNG):
```
docker run --name dummy --rm -it -p 3000:3000 <dummy-image-name>
```

5. Run the Frontend (DocumentReader):
```
docker run --name reader --rm --link dummy:dummy -e "DEBUG=False" -e "BASE_URL=http://dummy:3000" -e "DJANGO_ALLOWED_HOSTS=localhost" -it -p 8000:8000 reader python manage.py runserver 0.0.0.0:8000
```

6 Visit the app on: http://localhost:8000


## Running in GCP:

Ensure that the GCP Project is provisioned.
Instructions on that IaaC is in this repository:
https://github.com/emmanuelstroem/documentreader_iaac.git

### Setup:
1. Get Cluster Config:

```
gcloud container clusters get-credentials <cluster-name> --zone=<cluster-zone>
```

2. Deploy Namespace, Service and Ingress:
>Create Global IP addresses with names specified in the Ingress `global-ip-name` to be able to setup managed SSL certificates later on.

>Specify the name of ssl-cert to use in this step BEFORE creating the certificate.

```
kubectl apply -f .kubernetes/namespace_service_ingress.yaml
```

3. Deploy Dummy-PDF-or-PNG Deployment :P
```
kubectl apply -f .kubernetes/deployment_dummy.yaml
```

4. Deploy DocumentReader Deployment:
```
kubectl apply -f .kubernetes/deployment_reader.yaml
```

5. SSL Certificates:
>Important to first point the domains to the Global IP addresses as specified in `step 2` above:

>Specify the domain to be used to access the service

> Specify the name of the cerficicate to match `step 2`
```
kubectl apply -f .kubernetes/managed_ssl_certs.yaml
```

6. Access the Application through the Ingress IP or using the domain name specified in `step 5`



## Production Ready:
- private cluster
- vpc
- useful logging
- fail safe
- resource limit
- internal service communication
- healthcheck

