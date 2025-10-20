## Testing the Flask API with curl: Commands, Outputs, and Flags

Base URL: `http://127.0.0.1:5000`

### 1) Home

Command:
```bash
curl http://127.0.0.1:5000/
```

Output:
```
Welcome To The Sample To DO List App
```

---

### 2) Get all items

Command:
```bash
curl http://127.0.0.1:5000/items
```

Output:
```json
[
  {
    "description": "This is item 1",
    "id": 1,
    "name": "Item 1"
  },
  {
    "description": "This is item 2",
    "id": 2,
    "name": "Item 2"
  }
]
```

---

### 3) Get a single item (id = 1)

Command:
```bash
curl http://127.0.0.1:5000/items/1
```

Output:
```json
{
  "description": "This is item 1",
  "id": 1,
  "name": "Item 1"
}
```

---

### 4) Create a new item (POST)

Command:
```bash
curl -X POST http://127.0.0.1:5000/items \
  -H 'Content-Type: application/json' \
  -d '{"name":"Item 3","description":"This is item 3"}'
```

Output:
```json
{
  "description": "This is item 3",
  "id": 3,
  "name": "Item 3"
}
```

---

### 5) Update an existing item (PUT id = 1)

Command:
```bash
curl -X PUT http://127.0.0.1:5000/items/1 \
  -H 'Content-Type: application/json' \
  -d '{"name":"Updated Item 1","description":"Updated description"}'
```

Output:
```json
{
  "description": "Updated description",
  "id": 1,
  "name": "Updated Item 1"
}
```

---

### 6) Verify all items after update

Command:
```bash
curl http://127.0.0.1:5000/items
```

Output:
```json
[
  {
    "description": "Updated description",
    "id": 1,
    "name": "Updated Item 1"
  },
  {
    "description": "This is item 2",
    "id": 2,
    "name": "Item 2"
  },
  {
    "description": "This is item 3",
    "id": 3,
    "name": "Item 3"
  }
]
```

---

### 7) Delete an item (DELETE id = 1)

Command:
```bash
curl -X DELETE http://127.0.0.1:5000/items/1
```

Output:
```json
{
  "result": "Item deleted"
}
```

---

### 8) Verify remaining items after delete

Command:
```bash
curl http://127.0.0.1:5000/items
```

Output:
```json
[
  {
    "description": "This is item 2",
    "id": 2,
    "name": "Item 2"
  },
  {
    "description": "This is item 3",
    "id": 3,
    "name": "Item 3"
  }
]
```

---

## curl flags used (explained)

- **-X / --request**: Sets the HTTP method explicitly (e.g., `GET`, `POST`, `PUT`, `DELETE`). Often optional—`curl` infers `POST` when you provide `-d`.

- **-H / --header 'Content-Type: application/json'**: Adds an HTTP request header. `Content-Type` tells the server how to interpret the body. For JSON, use `application/json`.

- **-d / --data '{...}'**: Sends a request body. If `-X` is not specified, `curl` defaults to `POST` when `-d` is used. By default, `-d` URL-encodes data unless you specify a `Content-Type` of `application/json`, in which case the raw JSON string is sent.

Tips:
- Use line continuations (`\`) in Bash to split long commands across multiple lines (as shown above).
- For debugging, `-i` includes response headers, and `-v` prints verbose request/response info.
- To send a file as-is, use `--data-binary @file.json`.


