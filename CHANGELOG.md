# Changelog

## [4.0.0] - 2026-08-06

### Added
- **Dino Clock Font Customization**: You can now choose a custom font for the Chrome Dino Game clock directly from the new Settings UI, replacing the default Bungee font!
- **Ignore Media Keys**: A new toggle allows you to adjust volume, mute, and use play/pause buttons without dismissing the screensaver.
- **24-Hour Time**: Support for 24-hour military time formats across all clocks.
- **Leading Zero Support**: Ability to pad the hour with a leading zero (e.g., `09:00` instead of `9:00`).
- **Reset to Defaults**: Quickly restore factory defaults if you've messed up the colors or scales.
- **Independent Zoom Memory**: Each clock mode (Rotary, Fliqlo, Dino) now perfectly remembers its own custom zoom scale size independently. 

### Changed
- **Settings UI Redesign**: Completely refactored the native Windows settings dialog to use a grid layout, drastically improving visual aesthetics and usability for the many new toggles.
- **Domain Migration**: Repository migrated to `github.com/kushalarvindo/dinoscreener`.
- **Proprietary License**: Implemented strict All Rights Reserved licensing to protect intellectual property.

### Fixed
- Fixed an issue where the settings UI OK button would crash if internal layout components were missing.
- Adjusted vertical spacing for time and date in the Dino mode to be perfectly symmetrical with the ground level.
