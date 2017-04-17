# Message-consumer:
Prepare a new vm for message consumer.

## Install mysql:
Mysql database,
```
# apt-get install mysql-server
```

## Prerequisites:
```
# apt-get update
# apt-get install openjdk-7-jdk wget unzip
```

## Install maven:
```
# wget http://www-us.apache.org/dist/maven/maven-3/3.3.9/binaries/apache-maven-3.3.9-bin.tar.gz -P /tmp
# tar xf /tmp/apache-maven-3.3.9-bin.tar.gz -C /opt
# rm -rf /tmp/apache-maven-3.3.9-bin.tar.gz
# export PATH=/opt/apache-maven-3.3.9/bin:$PATH
```

## Manual install activemq
Download it form this location using a web browser,
http://www.apache.org/dyn/closer.cgi?filename=/activemq/5.14.3/apache-activemq-5.14.3-bin.tar.gz&action=download
```
tar xf /tmp/apache-activemq-5.14.3-bin.tar.gz -C /opt
mv /opt/apache-activemq-5.14.3 /opt/activemq
```

Start activemq,
```
/opt/activemq/bin/activemq start
```

Check activemq server,
```
http://localhost:8161/admin
```

## Build:
Building message-consumer,
```
git clone https://github.com/GluuFederation/message-consumer.git
cd message-consumer
mvn -Pprod clean package
```

## Add sql schema to mysql
get schema from here, https://github.com/GluuFederation/message-consumer/blob/master/schema/mysql_schema.sql

```
source ${path_to_file}/mysql_schema.sql
```

##Configure oxauth-server logging
To configure oxauth-server to send logging messages via JMS,
just add JMSAppender into log4j2.xml e.g (https://github.com/GluuFederation/oxAuth/blob/master/Server/src/main/resources/log4j2.xml)
```
    <JMS name="jmsQueue"
        destinationBindingName="dynamicQueues/oxauth.server.logging"
        factoryName="org.apache.activemq.jndi.ActiveMQInitialContextFactory"
        factoryBindingName="ConnectionFactory"
        providerURL="tcp://localhost:61616"
        userName="admin"
        password="admin">
    </JMS>
```
and <AppenderRef ref="jmsQueue"/> to the root tag in the log4j2.xml file.
More about JMSAppender you can read here.

## run message-consumer:
```
java -jar target/message-consumer-0.0.1-SNAPSHOT.jar --database=mysql
```

