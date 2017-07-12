# Python Flask

## Overview
The following documentation demonstrates how to use Gluu's OAuth 2.0 client software, [oxd](http://oxd.gluu.org), 
to send users from a Python Flask web app to the Gluu Server for authentication and authorization. 

## What is oxd?
oxd is a middleware service that provides API's that can be called by a web application that are easier than directly calling the API's of an OpenID Connect Provider (OP) or an UMA Authorization Server (AS). oxd is designed to work as a standalone service demon. It's a web server, running in an embedded Jetty server. Just start it and stop it like you would any other unix service.

By default, oxd is restricted to localhost, which means these APIs cannot be reached from another server on the network--only by services running the server locally. oxd should be deployed on each server that has web applications.

## Installation

Install the oxd server using the following instructions: [installation instructions](https://gluu.org/docs/oxd/install/). 

Note: In order to run oxd, you will need a valid license which can be acquired on the [oxd website](https://oxd.gluu.org). Signing up for a license is free, and even includes a $50 credit towards your first 60 days of use.

## Configuration 

Configure oxd using the following instructions: [configuration instructions](https://gluu.org/docs/oxd/conf/)

Note: You will need your license information to properly configure oxd. 
