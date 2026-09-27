# CHANGELOG

All notable development changes to the CSS/450 e-commerce capstone project are documented here.

## 2026-09-26

### Changed
- Removed obsolete temporary cart-seed development code from `app.py`.
- Removed an unused `Order` import.
- Renamed the demo tax-rate constant to `ORDER_TAX_RATE` for clearer production-oriented naming.
- Added stable cart-line identifiers to `CartItem` for UI state management.
- Replaced the four-column cart quantity controls with a more mobile-friendly quantity input and remove action.
- Improved cart behavior on narrow mobile displays while preserving the existing cart service logic.

### Tested
- Verified all 27 automated tests pass after the cleanup and cart UX changes.
- Completed desktop acceptance testing of the full customer journey.
- Completed mobile smoke testing of menu navigation, customization, cart quantity adjustment, removal, order submission, and confirmation.
- Verified cart totals and order data remain correct after quantity changes and item removal.

## 2026-09-24

### Added
- Added `CartService.add_item()` to support adding configured beverages to the active order.
- Added `Order` model for submitted-order data, including order number, items, subtotal, tax, total, and status.
- Added `OrderService` for validating and submitting completed orders.
- Added order confirmation view with preserved beverage details, totals, order number, and received status.
- Added navigation for continuing shopping and starting a new order.
- Expanded the automated test suite to 27 tests.

### Changed
- Replaced temporary seeded cart data with an empty production cart initialized through Streamlit session state.
- Connected the beverage customization flow to `CartItem` and the active cart.
- Preserved selected beverage size, applicable milk customization, quantity, and price through cart review and order submission.
- Connected the cart's Place order action to the order-submission workflow.
- Cleared the active cart after submission while preserving submitted-order data for confirmation.

### Tested
- Verified all 27 automated tests pass on macOS with Python 3.14.6.
- Completed an end-to-end smoke test covering menu browsing, beverage customization, cart addition, continued shopping, quantity adjustment, item removal, order submission, confirmation, and starting a new order.
- Verified multiple configured beverages persist correctly in the cart and that non-applicable milk details are omitted.

## 2026-09-22

### Added
- Added `CartItem` model for configured order items.
- Added `CartService` for quantity changes, item removal, subtotal, tax, and total calculations.
- Added cart review interface using Streamlit session state.
- Added temporary seeded cart data for isolated cart development.
- Expanded automated test suite to 23 tests.

### Changed
- Added size and applicable milk details to order review.
- Added configurable tax-rate input to cart calculations.

### Tested
- Verified all 23 automated tests pass on macOS with Python 3.14.6.
- Completed cart smoke testing for quantity changes, removal, recalculation, and empty-cart behavior.

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