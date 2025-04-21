# Ancient Calendar

The **Ancient Calendar** is a RESTful service that exposes information based
on the ancient Egyptian civil calendar, which is one of the oldest
chronological systems in human history. This API computes the current Egyptian
year starting from the historical epoch of 19 July 4236 BCE — the traditional
date marking the start of the Ancient Calendar. It provides valuable information
for educational, cultural, astronomical, and symbolic purposes, as well as for
integration into creative digital projects.

![Ancient Calendar Logo](doc/logo.jpg)

## Overview

The Ancient Calendar API is a modern implementation of the ancient Egyptian
civil calendar. It calculates the current Egyptian year starting from 19 July
4236 BCE, the traditional epoch of the calendar. This API is designed for
educational, cultural, and astronomical purposes, as well as for integration
into creative projects.

The calendar consists of 365 days divided into 12 months of 30 days each, plus
5 additional days known as "epagomenal days." The API provides accurate
calculations adjusted for timezones, making it accessible to users worldwide.

## Deployment

### Docker Image

The [`demsking/ancient-calendar`](https://hub.docker.com/r/demsking/ancient-calendar)
Docker image is officially available on Docker Hub, supporting both
`linux/amd64` and `linux/arm64` platforms. The image is configured to expose
port `4241`, which serves the API and documentation endpoints.

The local documentation can be accessed at `http://localhost:4241/docs` for easy
reference on available endpoints and usage instructions.

### Deploy with Docker

Use the official Docker image [`demsking/ancient-calendar`](https://hub.docker.com/r/demsking/ancient-calendar)
to run Ancient Calendar:

```sh
docker run -d --env-file <path_to_env_file> -p 4241:4241 demsking/ancient-calendar
```

Replace `<path_to_env_file>` with the path to your
[environment variables](#description/environment-variables) file containing the
necessary configurations.

### Deploy with Docker Compose

Create a `compose.yml` file:

```yaml
services:
  calendar:
    image: demsking/ancient-calendar
    ports:
      - 4241:4241
```

Run the container using `docker compose`:

```sh
docker compose up -d
```

## Environment Variables

When configuring **Ancient Calendar**, several environment variables are used to
control its behavior and connect with external services. Below is a breakdown
of these variables, grouped by their purpose.

### HTTP Configuration

- **HOST**: The host address on which the application will listen. Default is `"127.0.0.1"`.
- **PORT**: The port number on which the application will listen. Default is `4241`.

### API and Logging Configuration

These variables control the API root path, logging behavior, and server settings.

- **ROOT_PATH**:
  Defines the base URL path for all API routes. Defaults to `'/'`.

- **LOG_FILE**:
  Path to the log file for storing application logs. Empty defaults to console.

- **LOG_LEVEL**:
  Controls the verbosity of logs. Options: `'DEBUG'`, `'INFO'`, `'WARNING'`,
  `'ERROR'`, `'CRITICAL'`. Defaults to `'INFO'`.

### Performance Configuration

Settings that control the server's performance.

- **WORKERS**:
  The number of worker processes for handling requests. Defaults to the
  number of CPU cores on the system.

### Timezone Configuration

- **TIMEZONE**:
  The IANA timezone identifier used for all datetime operations. Common values include
  `'UTC'`, `'Africa/Cairo'`, or `'Europe/Paris'`. Defaults to `'UTC'`.
