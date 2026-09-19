# CHANGELOG

All notable development changes to the CSS/450 e-commerce capstone project are documented here.

## 2026-09-19

### Added
- Expanded repository validation for malformed menu data.
- Added validation for invalid Boolean values.
- Added validation for malformed and negative prices.
- Added validation for blank required text fields.
- Added validation for invalid and non-positive item IDs.
- Added duplicate item ID detection.
- Added required CSV column validation.
- Added Black Tea Lemonade as a menu item with `allows_milk=False` to support conditional customization testing.
- Expanded the automated test suite to 12 tests.

### Changed
- Improved repository error handling to raise clear `ValueError` messages instead of exposing lower-level parsing exceptions.
- Strengthened CSV parsing so malformed data is rejected before it reaches the application layer.
- Confirmed that milk customization remains a no-cost option for the current MVP.

### Tested
- Verified all 12 automated tests on macOS with Python 3.14.6.
- Performed malformed-data smoke tests by intentionally modifying individual CSV values.
- Verified the complete Streamlit workflow on macOS.
- Installed Python 3.14.6 in the Windows 22H2 lab VM after discovering the existing Python 3.9.7 environment was incompatible with current project requirements.
- Created a fresh Windows virtual environment and restored project dependencies from `requirements.txt`.
- Verified all 12 automated tests on Windows.
- Completed a successful end-to-end Streamlit smoke test on Windows.

## 2026-09-17

### Added
- Added beverage selection from the menu using `item_id`.
- Added beverage customization view.
- Added required Small, Medium, and Large size selections.
- Added conditional milk customization based on `allows_milk`.
- Added size-based price adjustments through `CustomizationService`.
- Added customization validation before continuing.
- Added session-state support for selected beverage, size, milk, and confirmed configuration.
- Added clean navigation back to the menu.
- Added automated tests for customization pricing.

### Changed
- Refactored repeated menu item presentation into a reusable helper.
- Moved pricing logic out of the Streamlit presentation layer and into `CustomizationService`.
- Updated size options to use the service-layer pricing configuration as the source of truth.
- Simplified `requirements.txt` to direct project dependencies.
- Added `.gitignore` and removed generated Python and macOS files from version control.
- Removed unused `data/menu.csv`.

### Fixed
- Fixed Streamlit session-state errors caused by modifying widget-backed values after widget creation.
- Fixed reversed size-selection validation logic.
- Fixed inconsistent `configured_item` session-state naming.
- Ensured confirmed customization is cleared when the customer changes size or milk.
- Ensured customization state resets when returning to the menu.

### Tested
- Completed menu-to-customization end-to-end smoke testing.
- Verified 5 automated tests passed after Feature 2 implementation.

## 2026-09-16

### Added
- Completed the menu browsing vertical slice.
- Added Coffee, Espresso, and Tea category browsing.
- Added Popular Drinks section.
- Added menu item rendering from CSV data.
- Added availability filtering through `MenuService`.
- Added repository and service unit tests.
- Expanded `menu_items.csv` with additional beverages.

### Changed
- Updated Cold Brew to the Coffee category.
- Refined the Streamlit menu browsing interface.

### Fixed
- Added `_to_bool()` conversion for CSV Boolean values.
- Corrected menu loading after identifying unsaved CSV data during smoke testing.

## 2026-09-15

### Added
- Created the initial project structure.
- Added `models`, `repositories`, `services`, `tests`, and `data` modules.
- Added the `MenuItem` data model.
- Added `MenuRepository` for reading menu data from CSV.
- Added `MenuService` for application-level menu filtering.
- Added initial `menu_items.csv` business data.
- Added Streamlit application entry point.
- Added `pytest.ini` for project import configuration.
- Added initial project dependencies.

### Tested
- Successfully launched the Streamlit application.
- Verified menu data could be loaded from CSV through the repository and service layers.