# WSO2 AS 5.2.1 Dockerfile

WSO2 AS 5.2.1 Dockerfile defines required resources for building a Docker image with WSO2 AS 5.2.1.

## How to build

1. Copy following files to the packages folder:
```
jdk-7u60-linux-x64.tar
wso2as-5.2.1.zip
wso2as-5.2.1-template-module-<version>.zip
mysql-connector-java-<version>-bin.jar (Note: Change the MYSQL_CONNECTOR_VERSION value in Dockerfile accordingly)
appfactory jars to be copied to dropins folder:
    org.wso2.carbon.appfactory.eventing_<version>.jar
    org.wso2.carbon.appfactory.common_<version>.jar
    org.wso2.carbon.appfactory.ext-<version>.jar
    org.wso2.carbon.appfactory.application.mgt.stub_<version>.jar
nimbus jar to be copied to dropins folder
```

2. Run build.sh file to build the docker image:
```
sh build.sh
```

3. List docker images:
```
docker images
```