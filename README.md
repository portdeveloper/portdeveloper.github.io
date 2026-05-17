# portdeveloper.github.io

Personal site. Plain HTML/CSS, no framework.

## Authoring articles

Source of truth lives in `articles-src/<slug>.md` (YAML frontmatter + markdown body).

### New article workflow

1. Drop assets into `assets/articles/<slug>/`.
2. Create `articles-src/<slug>.md`. Copy an existing one for the frontmatter shape.
3. Build:

   ```
   python3 build.py
   ```

   This regenerates `articles/<slug>.html`, `feed.xml`, and `sitemap.xml`.
4. Add the article to the Writing list in `index.html`.
5. Commit and push.

### Cross-posting

- **Medium** — paste the live `portdeveloper.github.io/articles/<slug>.html` URL into <https://medium.com/p/import>. Medium imports and sets `rel="canonical"` to the original automatically.
- **Dev.to** — uses the same `.md`:

  ```
  export DEVTO_API_KEY=...          # https://dev.to/settings/extensions
  python3 publish_devto.py articles-src/<slug>.md          # creates a draft
  python3 publish_devto.py articles-src/<slug>.md --publish  # publishes
  ```

  First run writes `devto_id` back into the frontmatter; subsequent runs update the same Dev.to post.

  Dev.to tags must be alphanumeric. `publish_devto.py` normalizes `tags` automatically (`"Claude skills"` → `"claudeskills"`). Override with `devto_tags: [...]` in frontmatter if needed.

## Local preview

```
python3 -m http.server 3001
```
