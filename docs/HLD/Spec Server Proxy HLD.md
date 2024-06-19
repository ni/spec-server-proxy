# NI Spec Server Proxy

- [NI Spec Server Proxy](#ni-spec-server-proxy)
  - [Who](#who)
  - [Problem statement](#problem-statement)
  - [Implementation and design](#implementation-and-design)
    - [SCM - SLE APIs](#scm---sle-apis)
    - [Architecture diagram](#architecture-diagram)
    - [Installation](#installation)
    - [Establishment of connection with SLE](#establishment-of-connection-with-sle)
    - [Get products](#get-products)
    - [Get specification](#get-specification)
    - [Upload BDC file.](#upload-bdc-file)
  - [Alternative implementations and designs](#alternative-implementations-and-designs)
  - [Open Issues](#open-issues)

## Who

Author: National Instruments <br/>
Team: ModernLab Success

## Problem statement
 
Currently there is no workflow to exchange data between SystemLink Enterprise (SLE) and NI TestStand.

## Implementation and design

NI TestStand has a workflow to exchange data between itself and Specification Compliance Manager using SCM APIs.

So, the solution is to create a python server to act as a proxy which redirects the requests sent to SCM server to SLE server without affecting the TestStand-SpecificationComplianceManager (SCM) workflow.

To create a python server, Flask framework will be used. The flask server will be running locally in the port 8000. The server can be accessed at http://localhost:8000

This python server internally uses the SystemLink Python Clients and SystemLink SDK to make request to the SLE server.

This client and SDK require Workspace ID and API key. These configurations are taken from the grains file and http_master.json respectively.

The API calls to the SCM server will be redirected to the equivalent SLE server.

The below table shows the API endpoints of SCM and its equivalent in SLE that will be used.

### SCM - SLE APIs

| Data Exchange      | SCM API                                                                    | Equivalent SLE API                                                                                 |
| ------------------ | -------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Get Products       | `/niscm/public/products`                                                   | `/v2/products`                                                                                     |
| Get Specifications | `/niscm/public/spec/<product_name>/<product_revision>`                     | `/nispec/v1/query-specs`                                                                           |
| Upload BDC file    | `/niscm/public/data/upload/<product_name>/<product_revision>/<discipline>` | `/v1/service-groups/Default/upload-files` <br/> To link the file to product: `/v2/update-products` |

As these SCM APIs have different request and response format when compared with their counterparts in SLE, the response from SLE APIs will be converted to SCM APIs' response format.

For Get products, PartNumber of SLE product will be used as the Product Name in the response.

For Get Specifications, conditions and info columns in SLE's response will be formatted to comply with SCM's response.

For upload BDC file, the uploaded file will be stored locally under a directory in the current working directory.
The upload BDC file process in SCM server always calls another request to know the status of the uploaded file following the upload request.
But in SLE server, it is not so. In order to respond to the process execution status a successful response is provided to the request always.

### Architecture diagram

The below picture shows data flow between SystemLink Enterprise and TestStand.

![DataFlow](DataFlow.png)

### Installation

- Follow the steps to set up [NI SystemLink Client](https://www.ni.com/docs/en-US/bundle/systemlink-enterprise/page/setting-up-systemlink-client.html#:~:text=Search%20for%20and%20install%20NI,which%20you%20want%20to%20connect)

- NI Spec Server Proxy Python Package has to be installed in NI SystemLink Client's Python Site Packages.

- Run `"C:\Program Files\National Instruments\Shared\Skyline\Python\3.8\python.exe" -m pip install ni_spec_server_proxy-X_X_X-py3-none-any.whl` to install whl file.

### Establishment of connection with SLE

- Launch NI SystemLink Client and connect to SystemLink Enterprise as per [instructions](https://www.ni.com/docs/en-US/bundle/systemlink-enterprise/page/setting-up-systemlink-client.html)

  - Configurations will be taken from SystemLink Clients.

  - If the SLE version is 2024-04 or older, update the API key in the master.json file at - "C:\ProgramData\National Instruments\Skyline\HttpConfigurations\http_master.json".

  - Refer to the [instructions to create an API key](https://www.ni.com/docs/en-US/bundle/systemlink-enterprise/page/creating-an-api-key.html)

- Run spec-server-proxy.bat file to run the server.
- Open NI TestStand Sequence Editor.
- Select *Tools > Import/Update from Specification Compliance Manager (SCM)* from the TestStand Sequence Editor menu bar.

![ToolsOption](ToolsOption.png)

- Enter the credentials in the dialog box,
  - Server - http://localhost:8000
  - API token - None

![ConnectToSLE](ConnectToSLE.png)

- On Clicking on the *Connect* button, it should be connected to Proxy Server.

### Get products

- After the establishment of connection, all the products' PartNumber available in the SLE server should be listed down.

![GetProduct](GetProducts.png)

### Get specification

- On selecting a PartNumber and Category from the dropped down list, the specifications available in the selected product should be loaded.

![SelectProduct](SelectProduct.png)

- The available specifications in the product should be imported into FileGlobals.SCM_Specifications in TestStand.

### Upload BDC file.

On following the below steps, BDC file generated by TestStand should be uploaded to SLE server.

- Ensure SCM Data in Result Processing is enabled.

![ResultProcessing](ResultProcessing.png)

- In TestStand, create a simple sequence which generates random numbers as measurement for a spec.
- Run the sequence to generate and upload the measurement to SLE.
- Once the sequence is run, the user can view the measurements as BDC files in the respective product under *Files* tab in SLE.

![UploadedFile.png](UploadedFile.png)

- Once the BDC file is uploaded, the routine will create a test result and steps using the file and the result will be available under the *Results* tab.

- The uploaded files will be stored locally.

## Alternative implementations and designs


## Open Issues

No open issues.