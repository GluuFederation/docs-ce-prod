# UMA 2 Scope Expressions

UMA 2 Scope expressions is Gluu invented extension of UMA 2 which gives flexible way to combine scopes and thus propose more robust way to grant access.

## Register resource with scope_expression

RS registers resource (note new `scope_expression` field, `resource_scopes` is ignored in this case)

```json
{  
   "resource_scopes":[],
   "description":"Collection of digital photographs",
   "icon_uri":"http://www.example.com/icons/flower.png",
   "name":"Photo Album",
   "type":"http://www.example.com/rsrcs/photoalbum",
   "scope_expression": {
      "rule": {
         "and": [
            {
               "or": [
                   {"var": 0},
                   {"var": 1}
               ]
            },
            {"var": 2}
         ]
      },
      "data": [
         "http://photoz.example.com/dev/actions/all",
         "http://photoz.example.com/dev/actions/add",
         "http://photoz.example.com/dev/actions/internalClient"
      ]
   }
}

```

## Ticket registration

RS registers tickets with all scopes mentioned in "data" (we need all scopes in order to evaluate expression, all or nothing principle)

```json

{  
   "resource_id":"112210f47de98100",
   "resource_scopes":[  
       "http://photoz.example.com/dev/actions/all",
       "http://photoz.example.com/dev/actions/add",
       "http://photoz.example.com/dev/actions/internalClient"
   ]
}
```

## Evaluation

UMA Engine iterates over each scope and fetch ALL policies for each scope. Evaluates all policies.
a) not enough claims - return need_info error
b) enough claims - evaluate results from ALL policies with "AND" rule for ONE given scope.
   b1) `http://photoz.example.com/dev/actions/all` -  `policyA AND policyB` => false
   b2) `http://photoz.example.com/dev/actions/add` -  `policyA AND policyD` => true
   b3) `http://photoz.example.com/dev/actions/internalClient` - `policyD AND policyE and policyK` => true

Results in expression : `(false OR true) AND true` => `true`

Below is example of including all scopes except `http://photoz.example.com/dev/actions/all` scope (because for this part of expression `false` is returned). 

```json
{  
   "active":true,
   "exp":1256953732,
   "iat":1256912345,
   "permissions":[  
      {  
         "resource_id":"112210f47de98100",
         "resource_scopes":[  
            "http://photoz.example.com/dev/actions/add",
            "http://photoz.example.com/dev/actions/internalClient"
         ],
         "exp":1256953732
      }
   ]
}
```