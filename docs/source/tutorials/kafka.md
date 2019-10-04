# Kafka logging for Gluu

## Overview

This tutorial offers a step-by-step guide for using [Apache Kafka](https://kafka.apache.org) to aggregate logs for oxAuth and oxTrust. 

## Process

1. From inside the chroot, unzip the oxAuth and Identity war files.

    ```
    # unzip -p /opt/gluu/jetty/oxauth/webapps/oxauth.war WEB-INF/classes/log4j2.xml > /opt/gluu/jetty/oxauth/resources/log4j2.xml
    # unzip -p /opt/gluu/jetty/identity/webapps/identity.war WEB-INF/classes/log4j2.xml > /opt/gluu/jetty/identity/resources/log4j2.xml
    ```
    
1. Download the Kafka Clients jar file and copy it into oxAuth and Identity.

    ```
    # mkdir /tmp/jars
    # wget http://central.maven.org/maven2/org/apache/kafka/kafka-clients/2.2.0/kafka-clients-2.2.0.jar -O /tmp/jars/kafka-clients-2.2.0.jar
    # wget http://central.maven.org/maven2/org/lz4/lz4-java/1.5.0/lz4-java-1.5.0.jar -O /tmp/jars/lz4-java-1.5.0.jar
    # wget http://central.maven.org/maven2/org/slf4j/slf4j-api/1.7.25/slf4j-api-1.7.25.jar -O /tmp/jars/slf4j-api-1.7.25.jar
    # wget http://central.maven.org/maven2/org/xerial/snappy/snappy-java/1.1.7.2/snappy-java-1.1.7.2.jar -O /tmp/jars/snappy-java-1.1.7.2.jar
    # wget http://central.maven.org/maven2/com/github/luben/zstd-jni/1.3.8-1/zstd-jni-1.3.8-1.jar -O /tmp/jars/zstd-jni-1.3.8-1.jar
    # cp /tmp/jars/*.jar /opt/gluu/jetty/oxauth/lib/ext/
    # cp /tmp/jars/*.jar /opt/gluu/jetty/identity/lib/ext/
    # rm -rf /tmp/jars
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
