# Fine Tuning Gluu Server
Gluu Server has a stateless architecture and scales quite easily. However to achieve high-performance, the server must be tuned accordingly.

Tuning consists of:

- OS Tuning   
- Memory and infrastructure   
- LDAP Server (Gluu OpenDJ)      
- Web Application Container (Tomcat, Jetty, JBoss)   
- Gluu Server configuration Tuning    

## OS Tuning

CE is designed to work on Linux, therefore it's recommended to tune the following:

!!! Note
    Most ofthe below configuration can be tuned in `/etc/security/limits.conf`, however it may depend on OS. 

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
    For convenience all samples stick to Gluu OpenDJ, however general recommendations are the same for other LDAP Servers.

1. Maximum number of allowed connections: If there are not enough connections to serve the client, a connection is
put "on hold" and waits. To avoid delays it's recommended to provide expected maximum allowed connections, e.g. 

    ```
    max-allowed-client-connections=1000
    ```
    
1. Provide enough resources to LDAP Server: For example OpenDJ uses JVM for running, for high performance it's
    recommended to give enough memory via JVM system properties.
1. Allow LDAP Server use cache as much as possible.

   ```
   dsconfig -n set-backend-prop --backend-name userRoot --set db-cache-percent:50
   ```

## Jetty

By default jetty task queue is not limited. If it's expected get high load then it make sense to limit it. Also configuration may depend for each particular example.

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

- oxauth-ldap.properties - Increase ldap connection pool size
```
     maxconnections: 1000
```

- Make sure logging is completely OFF. Logging blocks threads and have very big impact on performance. First test CE with low load and then for high load turn off logging completely.
In `Configuration -> JSON Configuration -> oxAuth Configuration` set `loggingLevel: OFF`. Check log files whether logging is really off.
 
- Turn off metrics. Login to oxTrust and in `Configuration -> JSON Configuration -> oxAuth Configuration` set `metricReporterEnabled: false`.

## Gluu Server Benchmark

Single CE node performance depends on cache provider. 

- IN MEMORY - average performance 120req/s 
- MEMCACHED - 120 req/s with thread count lower 100. If load with more then 100 threads, rejections start to appear. ~120 threads - ~1% of rejections, with ~400 threads - 20% of rejections.
- REDIS - 130 req/s, around 1% of errors (20000 requests processed). The nature of errors is under investigation, we will update this page once we figure out the reason of this 1% of errors.

# Useful Links

- [OpenDJ Performance Tuning](https://backstage.forgerock.com/#!/docs/opendj/2.6.0/admin-guide/chap-tuning)
- [OpenDJ Global configuration](http://opendj.forgerock.org/opendj-server/configref/global.html#max-allowed-client-connections)
