---
name: Muted Tech Noir
colors:
  surface: '#191114'
  surface-dim: '#191114'
  surface-bright: '#413739'
  surface-container-lowest: '#140c0e'
  surface-container-low: '#22191c'
  surface-container: '#261d20'
  surface-container-high: '#31272a'
  surface-container-highest: '#3c3235'
  on-surface: '#efdee2'
  on-surface-variant: '#dac0c6'
  inverse-surface: '#efdee2'
  inverse-on-surface: '#382e30'
  outline: '#a28b90'
  outline-variant: '#544247'
  surface-tint: '#ffb1c8'
  primary: '#ffb1c8'
  on-primary: '#610b33'
  primary-container: '#e6779d'
  on-primary-container: '#630d35'
  inverse-primary: '#9c3d61'
  secondary: '#f3b6c8'
  on-secondary: '#4c2332'
  secondary-container: '#663948'
  on-secondary-container: '#e0a5b6'
  tertiary: '#84da87'
  on-tertiary: '#00390f'
  tertiary-container: '#58ac5f'
  on-tertiary-container: '#003b10'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffd9e2'
  primary-fixed-dim: '#ffb1c8'
  on-primary-fixed: '#3e001d'
  on-primary-fixed-variant: '#7e2549'
  secondary-fixed: '#ffd9e2'
  secondary-fixed-dim: '#f3b6c8'
  on-secondary-fixed: '#330f1d'
  on-secondary-fixed-variant: '#663948'
  tertiary-fixed: '#9ff7a1'
  tertiary-fixed-dim: '#84da87'
  on-tertiary-fixed: '#002106'
  on-tertiary-fixed-variant: '#00531a'
  background: '#191114'
  on-background: '#efdee2'
  surface-variant: '#3c3235'
typography:
  h1:
    fontFamily: Sora
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.2'
  h2:
    fontFamily: Sora
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  label-sm:
    fontFamily: Space Grotesk
    fontSize: 14px
    fontWeight: '500'
    lineHeight: '1'
    letterSpacing: 0.05em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 48px
---

# Design System: Muted Tech Noir

## Brand & Style
This design system embodies a **Sophisticated / Industrial** aesthetic tailored for professional digital environments that require focus and depth. It transitions from a loud, neon-centric persona to a more refined, "Muted Tech" character. The brand personality is steady, precise, and mature, utilizing a dark-mode-first approach that favors organic, dusty tones over high-energy vibrance. It seeks to evoke a sense of calm technical mastery and understated elegance.

## Colors
The system is optimized for **Dark Mode**, utilizing a palette of desaturated roses and earthy greens against a warm, neutral-grey base.
*   **Primary:** #bb557a — A muted rose used for primary actions and brand emphasis.
*   **Secondary:** #9c6878 — A dusty mauve for supportive interactive elements.
*   **Tertiary:** #58ac5f — A forest green for success states and secondary accents.
*   **Neutral:** #817477 — A warm, stony grey that serves as the foundation for surfaces and backgrounds.

## Typography
A sophisticated three-font pairing ensures both personality and performance:
*   **Headlines:** **Sora** is used for all headings, providing a bold, geometric character.
*   **Body:** **Inter** is used for all body copy and descriptions to ensure maximum readability on screens.
*   **Labels:** **Space Grotesk** is used for UI labels, buttons, and data visualizations, lending a technical, futuristic edge to the interface.

## Layout & Spacing
The system utilizes a fluid grid with a base-8 rhythm. With a spacing multiplier of 2, the UI emphasizes clarity through generous whitespace. 
*   **Gaps & Gutters:** Scaled in multiples of 8px (e.g., 16px, 24px, 48px).
*   **Margins:** Standardized at 24px for mobile and 48px for desktop layouts.

## Elevation & Depth
Depth is achieved through **Tonal Layering**. In this dark environment, "higher" elements are represented by lighter, warmer shifts of the neutral grey base rather than heavy shadows. Components maintain a flat, architectural feel, using subtle value shifts to indicate hierarchy and interaction.

## Shapes
The design language uses **Soft** geometry. 
*   **Standard Radius:** 0.25rem (4px) for buttons and input fields.
*   **Large Radius:** 0.5rem (8px) for cards, panels, and modals.
This slight rounding provides a modern, polished feel that balances the technical sharpness of the labels.

## Components
*   **Buttons:** Feature the 4px rounded corners. Primary buttons use the muted rose (#bb557a); secondary buttons use the dusty mauve (#9c6878) as an outline or low-opacity fill.
*   **Input Fields:** Use a surface slightly lighter than the background with a muted rose focus state. Labels are set in Space Grotesk.
*   **Cards:** Elevated via subtle tonal shifts in the neutral palette, keeping the interface feeling grounded and cohesive.
*   **Selection Controls:** Checkboxes and radio buttons use the tertiary green (#58ac5f) for active states to provide clear, natural feedback.