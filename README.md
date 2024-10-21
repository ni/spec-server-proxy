# NI Spec Server Proxy

- [NI Spec Server Proxy](#ni-spec-server-proxy)
  - [Introduction](#introduction)
  - [Dependencies](#dependencies)
  - [Example using NI TestStand](#example-using-ni-teststand)
    - [Installing Python package using wheel file](#installing-python-package-using-wheel-file)
    - [NI TestStand](#ni-teststand)

## Introduction

- NI Spec Server Proxy is a Python server used for accessing SLE products and specifications using SLE APIs.

## Dependencies

- Python 3.8 - From [SystemLink Client](https://www.ni.com/en/support/downloads/software-products/download.systemlink-client.html#521644)
- systemlink-sdk = "^24.0.0" From [SystemLink Client](https://www.ni.com/en/support/downloads/software-products/download.systemlink-client.html#521644)

## Example using NI TestStand

### Installing Python package using wheel file

- Run `"C:\Program Files\National Instruments\Shared\Skyline\Python\3.8\python.exe" -m pip install ni_spec_server_proxy-X_X_X-py3-none-any.whl` to install whl file.
- Run `"C:\Program Files\National Instruments\Shared\Skyline\Python\3.8\python.exe" -m ni_spec_server_proxy` to run server.

### NI TestStand

- Open NI TestStand.
- Click `Tools`.
- Click `Import/Update from Specification Compliance Manager (SCM)`.
- In the opened dialog box, enter Server URL as `http://localhost:50000/`.
- No API key is required.
- Click `Connect` to connect to NI Spec Server Proxy. Ensure the NI Spec Server Proxy server is running before connecting.
