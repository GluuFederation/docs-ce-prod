# Managing JVM's memory allocations in Gluu Server

Gluu server is powered by Java, with each its core component dwelling 
in a separate JVM (Java Virtual Machine) running inside of container.

When any internal Gluu's service is started with a command like `# service oxauth start`,
a corresponding JVM is launched with a set of predetermined parameters passed 
to it in command line, which you can control by editing corresponding 
configuration file under `/etc/default` inside of the container.

The only line you should be interested in starts with "JAVA_OPTIONS=" and may look like 
exemplified below:

```
JAVA_OPTIONS="-server -Xms768m -Xmx1536m -XX:MaxMetaspaceSize=256m -XX:+DisableExplicitGC -Dgluu.base=/etc/gluu -Dcatalina.base=/opt/gluu/jetty/idp"
```

The most easiest way to go about memory allocations is to designate a huge 
chunk of memory to Gluu Server when running setup.py script. Thus 6-8GB of 
physical RAM is a recommended volume for a production instance (with 5-7 of them dedicated to Gluu in setup.py).
In such case you may not need to tweak memory limits at all, 
default settings should be fine for all-purpose small/medium isntance, 
but in case of production instances under heavy load you may need to 
figure out the most optimal combination of JVM's native memory's proportions 
and garbage collectors assigned to different spaces inside it (most of that 
is beyond the scope of this document, though). An official Oracle's page on 
[ergonomics in Java](https://docs.oracle.com/javase/8/docs/technotes/guides/vm/gctuning/ergonomics.html) 8 could be a starting point for a search for the correct settings for your particular case.

By changing values of "-Xms" and "-Xms" parameters you can set starting 
and maximal size of the whole JVM's heap correspondingly. JVM will resize 
it during its run to better accomodate the application(s) in it, but never 
will go beyond those limits. If at some point it'll become unable to allocate 
space for a new object create by application, it will result in a re-known 
Java's Out Of Memory (OOM) error, which most likely will hamper its execution, or 
will result in its crash. You also may choose proportions in which the whole 
heap space will be devided between New and Old generation spaces, and different 
their sub-spaces with parameters "NewSize", "MaxNewSize" and "NewRatio". You can 
learn more about how to proprly devide heap between all the spaces [here](https://docs.oracle.com/javase/8/docs/technotes/guides/vm/gctuning/sizing.html)

In case any of those parameters are ommited, 
it will automatically calculate them taking into account properties of the environment 
it's launched in. Some estimations of what those default values could be can be 
received by running command like this in container: 
`# java -server -XX:+DisableExplicitGC -XX:+PrintFlagsFinal -version` 

Please note that due to significant changes in Java 8's architecture regarding how 
Metaspace (successor of PermGen of Java 7) is implemented, you must always 
set some reasonable limit for Metaspace with "-XX:MaxMetaspaceSize=" parameter. 
By default it's allowed to expand up untill free physical memory of the host will allow it, 
potentially bringing the whole system down as a result, in case some memory leakage 
to Metaspace exists.

## Monitoring JVM's garbage collection



## Choosing correct heap's size

This may be harder than it first appears. Larger not necessarily means better 
when it comes to garbage collection, especially when it comes to the size of 
the Old Generation space. Objects being propagated from New Generation space 
are consequently being allocated memory in OldGen until its filled up to current 
maximal limit. When this happens, a so called "Stop the World" 
event takes place and the JVM is paused till the end of the full GC phase 
(that may vary, depending on type of garbage collector assigned to OldGen; 
certain GCs are capable of doing collections in parallel to the main execution 
flow). The bigger the size of OldGen, the longer is the pause, which may 
affect user's experience, especially in interactive or real-time applications. 
At the same time, choosing too small size for it will result in much frequent 
collections, resulting in more overhead in terms of CPU's time, and may even 
result in Java's Out Of Memory errors in case maximal possible limit of heap 
size is already reached, but there is no space to allocate for a new object 
anyway.

A great tool which may help to visualize your JVM's heaps in real time is called 
[VisualVM](https://visualvm.github.io/) and its plugin "Visual GC" in particular. 
You can found a lot of guides on how to use it over internet. Let's concentrate on 
a more simplistic, yet powerfull tool called "jstat" instead.

Being a part of Java SDK and a console tool, jstat has everything you may need 
to quickly gauge state of different memory spaces within JVM in which your app runs 
on the fly.  Starting Gluu CE 3.1.0, it may no longer be present in container 
by default, so  you may need to acquire Java 8 SDK before you'll be able to use it.

You can follow next step to get GC stats for some of Gluu's JVMs:

1. Move into container: `# service gluu-server-3.1.2 login`
2. List all Java instances running at the moment: `su jetty -c '/path/to/java-8-sdk/bin/jps -ml'` First column contains ID of each JVM; you can guess which component it belongs to by checking pathes in its other parameters, or finding it by its ID in output of `ps -aux | grep -i java`
3. Connect to the chosen JVM to start gathering GC statistics with `# su jetty -c ''/path/to/java-8-sdk/bin/jstat -gccause -h20 JID 1000'`, where "JID" is numerical ID of JVM you've found out on previous step. You can use "-gccapacity" and "-gcmetacapacity" as well to get different perspectives. Parameters "-h20" and "1000" instruct jstat to print headers each 20 lines and dump a new line of stats each 1000 milliseconds, correspondingly.

Meaning of individual counters displayed by jstat can be found [here](https://docs.oracle.com/javase/8/docs/technotes/tools/unix/jstat.html). You may need to familiarize yoursefl with different garbage collectors types and strategies they employ, as well as general concepts of memory organization used by any Java implementation, and OpenJDK in particular (like heap, native memory, OldGen and NewGen spaces and Metaspace, Stop-the-World event etc)

## A quick hand-on example
