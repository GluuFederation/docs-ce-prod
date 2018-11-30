# Central logging

The message-consumer software centralizes all oxauth logs by exposing a RESTful API that enables quick searching of custom conditions.

## Log Node:

It is recommended to setup a new VM for the message-consumer software.

## Prerequisites

You will need MySQL, Java, Maven, ActiveMQ, Unzip and wget installed on the VM. 

```
# apt-get update
# apt-get install openjdk-7-jdk-headless wget unzip mysql-server
# apt-get install mysql-server
# mysql_secure_installation
```

### Install Maven
```
# wget http://www-us.apache.org/dist/maven/maven-3/3.3.9/binaries/apache-maven-3.3.9-bin.tar.gz -P /tmp
# tar xf /tmp/apache-maven-3.3.9-bin.tar.gz -C /opt
# rm -rf /tmp/apache-maven-3.3.9-bin.tar.gz
# export PATH=/opt/apache-maven-3.3.9/bin:$PATH
```

### Manual install ActiveMQ
Using a web browser, download ActiveMQ from the following location:
http://www.apache.org/dyn/closer.cgi?filename=/activemq/5.14.3/apache-activemq-5.14.3-bin.tar.gz&action=download

```
tar xf /tmp/apache-activemq-5.14.3-bin.tar.gz -C /opt
mv /opt/apache-activemq-5.14.3 /opt/activemq
```
Start ActiveMQ:

```
/opt/activemq/bin/activemq start
```

Change ActiveMQ default admin password.

## Build and install message-consumer
Clone message-consumer from github then run the following commands:

```
git clone https://github.com/GluuFederation/message-consumer.git
cd message-consumer
mvn -Pprod clean package
mv message-consumer-master/target/message-consumer-0.0.1-SNAPSHOT.jar /opt
```

## Add SQL schema to MySQL

Get schema from here, https://github.com/GluuFederation/message-consumer/blob/master/schema/mysql_schema.sql
and login to the MySQL shell:

```
source /path/to/file/mysql_schema.sql
```

## Configure oxauth-server logging
To configure [oxauth-server](https://github.com/GluuFederation/oxAuth/tree/master/Server) to send logging messages via JMS, just add JMSAppender into [log4j2.xml](https://github.com/GluuFederation/oxAuth/blob/master/Server/src/main/resources/log4j2.xml) e.g:

```
    <JMS name="jmsQueue"
        destinationBindingName="dynamicQueues/oxauth.server.logging"
        factoryName="org.apache.activemq.jndi.ActiveMQInitialContextFactory"
        factoryBindingName="ConnectionFactory"
        providerURL="tcp://mc.gluu.private:61616"
        userName="admin"
        password="{yourpass}">
    </JMS>

```
and `<AppenderRef ref="jmsQueue"/>` to the `root` tag in the [log4j2.xml](https://github.com/GluuFederation/oxAuth/blob/master/Server/src/main/resources/log4j2.xml#L139) file.

## message-consumer properties file

Message-consumer needs a properties file to run. Add the following content in `/etc/message-consumer/prod-mc-mysql.properties` : 

```
spring.activemq.broker-url=failover:(tcp://localhost:61616)?timeout=5000
spring.activemq.user=admin
spring.activemq.password={yourpass}
spring.activemq.packages.trust-all=true

#spring.datasource.url=jdbc:mysql://localhost:3306/gluu_log
spring.datasource.username=root
spring.datasource.password={yourpass}

spring.jpa.database=mysql
spring.jpa.database-platform=org.hibernate.dialect.MySQL5InnoDBDialect

spring.data.rest.base-path=/logger/api
spring.data.rest.default-page-size=20
spring.data.rest.max-page-size=100

server.port=9339


# ===================================================================
# message-consumer specific properties
# ===================================================================
message-consumer.oauth2-audit.destination=oauth2.audit.logging
message-consumer.oauth2-audit.days-after-logs-can-be-deleted=365
#every day at 1:01:am
message-consumer.oauth2-audit.cron-for-log-cleaner=0 1 1 * * ?

message-consumer.oxauth-server.destination=oxauth.server.logging
message-consumer.oxauth-server.days-after-logs-can-be-deleted=10
#every day at 1:01:am
message-consumer.oxauth-server.cron-for-log-cleaner=0 1 1 * * ?
```

## run message-consumer

```
java -jar /opt/message-consumer-0.0.1-SNAPSHOT.jar --spring.config.location=/etc/message-consumer/ --spring.config.name=prod-mc-mysql --database=mysql
```

## Adding message-consumer to cluster

Simply add the IP of the message-consumer node in the chroot `/etc/hosts` file of host-1 and host-2.
