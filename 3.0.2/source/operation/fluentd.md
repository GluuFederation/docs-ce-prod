# External Logging using FluentD

## Overview

Gluu Server leverages FluentD to perform external logging, capturing detailed activities of
Gluu Server components like oxTrust and oxAuth. This provides you with more intel while working on 
an issue.

### Requirements:
 - FluentD
 - Active Gluu Server Installed
 - log4j2.xml for oxTrust and oxAuth
 
### FluentD Installation

FluentD can be downloaded and installed depending in the OS you are using. 
You can find instrucitons to download and install FluentD from [FluentD Docs](https://docs.fluentd.org/v0.12/articles/install-by-deb).

FluentD has to be installed outside of the chroot container.

### External logging configuration

1. Get log4j2.xml for oxAuth and oxTrust from respective github sources.
    * log4j2.xml for [oxAuth](https://github.com/GluuFederation/oxAuth/blob/master/Server/src/main/resources/log4j2.xml)
    * log42j.xml for [oxTrust](https://github.com/GluuFederation/oxTrust/blob/master/server/src/main/resources/log4j2.xml)
2. Copy log4j2.xml into the chroot container
3. Update log4j2.xml by adding [Fluency Appender](https://github.com/wywygmbh/log4j-plugin-fluency/blob/master/src/com/wywy/log4j/appender/FluencyAppender.java)
, like below

```xml
<Fluency name="fluency" tag="yourTag">
    <!-- all settings are optional, see defaultFluency() for default values -->
    <!-- you can add as may fields as you like (or none at all) -->
    <StaticField name="application">yourApplication</StaticField>
    <StaticField name="someOtherField">some value</StaticField>
    <Server host="primary-node" port="24224"/>
    <Server host="secondary-node" port="24224"/>
    <FluencyConfig
      ackResponseMode="true"
      fileBackupDir="/tmp/fluency"
      bufferChunkInitialSize="4194304"
      bufferChunkRetentionSize="16777216"
      maxBufferSize="268435456"
      waitUntilBufferFlushed="30"
      waitUntilFlusherTerminated="40"
      flushIntervalMillis="200"
      senderMaxRetryCount="12" />
</Fluency>
```
    
Simplest configuration could be like this ` <Fluency name="fluency" tag="oxTrust_Fluency"/>`

By default, FluencyAppender will connect to  `127.0.0.1:24224` .

!!!Note:
    Please make sure to open the required ports like `24224` and `24230`
    
For more about configuration, read [log4j fluency plugin documentation](https://github.com/wywygmbh/log4j-plugin-fluency).

4. Update the FluentD configuration file (e.g  `/etc/td-agent/td-agent.conf` ) by adding  `yourTag`

```
<match oxTrust_Fluency>
  @type stdout
</match>
```
    
For more about configuring FluentD, read the [config docs](https://docs.fluentd.org/v0.12/articles/config-file).

5. Restart FluentD using the following commands

```
    #/etc/init.d/td-agent stop
    
    #/etc/init.d/td-agent start
```

6. Restart oxTrust

    `service identity restart`

### Gluu oxTrust configuration

Logger has to be configured externally. 
In order to do this, 

1. Navigate to  `Configuration` >  `Configure Log Viewer`

2. Enter the path of your log4j2 configuration file to the `oxTrust External 
log4j location` field, repeat the same steps for `oxAuth External log4j2` location, 
if required.

3. Click on `update`

### Test and Sample logs

To test, whether the configuration has been captured correctly, 

check the logs in `/var/log/td-agent/td-agent.logs`. 
Log file can be specified to be generated in a particular path of your choice by editing `/etc/td-agent/td-agent.conf`

```
49577-11-18 19:54:59 +0200 oxtrust_FluentD: {"sourceLine":98,"@timestamp":"2017-08-10T10:07:18.899+0000","level":"INFO","logger":"o.g.o.s.s.l.LdapStatusTimer","sourceMethod":"logConnectionProviderStatistic","sourceClass":"org.gluu.oxtrust.service.status.ldap.LdapStatusTimer","loggerFull":"org.gluu.oxtrust.service.status.ldap.LdapStatusTimer","thread":"Thread-362","message":"connectionProvider statistics: LDAPConnectionPoolStatistics(numAvailableConnections=2, maxAvailableConnections=10, numSuccessfulConnectionAttempts=2, numFailedConnectionAttempts=0, numConnectionsClosedDefunct=0, numConnectionsClosedExpired=0, numConnectionsClosedUnneeded=0, numSuccessfulCheckouts=459, numFailedCheckouts=0, numReleasedValid=459)\n","sourceFile":"LdapStatusTimer.java"}
49577-11-18 19:55:00 +0200 oxtrust_FluentD: {"sourceLine":103,"@timestamp":"2017-08-10T10:07:18.900+0000","level":"ERROR","logger":"o.g.o.s.s.l.LdapStatusTimer","sourceMethod":"logConnectionProviderStatistic","sourceClass":"org.gluu.oxtrust.service.status.ldap.LdapStatusTimer","loggerFull":"org.gluu.oxtrust.service.status.ldap.LdapStatusTimer","thread":"Thread-362","message":"bindConnectionProvider is empty\n","sourceFile":"LdapStatusTimer.java"}
49577-11-18 20:05:10 +0200 oxtrust_FluentD: {"sourceLine":75,"@timestamp":"2017-08-10T10:07:19.510+0000","level":"WARN","logger":"o.k.f.s.RetryableSender","sourceMethod":"sendInternal","sourceClass":"org.komamitsu.fluency.sender.RetryableSender","loggerFull":"org.komamitsu.fluency.sender.RetryableSender","thread":"pool-5-thread-1","message":"Sender failed to send data. sender=RetryableSender{baseSender=TCPSender{channel=null, config=Config{baseConfig=org.komamitsu.fluency.sender.Sender$Config@1397656f, host='127.0.0.1', port=24224, connectionTimeoutMilli=5000, readTimeoutMilli=5000, heartbeaterConfig=null, failureDetectorConfig=Config{failureIntervalMillis=3000}, failureDetectorStrategyConfig=org.komamitsu.fluency.sender.failuredetect.PhiAccrualFailureDetectStrategy$Config@5c2c01a6}, 
failureDetector=null} org.komamitsu.fluency.sender.TCPSender@4c34ce47, retryStrategy=ExponentialBackOffRetryStrategy{config=Config{baseConfig=Config{maxRetryCount=7}, baseIntervalMillis=400, maxIntervalMillis=30000}} RetryStrategy{config=Config{maxRetryCount=7}}, isClosed=false} org.komamitsu.fluency.sender.RetryableSender@5753cf72, retry=0\njava.io.IOException: Connection reset by peer\n\tat sun.nio.ch.FileDispatcherImpl.writev0(Native Method) [?:1.8.0_112]\n\tat sun.nio.ch.SocketDispatcher.writev(SocketDispatcher.java:51) [?:1.8.0_112]\n\tat sun.nio.ch.IOUtil.write(IOUtil.java:148) [?:1.8.0_112]\n\tat sun.nio.ch.SocketChannelImpl.write(SocketChannelImpl.java:504) [?:1.8.0_112]\n\tat java.nio.channels.SocketChannel.write(SocketChannel.java:502) 
[?:1.8.0_112]\n\tat org.komamitsu.fluency.sender.TCPSender.sendBuffers(TCPSender.java:84) [fluency-1.1.0.jar:?]\n\tat org.komamitsu.fluency.sender.TCPSender.sendInternal(TCPSender.java:105) [fluency-1.1.0.jar:?]\n\tat org.komamitsu.fluency.sender.Sender.sendInternalWithRestoreBufferPositions(Sender.java:48) [fluency-1.1.0.jar:?]\n\tat org.komamitsu.fluency.sender.Sender.send(Sender.java:30) ~[fluency-1.1.0.jar:?]\n\tat org.komamitsu.fluency.sender.RetryableSender.sendInternal(RetryableSender.java:66) [fluency-1.1.0.jar:?]\n\tat org.komamitsu.fluency.sender.Sender.sendInternalWithRestoreBufferPositions(Sender.java:48) [fluency-1.1.0.jar:?]\n\tat org.komamitsu.fluency.sender.Sender.send(Sender.java:30) [fluency-1.1.0.jar:?]\n\tat org.komamitsu.fluency.buffer.PackedForwardBuffer.flushInternal(PackedForwardBuffer.java:230) 
[fluency-1.1.0.jar:?]\n\tat org.komamitsu.fluency.buffer.Buffer.flush(Buffer.java:81) [fluency-1.1.0.jar:?]\n\tat org.komamitsu.fluency.flusher.AsyncFlusher$1.run(AsyncFlusher.java:32) [fluency-1.1.0.jar:?]\n\tat java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1142) [?:1.8.0_112]\n\tat java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:617) [?:1.8.0_112]\n\tat java.lang.Thread.run(Thread.java:745) [?:1.8.0_112]\n","sourceFile":"RetryableSender.java"}
```