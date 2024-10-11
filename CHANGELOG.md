# Changelog

All notable change to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## NI Spec Server Proxy

## [1.2.1.dev0] - 2024-10-09

### Changed

- To Local host from internal host. Use `localhost` instead of `0.0.0.0` while hosting.
- User manual set up instruction and README.

## [1.2.0] - 2024-05-16

### Changed

- Get Minion ID from file instead of using Query System API.

## [1.1.0] - 2024-05-15

### Added

- TestBench and ChipId META columns in the BDC file.

## [1.0.0] - 2024-05-02

### Added

- Generate SCM API end points response from SLE API response for GetProducts, GetSpecs, UploadBDC file.

### Note

- Condition column values of string type, not being sorted in SLE Response as SCM.
- Empty condition column value is skipped in the SLE response, whereas SCM does have it has None.
- Integer/float type condition column names, not recognized by the jupyter notebook in SLE for reading specs.
- Condition column name with many units, not stored in the clear way in SLE response.
- File is saved locally to a folder in the current working directory and pushed to SLE.
- File name is sanitized to have empty space `''` for `[` and underscores `_` for `]`.