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
    # cp /path/to/kafka/libs/kafka-clients-x.y.z.jar /opt/gluu/jetty/oxauth/custom/libs/
    # cp /path/to/kafka/libs/kafka-clients-x.y.z.jar /opt/gluu/jetty/identity/custom/libs/
    ```
    
1. Make the following changes to `log4j2.xml` in both `/opt/gluu/jetty/oxauth/resources` and `/opt/gluu/jetty/identity/resources`:
    - Under section appenders, add:

        ```
        <Kafka name="Kafka" topic="my-gluu-topic">
        <PatternLayout pattern="%d %-5p [kafka] [%t] [%C{6}] (%F:%L) - %m%n"/>  
        <Property name="bootstrap.servers"=>KAFKA-1.MY.DOMAIN:9092,KAFKA-2.MY.DOMAIN:9092,...</Property>
    
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
        
1. Add **-Dlog4j.configurationFile=/opt/gluu/jetty/oxauth/resources/log4j2.xml** to `java_options` in `/etc/default/oxauth` and  **-Dlog4j.configurationFile=/opt/gluu/jetty/identity/resources/log4j2.xml** to `java_options` in `/etc/default/identity`.

1. [Restart](../operation/services.md#restart) the `oxauth` and `identity` services

1. Log out of the chroot and reload systemd with the following command:

    ```
    systemctl daemon-reload
    ```
