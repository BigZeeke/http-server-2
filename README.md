# HTTP Server 2

You'll modify a low-level Python HTTP server that's *almost* working but has a bug — and then extend it with a new endpoint.

> If you just came from [HTTP Server 1](https://github.com/CP-Evenings-and-Weekends/http-server-1), this `server.py` should look familiar: it's roughly what you built up to.  The `Request.parse_request` method is left as a stub for you to implement.

## Requirements

### 1. Find and fix the bug

Run the server:

```
$ python server.py
waiting for a request on localhost:9292
```

…then make a request from another terminal:

```
$ curl http://localhost:9292/
```

You'll get an error.  Trace it: which line crashed?  Why?  Use print statements or breakpoints to inspect the state.  (Hint: look at what `Request.parse_request` does today vs. what `server.py` expects `parsed_request` to look like.)

Fix it so that `Request.parse_request` populates `self.parsed_request` as a dict with at least a `"uri"` key:

```python
{"uri": "/", "method": "GET", ...}
```

Once that's done, `curl http://localhost:9292/` should return your "Hello World" HTML response.

### 2. Add a `/time` endpoint that returns JSON

Extend `server.py` so that `GET /time` responds with JSON (not HTML) like:

```json
{
  "current_time": "2026-07-21 21:07:51.809581"
}
```

The response needs to:
- Use `Content-Type: application/json` (not `text/html`)
- Include a correct `Content-Length`
- Use `json.dumps(...)` to serialize the body — `datetime` and `json` are already imported

The existing HTML handler (`build_html_response`) is a good template — build a similar `build_json_response` function.

### 3. Manually test both endpoints

- `curl http://localhost:9292/` should show the Hello World HTML
- `curl -v http://localhost:9292/time` should show JSON, plus `Content-Type: application/json` in the response headers

## Things to think about
- The starter server uses port **9292**.  The day-2 lesson used **9295**.  What would change if you swapped ports?  What happens if you try to bind to a port already in use?
- The existing HTML response uses `build_html_response` which includes `Content-Length`.  The lesson's example response doesn't.  What happens if you omit `Content-Length` — does the client still work?  How?
- What should `/time` do if the client sends a `POST` instead of a `GET`?  Right now the server ignores method entirely.

## Stretch
- Reject unknown URIs with a proper `404 Not Found` response.
- Add a `/users` endpoint that returns a CSV's contents as JSON (mirroring the lesson example).
- Read the HTTP method from the request and only accept `GET` for these endpoints — respond `405 Method Not Allowed` otherwise.
- Add a `Response` class so the body of the loop becomes `client_connection.send(response.encode())` regardless of endpoint.

> Stuck? Have a code error? Use the ["4 Before Me"](https://docs.google.com/document/d/1nseOs5oabYBKNHfwJZNAR7GlU0zkZxNagsw63AD7XV0/edit) debugging checklist to help you solve it!
