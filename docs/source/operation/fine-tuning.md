# Fine Tuning Gluu Server
The Gluu Server has a stateless architecture and scales quite well out-of-the-box. However, to achieve maximum performance, the following server components must be tuned accordingly: 

- Operating System (OS)    
- Memory and infrastructure   
- LDAP        
- Web application container (Jetty, JBoss)   
- Gluu Server configurations    

## OS Tuning

The Gluu Server is designed for Linux. Therefore, the following can be tuned as needed:   

!!! Note
    Most of the configurations below can be tuned in `/etc/security/limits.conf`, however it may depend on OS. 

1. Increase TCP Buffer Sizes

   ```
   sysctl -w net.core.rmem_max=16777216
   sysctl -w net.core.wmem_max=16777216
   sysctl -w net.ipv4.tcp_rmem="4096 87380 16777216"
   sysctl -w net.ipv4.tcp_wmem="4096 16384 16777216"
   ```

1. Increase connection listening size

   ```
   sysctl -w net.core.somaxconn=4096
   sysctl -w net.core.netdev_max_backlog=16384
   sysctl -w net.ipv4.tcp_max_syn_backlog=8192
   sysctl -w net.ipv4.tcp_syncookies=1
   ```

1. Increase ports range

   ```
   sysctl -w net.ipv4.ip_local_port_range="1024 65535"
   sysctl -w net.ipv4.tcp_tw_recycle=1
   ```

1. Increase file descriptors

   ```
   * soft nofile 65536
   * hard nofile 262144
   ```

## Memory and infrastructure

Make sure there is enough memory for each Gluu Server component (e.g. LDAP Server, Jetty). For high load systems, it can be helpful to have each component on separate machine.   

## LDAP Server

!!! Note
    For convenience, all samples are for Gluu OpenDJ. However, these are general recommendations that should apply for other LDAP Servers too.

1. Maximum allowed connections: If there are not enough connections to serve the client, a connection is put "on hold". To avoid delays, provide the expected maximum allowed connections, e.g.:

    ```
    max-allowed-client-connections=1000
    ```
    
1. LDAP Server resources: Make sure to provide enough resources to LDAP. For example, OpenDJ uses JVM for running. For high performance, make sure enough memory is provided via the JVM system properties.
    
1. Use cache as much as possible. For example: 

   ```
   dsconfig -n set-backend-prop --backend-name userRoot --set db-cache-percent:50
   ```

1. Additional LDAP performance resources can be found in the dollowing docs: 

   - [OpenDJ Performance Tuning](https://backstage.forgerock.com/#!/docs/opendj/2.6.0/admin-guide/chap-tuning) 
   - [OpenDJ Global configuration](http://opendj.forgerock.org/opendj-server/configref/global.html#max-allowed-client-connections). 


## Jetty

By default, jetty's task queue is unlimited. If load is expected to be high, limit the task queue. Configuration may vary for each particular scenario.

Example configuration:

```
<Configure id="Server" class="org.eclipse.jetty.server.Server">
    <Set name="ThreadPool">
      <New class="org.eclipse.jetty.util.thread.QueuedThreadPool">
        <!-- specify a bounded queue -->
        <Arg>
           <New class="java.util.concurrent.ArrayBlockingQueue">
              <Arg type="int">6000</Arg>
           </New>
      </Arg>
        <Set name="minThreads">10</Set>
        <Set name="maxThreads">200</Set>
        <Set name="detailedDump">false</Set>
      </New>
    </Set>
</Configure>
```

## Gluu Server

- oxauth-ldap.properties: Increase the LDAP connection pool size, e.g.: 

   ```
   maxconnections: 1000
   ```

- Make sure logging is turned OFF. Logging blocks threads and has a significant impact on performance. First test with low load, then test for high load with logging completely off. To turn off logging, in oxTrust navigate to `Configuration -> JSON Configuration -> oxAuth Configuration` and set `loggingLevel:` to `OFF`. Check the log files to confirm logging is off.
 
- Turn off metrics. Gathering metrics also impacts performance. To turn metrics off, in oxTrust navigate to: `Configuration -> JSON Configuration -> oxAuth Configuration`, and set `metricReporterEnabled:` to `false`.
