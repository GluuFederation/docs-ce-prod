# Design Goals

## Free Open Source Identity Suite

One of the things that has made access management difficult for
organizations is that there is no one tool you can deploy to solve even
average requirements. The Gluu Server provides a recipe to deploy a
combination of the best free open source tools, working together.

## Support most promising open standards

The goal of the Gluu Server is to support the minimum number of
standards necessary to authenticate people, and to authorize them to
access the resources they need to do business for the domain. The Gluu
Server should be practical about supporting older protocols, but always
strive to be the first implementer of the most promising new protocols.

## Leverage existing business processes

Where possible, the Gluu Server goes to work with a minimal amount 
of changes to existing business processes. Don't "rip and replace",
but for new applications, use new protocols wherever possible to 
avoid the creation of future upgrade work.

## Free license

The components of the Gluu Server should be free to use in production.
This license strategy will produce the best software at the lowest 
total cost of ownership for the organization.

## Write as a last resort 

Use the best software that exists. If something the Gluu Server needs
doesn't exist, it may become an OX project. If some group comes along and
writes software better than an existing OX component, use it!

## Not just comprehensive, but easy to use

The Gluu Server should make it easy for domain system administrators
to control access to Web and network resources. Usability is more
important than features.

## Horizontal scalability

System administrators should be able to add more servers to make the 
Gluu Server scale as much as needed.

## Extreme flexibility

As Kent Beck says, "Embrace Change". The key to the Gluu Server's success
has been its ability to handle all sorts of crazy requirements--quickly.
Sometimes raw speed is needed, but equally important is the ability for
the access management framework to be really smart.

