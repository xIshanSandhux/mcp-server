# LeetCode GraphQL API

Status: Draft

## Overview

LeetCode uses an internal GraphQL endpoint for much of the data used by its website:

```text
https://leetcode.com/graphql/
```

LeetCode does not provide a documented public developer API, so this endpoint should be treated as an unstable implementation detail. Keep all LeetCode-specific request code inside `leetcode_client.py`.

## GraphQL request shape

GraphQL requests are sent as HTTP `POST` requests with a JSON body:

```json
{
  "operationName": "operationName",
  "variables": {},
  "query": "query operationName { ... }"
}
```

The response generally contains `data`, `errors`, or both:

```json
{
  "data": {
    "example": {}
  },
  "errors": []
}
```

The client must check both the HTTP status and the GraphQL `errors` field. An HTTP 200 response does not guarantee that the query succeeded.

## Authentication

Public queries may work without login. Account-specific queries generally require the browser session cookies:

```text
LEETCODE_SESSION
csrftoken
```

Authenticated requests commonly include:

```http
Cookie: LEETCODE_SESSION=<session>; csrftoken=<csrf>
X-CSRFToken: <csrf>
Referer: https://leetcode.com/
Origin: https://leetcode.com
Content-Type: application/json
```

`LEETCODE_SESSION` authenticates the account. `csrftoken` helps protect state-changing requests from CSRF attacks. The CSRF cookie value and `X-CSRFToken` header value should match.

The `Referer` header tells LeetCode which page initiated the request. Postman and command-line clients may need this header added explicitly. A missing or invalid `Referer` can result in an HTML `403 Forbidden` response before GraphQL processes a request.

## Basic testing

Start with a read-only request:

```bash
curl -sS https://leetcode.com/graphql/ \
  -H 'Content-Type: application/json' \
  -H 'Referer: https://leetcode.com/' \
  --data '{"operationName":"example","variables":{},"query":"query example { ... }"}'
```

In Postman:

1. Create a `POST` request to `https://leetcode.com/graphql/`.
2. Use **Body → GraphQL** or **Body → raw → JSON**.
3. Add `Content-Type: application/json`.
4. Add `Referer: https://leetcode.com/` if the request receives a 403.
5. For authenticated queries, add the cookies and `X-CSRFToken` header.

If a request works with cURL but fails in Postman, import the working cURL into Postman. This preserves the URL, body, cookies, and headers. A browser request can also be inspected through Developer Tools → Network → Copy as cURL.

## Query documentation

Query definitions will be added here as the client is implemented.


## Client boundary

The application should hide raw GraphQL details behind a small client interface:

```text
graphql_request(query, variables, operation_name)
get_problem(...)
get_progress(...)
get_submissions(...)
```

The MCP layer should expose specific application operations rather than an arbitrary generic GraphQL tool.

## Security

- Treat `LEETCODE_SESSION` as a password.
- Never commit cookies or tokens.
- Never log authentication headers.
- Do not send authenticated requests through third-party proxies.
- Keep Postman environments local and private.
- Do not include credentials in copied cURL examples or documentation.

