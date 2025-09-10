[Token refresh mechanism](#token-refresh-mechanism)

ENV File Parameters

Put it next to the src

```
# Base URL of the authentication service
BASE_URL = "https://auth-central-challange.vercel.app"

# Database stack to use for token storage: sqlite (development) | redis (production)
AUTH_DB_STACK = "sqlite"

# Redis configuration (used only if AUTH_DB_STACK = redis)
REDIS_HOST = ""
REDIS_PORT = 12345
REDIS_PASSWORD = ""
```

To Run

```
fastapi dev .\src\main.py
```

## App architecture description

### Infra Layer

In this layer, the application infrastructure is defined, such as:

- Fastapi config such as
  - middleware
  - tasks that should be run on startup or shutdown,
  - implement some states based on settings loaded from .env in main app to have access them throughout the entire project
- Application settings load from the `.env` file
  - load with pydantic_settings
- Services for interacting with external APIs
  - include interfaces and their implementation
- Errors related to this layer and other layers
  - include status code and message
- Database and its models (tables)
- Mixin classes

```
infra/
├── db/
│   ├── redis/
│   │   └── <files or directories...>
│   │
│   └── service/
│       └── <files or directories...>
│
├── exception/
│   └── <files...>
│
├── external_api/
│   ├── interface/
│   │   └── <files...>
│   │
│   └── service/
│       └── <files...>
│
├── fastapi_config/
│   └── <files...>
│
├── mixins/
│   └── <files...>
│
└── settings/
    └── <files...>
```

### Domain Layer

In this layer, data models are defined that are only used inside the application, meaning between layers, for transferring data.

```
domain/
└── schemas/
    ├── <schema_group_name>/
    │   └── <files...>
    │
    ├── <schema_group_name>/
    │   └── <files...>
    │
    └── <schema_group_name>/
        └── <files...>
```

### Models Layer

In this layer, data models are defined that are only used for receiving or sending data to the client.

```
models/
└── schemas/
    ├── <schema_group_name>/
    │   └── <files...>
    │
    ├── <schema_group_name>/
    │   └── <files...>
    │
    └── <schema_group_name>/
        └── <files...>
```

### Repo Layer

In this layer, communication with the database is handled.
Repository classes are defined here, whose methods provide interaction with the database.
Each repository class inherits from an interface defined in this layer.
Interfaces define the structure of database communication, so we can have multiple repository classes based on a single interface and use them for dependency injection.

```
repo/
├── interface/
│   └── <files...>
└── <implementation_name>/
    └── <files...>
```

Naming implementations can be based on:

- **Storage type** — for example: `sql`, `nosql`

```
repo/
├── interface/
│   └── <files...>
├── sql/
│   └── <files...>
└── nosql/
    └── <files...>
```

- **Storage name** — for example: `postgresql`, or `mongodb`.

```
repo/
├── interface/
│   └── <files...>
├── postgresql/
│   └── <files...>
└── mongodb/
    └── <files...>
```

### Routes Layer

In this layer, endpoints are defined along with their dependencies, response statuses, and other endpoint-related configurations.

```
routes/
├── api_endpoints/
│   ├── <endpoint_group_name>/
│   │   └── <files...>
│   │
│   ├── <endpoint_group_name>/
│   │   └── <files...>
│   │
│   └── main_router.py
│
├── depends/
│   └── <files...>
│
└── http_response/
    └── <files...>
```

### Usecase Layer

In this layer, the application’s business logic is defined.
This layer acts as an important bridge between endpoints in the Routes layer, the database in the Repo layer, and external APIs in the Infra layer.

One of the implementen logics is the token refresh mechanism.

```
usecase/
├── <usecase_group_name>/
│   └── <files...>
│
├── <usecase_group_name>/
│   └── <files...>
│
└── <usecase_group_name>/
    └── <files...>
```

#### Note

The layers are not limited to the mentioned items and can also include other related configurations.

## Token Refresh Mechanism

After user registration, when logging in, the **access token**, **refresh token**, and **token type** are received from the auth server.
These information, along with the user’s email and the `calculated expiration time` of the **access token** and **refresh token**, are stored in the database.

When saving this information in the database, a **UUID** is generated as the access identifier and stored with the information in database as `device_id`.

The email is stored to let us delete all auth records at once if the user changes it later.
The device_id is stored to allow multi-device login, manage tokens per device, show the list of logged-in devices, let the user log out from any device, and notify them of new logins to handle unauthorized access if needed.

In **Redis**, the `device_id` is used as the `name`, and the other details are stored as key–value pairs.

**Example (Redis schema):**

```
UUID: <uuid>
  │
  ├── email: 'sample@gmail.com'
  │
  ├── token_type: 'bearer'
  │
  ├── access_token: 'eyJhbGciOiJI...'
  │
  ├── access_expiry: 2025-09-06 19:01:45.165131+00:00
  │
  ├── refresh_token: 'eyJhbGciOiJI...'
  │
  └── refresh_expiry: 2025-09-06 19:03:45.165131+00:00
```

In the **SQL database**, the `device_id` is stored along with the rest of the information.

**Example (SQL schema):**

```
| id | device_id (UUID)                 | email            | access_token    | access_expiry                    | refresh_token   | refresh_expiry                   | token_type |
|  1 | e8fbab2370f64befb83f2ec62ffc6055 | sample@gmail.com | eyJhbGciOiJI... | 2025-09-06 19:01:45.165131+00:00 | eyJhbGciOiJI... | 2025-09-06 19:03:45.165131+00:00 | bearer     |
```

Immediately after saving the information in the database, the `device_id` is stored in the user’s cookies as a **session-type cookie**.

---

### Authentication Flow

For every process that requires user authentication:

1. Get the `device_id` from the cookie.
2. Use it to fetch the information from the database.
3. Check the **access token expiration date**:

   - If the access token is still valid → the user request is continues using the access token.

   - If the access token is invalid → check the **refresh token expiration date**.

     - If the refresh token is expired → stop the request here, return an error message, or redirect the user to the login page.

     - If the refresh token is valid → send it to `auth-server/refresh-token` endpoint, get new **access** and **refresh** tokens, update the database using the `device_id`, and continue the user’s request with the new access token.

---

### Optimization

To optimize further, we can set an **expiry time for records in Redis**,it can be equal to the lifetime of the refresh token.
After the time has passed (or the refresh token has expired), the record will automatically be removed, and the user will need to log in again.
When the tokens expire, its database record will no longer have any use.
