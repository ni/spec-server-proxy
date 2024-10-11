# NI Spec Server Proxy

### Description

- NI Spec Server Proxy is a python server used for accessing SLE products and specifications using SLE APIs.

### Prerequisites

- Follow the steps to set up [NI SystemLink Client](https://www.ni.com/docs/en-US/bundle/systemlink-enterprise/page/setting-up-systemlink-client.html#:~:text=Search%20for%20and%20install%20NI,which%20you%20want%20to%20connect)

#### Note

- Ensure to select the `NI SystemLink Python 3.8 SDK` during installation of NI SystemLink Client.

### Code Setup

- Clone the repository using `git clone <respository link>`.
- Check out to the required branch using `git checkout <branch name>`.

### Setup Virtual Environment

- Open terminal.
- Run `cd ni-spec-server-proxy`
- Run `poetry env use "C:\Program Files\National Instruments\Shared\Skyline\Python\3.8\python.exe"`.
- Run `poetry shell` to activate virtual environment.
- Run `poetry install` to install dependency files.

#### Note

- Ensure NI VPN is connected.

### Example using NI TestStand

#### Build whl File

- Run `poetry build` to build whl file.

#### Installation of whl File

- Run `"C:\Program Files\National Instruments\Shared\Skyline\Python\3.8\python.exe" -m pip install ni_spec_server_proxy-X_X_X-py3-none-any.whl` to install whl file.
- Run `"C:\Program Files\National Instruments\Shared\Skyline\Python\3.8\python.exe" -m ni_spec_server_proxy` to run server.

#### NI TestStand

- Open NI TestStand.
- Click `Tools`.
- Click `Import/Update from Specification Compliance Manager (SCM)`.
- In the opened dialog box, enter Server URL as `http://localhost:50000/`.
- No API key is required.
- Click `Connect` to connect to NI Spec Server Proxy. Ensure the NI Spec Server Proxy server is running before connecting.
