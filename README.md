# NI Spec Server Proxy

- [NI Spec Server Proxy](#ni-spec-server-proxy)
  - [Introduction](#introduction)
  - [Dependencies](#dependencies)
  - [Example using NI TestStand](#example-using-ni-teststand)
    - [Installing Python package using wheel file](#installing-python-package-using-wheel-file)
    - [NI TestStand](#ni-teststand)

## Introduction

- NI Spec Server Proxy is a Python server that extracts product specifications and uploads measurement data to SystemLink Enterprise(SLE) using the NI Specification Compliance Manager(SCM) Server's APIs. This enables user applications built for the NI SCM Server to work with SLE without application-side changes.

## Dependencies

- Python 3.8.5
- systemlink-sdk = "^24.0.0"

The above dependencies are satisfied by installing [SystemLink Client](https://www.ni.com/en/support/downloads/software-products/download.systemlink-client.html) with `Python SDK` option checked.

## Example using NI TestStand

### Installing Python package using wheel file

- Run `"C:\Program Files\National Instruments\Shared\Skyline\Python\3.8\python.exe" -m pip install ni_spec_server_proxy-X_X_X-py3-none-any.whl` to install whl file.
- Run `"C:\Program Files\National Instruments\Shared\Skyline\Python\3.8\python.exe" -m ni_spec_server_proxy` to run server.

### NI TestStand

- Launch NI TestStand Sequence Editor.
- Click `Tools`.
- Click `Import/Update from Specification Compliance Manager (SCM)`.
- In the opened dialog box, enter Server URL as `http://localhost:50000/`.
- No API key is required.
- Click `Connect` to connect to NI Spec Server Proxy. Ensure the NI Spec Server Proxy server is running before connecting.
