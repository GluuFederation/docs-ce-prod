# Enable Kafka Logging with the Gluu Server

## Overview

### Process

(Inside the chroot)

```
# unzip -p /opt/gluu/jetty/oxauth/webapps/oxauth.war WEB-INF/classes/log4j2.xml > /opt/gluu/jetty/oxauth/resources/log4j2.xml

# unzip -p /opt/gluu/jetty/identity/webapps/identity.war WEB-INF/classes/log4j2.xml > /opt/gluu/jetty/identity/resources/log4j2.xml
# wget http://central.maven.org/maven2/org/apache/kafka/kafka-clients/2.1.1/kafka-clients-2.1.1.jar
[1] -O /tmp/kafka-clients-2.1.1.jar
# cp /tmp/kafka-clients-2.1.1.jar /opt/gluu/jetty/oxauth/custom/libs/
# cp /tmp/kafka-clients-2.1.1.jar /opt/gluu/jetty/identity/custom/libs/

##

EDIT LOG4J2.XML IN BOTH /OPT/GLUU/JETTY/OXAUTH/RESOURCES AND /OPT/GLUU/JETTY/IDENTITY/RESOURCES.
UNDER SECTION APPENDERS ADD

%m%n”/>
name="bootstrap.servers"="">KAFKA-1.MY.DOMAIN:9094,KAFKA-2.MY.DOMAIN:9094,...

gzip
/PATH/TO/TRUSTSTORE.JKS
PASSWORD_FOR_TRUSTSTORE
SSL

AND UNDER EACH LOGGER (DON’T FORGET THE ROOT LOGGER) IN SECTION LOGGERS THAT HAVE A APPENDERREF ADD

ADD "-DLOG4J.CONFIGURATIONFILE=RESOURCES/LOG4J2.XML” TO JAVA_OPTIONS IN /ETC/DEFAULT/OXAUTH AND /ETC/DEFAULT/IDENTITY

# systemctl daemon-reload
# service oxauth restart && service identity restart
```
