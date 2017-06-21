# Angular

## Overview
The following documentation demonstrates how to use Gluu's [OpenID Connect JavaScript implicit client](https://github.com/GluuFederation/openid-implicit-client) to send users from an single page Angular app to the Gluu Server for authentication and authorization. 

> Note: The code used for this client was forked from a JavaScript library written by Edmund Jay.

## What is the JavaScript Implicit Client?
This JavaScript client implements the [OpenID Connect implicit flow](http://openid.net/specs/openid-connect-core-1_0.html#ImplicitFlowAuth). The Implicit Flow is mainly used by Clients implemented in a browser using a scripting language. The Access Token and ID Token are returned directly to the Client, which may expose them to the End-User and applications that have access to the End-User's User Agent. The Authorization Server does not perform Client Authentication. 

The OpenID Connect Implicit Flow follows the following steps:

- Client prepares an Authentication Request containing the desired request parameters.
- Client sends the request to the Authorization Server.
- Authorization Server Authenticates the End-User.
- Authorization Server obtains End-User Consent/Authorization.
- Authorization Server sends the End-User back to the Client with an ID Token and, if requested, an Access Token.
- Client validates the ID token and retrieves the End-User's Subject Identifier.

## Installation

To use this library, include the openidconnect.js your HTML page.

- Set the provider and client configuration info through JSON objects;
- Call the server – login;
- In the callback page, callback.html, you will get ID Token back, so that you can put it into the cookie to handle the session.

## Configuration 


