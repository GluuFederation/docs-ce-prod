# OXD
oxd is a mediator, a service demon that listens on localhost, providing easy APIs that 
can be called by a web application to simplify using an external OAuth2 server for 
authentication or authorization. oxd is not a proxy--sometimes it makes API calls 
on behalf of an application, but other times it just forms the right URLs and returns them to the application. 

One significant advantage of using oxd over a native client library is that oxd 
consolidates the OAuth2 code in one package. If there are updates to the OAuth2 client 
code, you can update the oxd-server package, without changing the interface to the application.

## Documentation
The complete documentation for oxd is made available in a separate address. 
Please see [this link](https://gluu.org/docs-oxd/) for the OXD documentation.
