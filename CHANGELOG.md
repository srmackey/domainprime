# Changelog

## [Unreleased]

### Added

- A board line can end with `· waiting` when the principal is waiting on it. Envoy reads it as awaiting rather than unaccounted, so it is never flagged, and it stays until the principal changes it. A rewrite of the board keeps the mark.

## [0.1.1] - 2026-10-31

### Changed

- The session-start pack no longer marks a sitrep stale for its age, or for a date written inside a Forefront. Board lines that are overdue or due within seven days are still called out. A settle-wait heading is the chair's address.
