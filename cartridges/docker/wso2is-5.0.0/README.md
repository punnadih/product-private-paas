# WSO2 IS 5.0.0 Dockerfile

WSO2 IS 5.0.0 Dockerfile defines required resources for building a Docker image with WSO2 IS 5.0.0.

## How to build

1. Copy following files to the packages folder:
```
wso2is-5.0.0.zip
wso2is-5.0.0-template-module-<PPAAS_VERSION>.zip
```

2. Run build.sh file to build the docker image:
```
sh build.sh
```

3. List docker images:
```
docker images
```