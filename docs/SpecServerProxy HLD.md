# NI SpecServerProxy

- [NI SpecServerProxy](#ni-specserverproxy)
  - [Who](#who)
  - [Problem Statement](#problem-statement)
  - [Proposed Solution](#proposed-solution)
  - [Implementation / Design](#implementation--design)
  - [Open Issues](#open-issues)

## Who
_Author:_ National Instruments <br/>
_Team:_ ModernLab Success

## Problem Statement

Currently there is no workflow to exchange data between SystemLink Enterprise (SLE) and NI TestStand without affecting the TestStand-SpecificationComplianceManager (SCM) workflow.

## Proposed Solution

Python package to enable data exchange between SystemLink Enterprise (SLE) and NI TestStand.

## Implementation / Design

- Flask server to act as a proxy which redirects requests sent to SCM server to SLE server.
- Server uses SystemLink Python Clients to access SLE APIs.
- Endpoints to enable
  - Get products from SLE server.
  - Get available specs in a product in SLE server.
  - Upload measurement BDC file to a product in SLE server.

## Open Issues

- Temporary solution only.
- Uploaded measurement BDC files are stored locally.
