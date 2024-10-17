# NI Spec Server Proxy

- [NI Spec Server Proxy](#ni-spec-server-proxy)
  - [Introduction](#introduction)
  - [Dependencies](#dependencies)
  - [Example using NI TestStand](#example-using-ni-teststand)
    - [Installation of whl File](#installation-of-whl-file)
    - [NI TestStand](#ni-teststand)

## Introduction

- NI Spec Server Proxy is a python server used for accessing SLE products and specifications using SLE APIs.

## Dependencies

- Python 3.8 - From [SystemLink Client](https://www.ni.com/en/support/downloads/software-products/download.systemlink-client.html#521644)
- [aiohttp = "^3.10.9"](https://pypi.org/project/aiohttp/)
- [yarl = "1.13.0"](https://pypi.org/project/yarl/1.13.0/)
- [flask = "^3.0.3"](https://pypi.org/project/Flask-Async/)
- [nisystemlink-clients = "^1.3.0"](https://pypi.org/project/nisystemlink-clients/)
- systemlink-sdk = "^24.0.0" From [SystemLink Client](https://www.ni.com/en/support/downloads/software-products/download.systemlink-client.html#521644)
- [pyyaml = "^6.0.0"](https://pypi.org/project/PyYAML/)
- [pandas = "^2.0.0"](https://pypi.org/project/pandas/)

## Example using NI TestStand

### Installation of whl File

- Run `"C:\Program Files\National Instruments\Shared\Skyline\Python\3.8\python.exe" -m pip install ni_spec_server_proxy-X_X_X-py3-none-any.whl` to install whl file.
- Run `"C:\Program Files\National Instruments\Shared\Skyline\Python\3.8\python.exe" -m ni_spec_server_proxy` to run server.

### NI TestStand

- Open NI TestStand.
- Click `Tools`.
- Click `Import/Update from Specification Compliance Manager (SCM)`.
- In the opened dialog box, enter Server URL as `http://localhost:50000/`.
- No API key is required.
- Click `Connect` to connect to NI Spec Server Proxy. Ensure the NI Spec Server Proxy server is running before connecting.
