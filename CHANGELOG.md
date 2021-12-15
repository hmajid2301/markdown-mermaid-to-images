# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2021-12-15
### Added
- Parse image name if first line starts with `%%`.

## [0.2.1] - 2021-03-03
### Changed
- Dependencies won't jump to next major version.
- Latest version of mermaid-cli `8.9.1`.

## [0.2.0] - 2020-04-01
### Added
- Versions to `cli.py` and `Dockerfile`.
- Cleanup output folder before tests run, else they will fail.

### Changed
- Installs `node_modules`, mermaid-cli, in the users home dir `(~)` so that we know it can always be accessed.
- Docker image with an `ENTRYPOINT` to make it easier for people to use script in docker one liner.

### Fixed
- Needed to run script in same folder as `package.json`. Now you can run it from anywhere.

### Removed
- `package*.json` files, we don't need to rely on them.

## [0.1.5] - 2020-03-30
### Fixed
- When converting to markdown using the wrong format, specify `github` style markdown to get correct markdown tables.

## [0.1.4] - 2020-03-30
### Changed
- Using the official mermaid cli tool instead of the other version, was causing various bugs related to creating images.

## [0.1.3] - 2020-03-11
### Fixed
- When running in Docker container, trims image this was due to version of chromium being installed (80) now using 72.

## [0.1.2] - 2020-03-11
### Added
- Coverage job in `.gitlab-ci.yml`.

### Fixed
- Incorrect description for logging level in args.
- Updated description in `README.rst`.

## [0.1.1] - 2020-03-11
### Fixed
- Install mmdc globally in Docker image. 

### Changed
- Tests now compare files directly, as we mock the uuid value for image names.

## [0.1.0] - 2020-03-11
### Added
- Initial Release.

[Unreleased]: https://gitlab.com/hmajid2301/markdown-mermaid-to-images/-/compare/release%2F0.3.0...master
[0.3.0]: https://gitlab.com/hmajid2301/markdown-mermaid-to-images/-/compare/release%2F0.3.0...0.2.1
[0.2.1]: https://gitlab.com/hmajid2301/markdown-mermaid-to-images/-/compare/release%2F0.2.1...0.2.0
[0.2.0]: https://gitlab.com/hmajid2301/markdown-mermaid-to-images/-/compare/release%2F0.2.0...0.1.5
[0.1.5]: https://gitlab.com/hmajid2301/markdown-mermaid-to-images/-/compare/release%2F0.1.5...0.1.4
[0.1.4]: https://gitlab.com/hmajid2301/markdown-mermaid-to-images/-/compare/release%2F0.1.4...0.1.3
[0.1.3]: https://gitlab.com/hmajid2301/markdown-mermaid-to-images/-/compare/release%2F0.1.2...0.1.3
[0.1.2]: https://gitlab.com/hmajid2301/markdown-mermaid-to-images/-/compare/release%2F0.1.1...0.1.2
[0.1.1]: https://gitlab.com/hmajid2301/markdown-mermaid-to-images/-/compare/release%2F0.1.0...0.1.1
[0.1.0]: https://gitlab.com/hmajid2301/markdown-mermaid-to-images/-/tags/release%2F0.1.0