The Gluu Server supports the following standard OAuth 2.0 and UMA Authorization Server (AS) and OpenID Connect Provider (OP) endpoints:

Endpoint	Purpose

Server discovery: Discover the OAuth 2.0 / OpenID Connect endpoints, capabilities, supported cryptographic algoritms and features.

Server JWK set: Retrieve the public server JSON Web Key (JWK) required to verify the authenticity of issued ID and access tokens.

Client registration	Create, access, update and delete client registrations with the server.

Authorisation	The client sends the end-user's browser to this endpoint to request their authentication and consent. This endpoint is used in the code and implicit OAuth 2.0 flows which require end-user interaction.

Token	Post an OAuth 2.0 grant (code, refresh token, resource owner password credentials, client credentials) to obtain an ID and / or access token.

Token introspection	Validate an access token and retrieve its underlying authorisation (for resource servers).

Token revocation	Revoke an obtained access or refresh token.

UserInfo	Retrieve profile information and other attributes for a logged-in end-user.

Check session iframe	Poll the OpenID provider for changes of end-user authentication status.

Logout (end-session)	Sign out an end-user.
