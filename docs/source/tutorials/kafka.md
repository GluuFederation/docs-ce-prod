# Enable Kafka Logging with the Gluu Server

## Overview

This tutorial offers a step-by-step guide to enable [Apache Kafka log aggregation](https://kafka.apache.org) in the Gluu Server. 

## Process

1. From inside the chroot, unzip the oxAuth and Identity war files.

    ```
    # unzip -p /opt/gluu/jetty/oxauth/webapps/oxauth.war WEB-INF/classes/log4j2.xml > /opt/gluu/jetty/oxauth/resources/log4j2.xml
    # unzip -p /opt/gluu/jetty/identity/webapps/identity.war WEB-INF/classes/log4j2.xml > /opt/gluu/jetty/identity/resources/log4j2.xml
    ```
1. Download the Kafka Clients jar file and copy it into oxAuth and Identity.

    ```
    # wget http://central.maven.org/maven2/org/apache/kafka/kafka-clients/2.1.1/kafka-clients-2.1.1.jar -O /tmp/kafka-clients-2.1.1.jar
    # cp /tmp/kafka-clients-2.1.1.jar /opt/gluu/jetty/oxauth/custom/libs/
    # cp /tmp/kafka-clients-2.1.1.jar /opt/gluu/jetty/identity/custom/libs/
    ```
    
1. Make the following changes to `log4j2.xml` in both `/opt/gluu/jetty/oxauth/resources` and `/opt/gluu/jetty/identity/resources`:
    - Under section appenders, add:

        ```
        <Kafka name="Kafka" topic="my-gluu-topic">
        <PatternLayout pattern="%d %-5p [oxauth] [%t] [%C{6}] (%F:%L) - %m%n"/>  
        <Property name="bootstrap.servers"=>KAFKA-1.MY.DOMAIN:9094,KAFKA-2.MY.DOMAIN:9094,...</Property>
    
        <Property name="compression.type">gzip</Property>
        <Property name="ssl.truststore.location">/PATH/TO/truststore.jks</Property>
        <Property name="ssl.truststore.password">PASSWORD_FOR_TRUSTSTORE</Property>
        <Property name="security.protocol">SSL</Property>
        </Kafka>
        ```
    
    - Under each logger, **including the root logger**, in sections that have an `AppenderRef`, add:
    
        ```
        <AppenderRef ref="Kafka" />
        ```
        
1. Add "-dlog4j.configurationfile=resources/log4j2.xml" to `java_options` in both `/etc/default/oxauth` and `/etc/default/identity`

1. Restart systemd, oxAuth, and Identity

    ```
    # service oxauth restart && service identity restart
    # logout
    # systemctl daemon-reload
    ```
