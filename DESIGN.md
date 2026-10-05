---
version: alpha
name: Global Freight & Supply Chain Interface
description: "Design tokens for the shipments page (list, search, create and edit in a modal, delete). Fonts, colours and component presets chosen with Google Stitch."
colors:
  primary: '#002B49'
  primary-hover: '#003D66'
  primary-active: '#001F35'
  on-primary: '#FFFFFF'
  secondary: '#0072CE'
  neutral: '#4A5568'
  background: '#F4F6F9'
  surface: '#FFFFFF'
  surface-subtle: '#F8FAFC'
  on-surface: '#111C2C'
  overlay: 'rgba(0, 43, 73, 0.4)'
  error: '#991B1B'
  error-container: '#FEF2F2'
  error-container-hover: '#FEE2E2'
  status-in-transit-surface: '#EFF6FF'
  status-in-transit-text: '#1E40AF'
  status-delivered-surface: '#ECFDF5'
  status-delivered-text: '#065F46'
typography:
  headline-lg:
    fontFamily: Hanken Grotesk
    fontSize: 24px
    fontWeight: 600
    lineHeight: 32px
    letterSpacing: -0.015em
  headline-md:
    fontFamily: Hanken Grotesk
    fontSize: 18px
    fontWeight: 600
    lineHeight: 24px
    letterSpacing: -0.01em
  body-md:
    fontFamily: Hanken Grotesk
    fontSize: 13px
    fontWeight: 400
    lineHeight: 18px
  label-ui:
    fontFamily: Hanken Grotesk
    fontSize: 12px
    fontWeight: 600
    lineHeight: 16px
    letterSpacing: 0.01em
  table-header:
    fontFamily: Hanken Grotesk
    fontSize: 11px
    fontWeight: 700
    lineHeight: 14px
    letterSpacing: 0.05em
  label-mono:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: 500
    lineHeight: 16px
    letterSpacing: 0.02em
  label-mono-sm:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: 500
    lineHeight: 14px
    letterSpacing: 0.03em
rounded:
  base: 0.25rem
  container: 0.5rem
  overlay: 0.75rem
spacing:
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 0.75rem
  space-lg: 1rem
  space-xl: 1.5rem
  margin: 1.5rem
components:
  page:
    backgroundColor: "{colors.background}"
    textColor: "{colors.on-surface}"
    typography: "{typography.body-md}"
  panel:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    rounded: "{rounded.container}"
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-ui}"
    rounded: "{rounded.base}"
    height: 36px
  button-primary-hover:
    backgroundColor: "{colors.primary-hover}"
  button-primary-active:
    backgroundColor: "{colors.primary-active}"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    typography: "{typography.label-ui}"
    rounded: "{rounded.base}"
    height: 36px
  button-secondary-hover:
    backgroundColor: "{colors.surface-subtle}"
  button-ghost:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.secondary}"
    typography: "{typography.label-ui}"
    rounded: "{rounded.base}"
    height: 36px
  button-ghost-hover:
    backgroundColor: "{colors.surface-subtle}"
    textColor: "{colors.secondary}"
  button-destructive:
    backgroundColor: "{colors.error-container}"
    textColor: "{colors.error}"
    typography: "{typography.label-ui}"
    rounded: "{rounded.base}"
    height: 36px
  button-destructive-hover:
    backgroundColor: "{colors.error-container-hover}"
    textColor: "{colors.error}"
  badge-booked:
    backgroundColor: "{colors.surface-subtle}"
    textColor: "{colors.neutral}"
    typography: "{typography.label-mono-sm}"
    rounded: "{rounded.base}"
    height: 22px
  badge-in-transit:
    backgroundColor: "{colors.status-in-transit-surface}"
    textColor: "{colors.status-in-transit-text}"
    typography: "{typography.label-mono-sm}"
    rounded: "{rounded.base}"
    height: 22px
  badge-delivered:
    backgroundColor: "{colors.status-delivered-surface}"
    textColor: "{colors.status-delivered-text}"
    typography: "{typography.label-mono-sm}"
    rounded: "{rounded.base}"
    height: 22px
  badge-cancelled:
    backgroundColor: "{colors.error-container}"
    textColor: "{colors.error}"
    typography: "{typography.label-mono-sm}"
    rounded: "{rounded.base}"
    height: 22px
  table-header:
    backgroundColor: "{colors.surface-subtle}"
    textColor: "{colors.neutral}"
    typography: "{typography.table-header}"
    height: 36px
  table-row:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    typography: "{typography.body-md}"
    height: 44px
  table-row-hover:
    backgroundColor: "{colors.surface-subtle}"
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    typography: "{typography.body-md}"
    rounded: "{rounded.base}"
    height: 36px
  modal:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    rounded: "{rounded.overlay}"
    width: 640px
  modal-backdrop:
    backgroundColor: "{colors.overlay}"
  alert-error:
    backgroundColor: "{colors.error-container}"
    textColor: "{colors.error}"
    typography: "{typography.body-md}"
    rounded: "{rounded.base}"
---

## Brand & Style

Operational precision for people who manage freight: calm, dense, engineered rather than decorated. The aesthetic is **Executive Technical Minimalist**, Swiss functionalism with enterprise-SaaS restraint: no gradients, no decorative motion, crisp alignment, systematic type.

**Scope.** This file covers what the shipments app builds: one page with a toolbar (search and a "New shipment" button), a data table, a create/edit modal and an inline error banner.

## Colors

Deep maritime navy for structure and the main action, cobalt for interaction, steel grey for secondary text. Values live in the tokens above (line colours excepted, see Lines); this section says where each one is used.

- **Primary** (`primary`): primary buttons, modal titles, secondary-button text. Hover and pressed shades are `primary-hover` and `primary-active`; text on it is `on-primary`.
- **Secondary** (`secondary`): focus rings, the focused input border, ghost-button text.
- **Neutral** (`neutral`): table column headers and muted text such as the loading and empty states.
- **Canvas and panels:** the page sits on `background`; panels and table rows on `surface`; header fill and hover on `surface-subtle`; body text is `on-surface`.
- **Lines:** the token schema has no border property, so line colours are given here. *Panel line* `#E2E8F0`: panels and the modal header rule. *Strong line* `#CBD5E1`: inputs, the secondary button, the table header edge, the Booked badge. *Row line* `#F1F5F9`: between table rows. *Blue edge* `#BFDBFE`: In transit badge. *Green edge* `#A7F3D0`: Delivered badge. *Red edge* `#FECACA`: Cancelled badge, destructive button and error banner.
- **Overlay:** `overlay` behind the modal.
- **Error:** `error` text on `error-container`, hover `error-container-hover`. The Cancelled badge, the destructive button and the error banner all share it.

### Shipment status

One badge per status. The label is always spelled out, so colour never carries the meaning alone.

| API value | Badge label | Look |
|---|---|---|
| `booked` | Booked | grey: `surface-subtle` fill, `neutral` text, strong line |
| `in_transit` | In transit | blue: `status-in-transit-surface` fill, `status-in-transit-text` text, blue edge |
| `delivered` | Delivered | green: `status-delivered-surface` fill, `status-delivered-text` text, green edge |
| `cancelled` | Cancelled | red: `error-container` fill, `error` text, red edge |

## Typography

**Hanken Grotesk** for interface text; **JetBrains Mono** for operational identifiers and status badges (the shipment `reference` is the identifier here).

- `headline-lg`: page title. `headline-md`: modal title.
- `body-md`: table cells, inputs, helper and error text.
- `label-ui`: buttons and form labels.
- `label-mono`: the reference column. `label-mono-sm`: status badges.
- `table-header`: column headers, set in uppercase.

Numerals in tables use `font-variant-numeric: tabular-nums` so dates do not jitter.

## Layout & Spacing

A single fluid page inside the page `margin`, on a 4px base unit (the `space-*` scale). Toolbar controls are dense, table rows are taller. Text columns align left; reference, ETA and status are centred. Table cells never wrap: on narrow screens the table scrolls sideways inside its panel, and the toolbar wraps.

## Elevation & Depth

Depth comes from surface zoning and 1px borders, not blur.

- **Canvas:** `background`, no border.
- **Panel** (toolbar, table): `surface` with a 1px panel line, no shadow.
- **Modal:** `surface` over the `modal-backdrop`, with the shadow `0 20px 25px -5px rgba(0, 43, 73, 0.12), 0 8px 10px -6px rgba(0, 43, 73, 0.06)`.

## Shapes

Soft precision: small radii. `base` for buttons, inputs, badges and the error banner; `container` for panels; `overlay` for the modal.

## Components

### Buttons

Dense height, label in `label-ui`, radius `base`. Focus is a 2px offset ring in `secondary`. Hover and pressed states are the `-hover` and `-active` variants in the tokens. While a save is in progress the button shows at 60% opacity with a not-allowed cursor.

- **Primary:** "New shipment", "Save". Navy fill, white text.
- **Secondary:** "Cancel". `surface` fill, 1px strong line, `primary` text.
- **Ghost:** "Edit". No fill, `secondary` text.
- **Destructive:** "Delete". `error-container` fill, 1px red edge, `error` text.

### Status badges

`label-mono-sm`, radius `base`, 1px border in the badge's edge colour, padding 2px 8px. Text only.

### Table

Header: `table-header` type in `neutral` on `surface-subtle`, with a 1px strong line as bottom edge. Rows: `surface`, a 1px row line between rows, `surface-subtle` on hover. Loading and empty states are a plain `neutral` line inside the panel.

### Inputs

Text, select and date inputs share one style: 1px strong line, radius `base`, `body-md`, horizontal padding 10px. Focus: `secondary` border plus a 1px `secondary` ring. The toolbar search is the same input. A field error is `error` text in `body-md` under the field, first letter capitalised, and disappears as soon as the form is edited.

### Modal

Centred, `overlay` radius, over `modal-backdrop`. Title in `headline-md` and `primary`, a panel line under the header, actions right-aligned in the footer: Cancel (secondary), then Save (primary). One modal serves both create and edit; below 480px it uses a single column.

### Error banner

Inline above the table for API and network errors: `error-container` fill, 1px red edge, `error` text, `body-md`, radius `base`.
