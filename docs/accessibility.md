# Accessibility

## WCAG 2.2 AA conformance statement

The Inkomstprognos documentation site targets Web Content Accessibility
Guidelines (WCAG) 2.2 Level AA conformance.

## Checklist

| Criterion | Status | Notes |
|-----------|--------|-------|
| 1.1.1 Non-text content | Conformant | Alt text on all figures |
| 1.3.1 Info and relationships | Conformant | Semantic heading hierarchy (h1-h4) |
| 1.3.2 Meaningful sequence | Conformant | Logical reading order in all pages |
| 1.4.1 Use of colour | Conformant | Information not conveyed by colour alone |
| 1.4.3 Contrast (minimum) | Conformant | MkDocs Material theme provides >= 4.5:1 ratio |
| 1.4.4 Resize text | Conformant | Text scalable to 200% without loss |
| 2.1.1 Keyboard | Conformant | Full keyboard navigability |
| 2.4.1 Bypass blocks | Conformant | Skip-to-content link provided by theme |
| 2.4.2 Page titled | Conformant | Each page has a descriptive title |
| 2.4.6 Headings and labels | Conformant | Descriptive headings throughout |
| 3.1.1 Language of page | Conformant | lang="en" set in HTML |
| 4.1.1 Parsing | Conformant | Valid HTML output from MkDocs |

## Colour contrast

The MkDocs Material theme default palette (indigo primary, white background)
provides a contrast ratio exceeding 4.5:1 for normal text and 3:1 for large
text, meeting WCAG 2.2 AA requirements.

## Figures

All generated figures include descriptive alt text in the documentation.
Figures use colour palettes that are distinguishable in greyscale.

Last updated: 2026-05-11
