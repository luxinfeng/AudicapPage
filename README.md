# Audicap website

Astro source for the Audicap marketing site. GitHub Pages serves the generated files in `docs/`.

## Local development

Do not open `docs/index.html` with a `file://` URL. The site intentionally uses root-relative assets and links such as `/style.css`, so direct file viewing cannot reproduce the deployed website.

Start the Astro development server instead:

```sh
npm run dev:background
```

Then open [http://localhost:4321](http://localhost:4321).

Useful commands:

```sh
npm run dev:status
npm run dev:stop
npm run build
```

## Editing rules

- Edit page templates in `src/pages/`.
- Edit shared markup in `src/layouts/`.
- Edit static styles and assets in `public/`.
- Do not hand-edit generated files in `docs/`; `npm run build` replaces them.
- Homepage pages must use `variant="home"`.
- High-intent professional-learning landing pages must use `variant="seo"`.

The production build verifies that the homepage and six high-value SEO pages contain the body classes required by their scoped CSS.
