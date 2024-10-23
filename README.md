# NI Spec Server Proxy

- [NI Spec Server Proxy](#ni-spec-server-proxy)
  - [Introduction](#introduction)
  - [Dependencies](#dependencies)
  - [Installing Python package using wheel file](#installing-python-package-using-wheel-file)
  - [How to run?](#how-to-run)
  - [How to communicate TestStand with SLE?](#how-to-communicate-teststand-with-sle)
    - [SystemLink Client](#systemlink-client)
    - [NI TestStand](#ni-teststand)
    - [How to start the proxy on windows startup automatically?](#how-to-start-the-proxy-on-windows-startup-automatically)
      - [Note](#note)

## Introduction

- NI Spec Server Proxy is a Python server that extracts product specifications and uploads measurement data to SystemLink Enterprise(SLE) using the NI Specification Compliance Manager(SCM) Server's APIs. This enables user applications built for the NI SCM Server to work with SLE without application-side changes.

## Dependencies

- Python 3.8.5
- systemlink-sdk = "^24.0.0"

The above dependencies are satisfied by installing [SystemLink Client](https://www.ni.com/en/support/downloads/software-products/download.systemlink-client.html) with `Python SDK` option checked.

## Installing Python package using wheel file

- Open Command Prompt.
- Run `"C:\Program Files\National Instruments\Shared\Skyline\Python\3.8\python.exe" -m pip install ni_spec_server_proxy-X_X_X-py3-none-any.whl` to install whl file.

## How to run?

- Run [spec-server-proxy.bat](batch_files/spec-server-proxy.bat) to run server.
(OR)
- Open Command Prompt.
- Run `"C:\Program Files\National Instruments\Shared\Skyline\Python\3.8\python.exe" -m ni_spec_server_proxy` to run server.

## How to communicate TestStand with SLE?

Run the NI Spec Server Proxy after setting up [SystemLink Client](#systemlink-client). Refer to [How to run?](#how-to-run)

### SystemLink Client

- Launch NI SystemLink Client and connect to SystemLink Enterprise as per [instruction](https://www.ni.com/docs/en-US/bundle/systemlink-enterprise/page/setting-up-systemlink-client.html#:~:text=Search%20for%20and%20install%20NI,which%20you%20want%20to%20connect.)
  - If the SystemLink Enterprise(SLE) version is 2024-04 or older, update the API key in the master.json file at - *"C:\ProgramData\National Instruments\Skyline\HttpConfigurations\http_master.json"*.
  - Refer to the [instructions to Create an API key](https://www.ni.com/docs/en-US/bundle/systemlink-enterprise/page/creating-an-api-key.html).

### NI TestStand

- Launch NI TestStand Sequence Editor.
- Click `Tools`.
- Click `Import/Update from Specification Compliance Manager (SCM)`.
![ToolsOption](docs/images/ToolsOption.png)
- In the opened dialog box, enter Server URL as `http://localhost:50000/`.
- No API key is required.
![ConnectToSLE](docs/images/ConnectToSLE.png)
- Click `Connect` to connect to NI Spec Server Proxy. Ensure the NI Spec Server Proxy server is running before connecting.
- Once the server is connected, the Product drop-down lists the PartNumber available in SLE.
- Select a PartNumber and select the categories to import the specifications.
- Use the specification details imported into FileGlobals.SCM_Specifications in the Test Sequence for Test Automation and measurement data logging with test conditions using the TestStand SCM Integration Workflow.

### How to start the proxy on windows startup automatically?

- Download the [spec-server-proxy.bat](batch_files/spec-server-proxy.bat)
- Press **Win + R** to open the Run dialog.
- Type **shell:startup** and press Enter.
![RunDialog](docs/images/RunDialog.png)
- The Startup folder opens.
- Place the `spec-server-proxy.bat` file in the Startup folder.
- This batch file will start whenever the PC is turned on.

#### Note

- The proxy service will terminate when this window is closed.
![ProxyServerWindow](docs/images/ProxyServerWindow.png)