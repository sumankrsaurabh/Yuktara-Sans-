# Yuktara Sans

Brand typeface for Yuktara Tech, derived from Inter (SIL Open Font License 1.1) with Yuktara's house style switched on by default: single-storey "a", simplified "u", round quotes/commas, open digits (4 6 9), and slightly open letter-spacing.

## Families
- **Yuktara Sans** (text/UI): Light, Regular, Medium, SemiBold, Bold, Italic, BoldItalic
- **Yuktara Sans Display** (headlines, logos): Regular, Medium, SemiBold, Bold

## Folders
- `fonts/` desktop OpenType (.otf), for installing and design tools
- `css/` ready-made stylesheet declaring every weight
- `web/` .woff files for websites and apps
- `source/customize_inter.py` build script (needs Inter static OTFs + fontTools); edit `FEATURES` / `TRACKING` to restyle

## Quick start
```html
<link rel="stylesheet" href="css/yuktara-sans.css">
<style>body{font-family:"Yuktara Sans",system-ui,sans-serif} h1{font-family:"Yuktara Sans Display","Yuktara Sans",sans-serif}</style>
```

## Notes
The house style is applied through the `calt` OpenType feature, so it needs a modern text engine (browsers, Figma, Word, macOS/Windows apps). If an app turns contextual alternates off, you will see plain Inter shapes.

License: the font keeps the OFL 1.1 terms of Inter (see `LICENSE-Inter-OFL.txt`). Keep that file and the copyright notices when redistributing. Inter is a trademark of rsms; this font is renamed Yuktara Sans.
