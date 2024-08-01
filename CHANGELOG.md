# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of Carbon with a terminal-based GUI for Kubernetes management.
- Provider selection 
- Resources views in a table format
- Built-in terminal loaded config from yaml

### Changed
- None

### Fixed
- None

### Deprecated
- None

### Removed
- None

### Security
- None

## [1.0.0] - 2024-07-31

### Added
- Basic resources creation 
- Editable resource by selecting resources name
- More information on resources table header and data
- Creation menu on sidebar for resources

### Changed
- Improved code readability on ui.py
- Enhanced load config UI
- UI Improvements for better usability and accessibility.
- Moved tables code file to k8s folder

### Fixed
- Various bugs regarding mouse interaction
- Terminal output format
- Terminal command line
- Terminal not detecting yaml config file 
- Various bugs regarding yaml editor
- Various bugs regarding urwid functions

### Deprecated
- None

### Removed
- None

### Security
- None

## [1.1.0] - 2024-08-01

### Added
- **New Resources**: ConfigMaps and Secrets
- Can modify ConfigMaps and Secrets
- Loader on selecting resources

### Changed
- Adjust dependencies on setup.py
- Enhanced load config UI
- Modular component sidebar, loadconfig, and main menu
- Code refactor on ui.py

### Fixed
- Various bugs regarding resources loader

### Deprecated
- None

### Removed
- None

### Security
- None