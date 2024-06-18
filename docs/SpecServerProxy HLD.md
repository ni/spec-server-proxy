# NI SpecServerProxy

- [NI SpecServerProxy](#ni-specserverproxy)
  - [Who](#who)
  - [Problem Statement](#problem-statement)
  - [Proposed Solution](#proposed-solution)
  - [Implementation / Design](#implementation--design)
    - [Dataflow](#dataflow)
  - [Installation](#installation)
  - [Establishment of connection with SLE](#establishment-of-connection-with-sle)

## Who

Author: National Instruments <br/>
Team: ModernLab Success

## Problem Statement
 
Currently there is no workflow to exchange data between SystemLink Enterprise (SLE) and NI TestStand.

## Proposed Solution

NI TestStand has a feature to exchange data between itself and Specification Compliance Manager using SCM APIs

Python server to act as a proxy which redirects the requests sent to SCM server to SLE server without affecting the TestStand-SpecificationComplianceManager (SCM) workflow.


## Implementation / Design

- Flask server to act as a proxy which redirects requests sent to SCM server to SLE server.
- Server uses SystemLink Python Clients to access SLE APIs.
- Endpoints to enable
  - Get products from SLE server.
  - Get available specs in a product in SLE server.
  - Upload measurement BDC file to a product in SLE server.

### Dataflow

The below picture shows data flow between SystemLink Enterprise and TestStand
Image[Link]

## Installation

- NI SpecServerProxy Python Package has to be installed in NI SystemLink Client's Python Site Packages.
- Follow the steps to set up [NI SystemLink Client](https://www.ni.com/docs/en-US/bundle/systemlink-enterprise/page/setting-up-systemlink-client.html#:~:text=Search%20for%20and%20install%20NI,which%20you%20want%20to%20connect)
- Run `"C:\Program Files\National Instruments\Shared\Skyline\Python\3.8\python.exe" -m pip install ni_spec_server_proxy-X_X_X-py3-none-any.whl` to install whl file.

## Establishment of connection with SLE

- Launch NI SystemLink Client and connect to SystemLink Enterprise as per [instructions](https://www.ni.com/docs/en-US/bundle/systemlink-enterprise/page/setting-up-systemlink-client.html)
  - If the SLE version is 2024-04 or older, update the API key in the master.json file at - "C:\ProgramData\National Instruments\Skyline\HttpConfigurations\http_master.json".
  - Refer to the [instructions to create an API key](https://www.ni.com/docs/en-US/bundle/systemlink-enterprise/page/creating-an-api-key.html)
- Run spec-server-proxy.bat file to run the server.
- Open NI TestStand Sequence Editor.
- Select *Tools > Import/Update from Specification Compliance Manager (SCM)* from the TestStand Sequence Editor menu bar.[Image]()
- Enter the credentials in the dialog box,
  - Server - http://localhost:8000
  - API token - None
  [Image]
- On Clicking on the *Connect* button, it should be connected to Proxy Server.

