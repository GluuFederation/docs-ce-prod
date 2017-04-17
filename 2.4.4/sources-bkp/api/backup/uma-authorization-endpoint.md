# API Document

### /requester/perm

#### Overview


#### `/requester/perm`
##### requestRptPermissionAuthorization
**POST** `/requester/perm`

Client Requests Authorization Data
Once in possession of a permission ticket and an AAT for this
authorization server, the client asks the authorization server to give
it authorization data corresponding to that permission ticket. It
performs a POST on the RPT endpoint, supplying its own AAT in the header
and a JSON object in the body with a "ticket" property containing the
ticket as its value.

If the client had included an RPT in its failed access attempt, It MAY
also provide that RPT in an "rpt" property in its request to the
authorization server.

In circumstances where the client needs to provide requesting party
claims to the authorization server, it MAY also include a "claim_tokens"
property in its request; see Section 3.4.1.2.1 for more information. The
authorization server uses the ticket to look up the details of the
previously registered requested permission, maps the requested
permission to operative resource owner policies based on the resource
set identifier and scopes associated with it, potentially requests
additional information, and ultimately responds positively or negatively
to the request for authorization data.

The authorization server bases the issuing of authorization data on
resource owner policies. These policies thus amount to an asynchronous
OAuth authorization grant. The authorization server is also free to
enable the resource owner to set policies that require the owner to
interact with the server in near-real time to provide consent subsequent
to an access attempt. All such processes are outside the scope of this
specification.

###### URL
    http://gluu.org/requester/perm

###### Parameters
- body

    <table border="1">
        <tr>
            <th>Parameter</th>
            <th>Required</th>
            <th>Description</th>
            <th>Data Type</th>
        </tr>
        <tr>
            <th>body</th>
            <td>false</td>
            <td></td>
            <td><a href="#RptAuthorizationRequest">RptAuthorizationRequest</a></td>
        </tr>
    </table>
- header

    <table border="1">
        <tr>
            <th>Parameter</th>
            <th>Required</th>
            <th>Description</th>
            <th>Data Type</th>
        </tr>
        <tr>
            <th>Authorization</th>
            <td>false</td>
            <td></td>
            <td>string</td>
        </tr>
        <tr>
            <th>Host</th>
            <td>false</td>
            <td></td>
            <td>string</td>
        </tr>
    </table>

###### Response
[](#)


###### Errors
<table border="1">
    <tr>
        <th>Status Code</th>
        <th>Reason</th>
    </tr>
        <tr>
            <td>403</td>
            <td>Forbidden. Example of a &quot;need_info&quot; response with a full set of &quot;error_details&quot; hints:&#10;&#10;HTTP/1.1 403 Forbidden&#10;Content-Type: application/json&#10;Cache-Control: no-store&#10;...&#10;&#10;{&#10; &quot;error&quot;: &quot;need_info&quot;,&#10; &quot;error_details&quot;: {&#10;   &quot;authentication_context&quot;: {&#10;     &quot;required_acr&quot;: [&quot;https://example.com/acrs/LOA3.14159&quot;]&#10;   },&#10;   &quot;requesting_party_claims&quot;: {&#10;     &quot;required_claims&quot;: [&#10;       {&#10;         &quot;name&quot;: &quot;email23423453ou453&quot;,&#10;         &quot;friendly_name&quot;: &quot;email&quot;,&#10;         &quot;claim_type&quot;: &quot;urn:oid:0.9.2342.19200300.100.1.3&quot;,&#10;         &quot;claim_token_format&quot;: &#10;[&quot;http://openid.net/specs/openid-connect-core-1_0.html#HybridIDToken&quot;],&#10;         &quot;issuer&quot;: [&quot;https://example.com/idp&quot;]&#10;       }&#10;     ],&#10;     &quot;redirect_user&quot;: true,&#10;     &quot;ticket&quot;: &quot;016f84e8-f9b9-11e0-bd6f-0021cc6004de&quot;&#10;   }&#10; }&#10;}&#10;</td>
        </tr>
        <tr>
            <td>401</td>
            <td>Unauthorized</td>
        </tr>
        <tr>
            <td>400</td>
            <td>Bad request</td>
        </tr>
</table>


- - -

## Data Types


## <a name="ClaimTokenList">ClaimTokenList</a>

<table border="1">
    <tr>
        <th>type</th>
        <th>required</th>
        <th>access</th>
        <th>description</th>
        <th>notes</th>
    </tr>
    <tr>
        <td>boolean</td>
        <td>optional</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>int</td>
        <td>optional</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
</table>

## <a name="RptAuthorizationRequest">RptAuthorizationRequest</a>

<table border="1">
    <tr>
        <th>type</th>
        <th>required</th>
        <th>access</th>
        <th>description</th>
        <th>notes</th>
    </tr>
    <tr>
        <td><a href="#ClaimTokenList">ClaimTokenList</a></td>
        <td>optional</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>optional</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>optional</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
</table>

