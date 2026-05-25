# Image prompts: copy-page-button article

Working notes for generating the cover + inline images. Aesthetic: low-budget 1990s fantasy variety show / xianxia kitsch.

---

## fal.ai workflow

### Path 1: fast-sdxl with strong negative prompt

Cost: ~$0.003 per image.

- Model: `fal-ai/fast-sdxl` (or `fast-lightning-sdxl` for cheaper/faster)
- Image size: `1024x768`
- Steps: `25` to `30`
- Guidance scale: `6` to `7` (lower than default)
- Num images: `4` per run

### Exact playground settings (field by field)

| Field | Value |
|---|---|
| Prompt | one of the three prompts below |
| Seed | `random` for first roll. After a good roll, copy the seed and reuse it on the other two prompts to keep the same wizard. |
| Num Inference Steps | `25` |
| Sync Mode | off |
| Negative Prompt | the negative prompt block below (replace whatever is in there) |
| Image Size | Landscape, `1024 x 768` (prompts are written for 4:3, not square) |
| Expand Prompt | **OFF**. This auto-rewrites your prompt to be cleaner, which is the opposite of what we want. |
| Format | `jpeg`. JPEG compression artifacts are on-vibe, leave it. |
| Guidance scale (CFG) | `6` (drop from default 7.5). Lower CFG = less "ideal" rendering. |
| Embeddings | empty |
| Num Images | `4`. Same prompt, 4 rolls per run, ~$0.012 total. Pick best. |
| Safety Checker Version | `v1` |
| Loras | empty (path 1 only) |

### Path 2: SDXL + VHS LoRA (if path 1 too clean)

Cost: ~$0.005 per image.

- Model: `fal-ai/lora`
- Get a LoRA from civitai.com: filter by LoRA + SDXL, search `VHS` or `Analog Film` or `90s VHS`, sort by downloads
- Copy the `.safetensors` direct download URL
- In the Loras field, add: `path` = that URL, `scale` = `1.0` (push to `1.3` if weak, `0.7` if it eats the composition)
- Add the LoRA's trigger word at the start of the prompt if it has one
- Same prompt and negative as path 1

### Image-to-video

- Model: `fal-ai/kling-video/v2/standard/image-to-video` (or whatever the newest Kling i2v endpoint is on fal — check the model list, newer versions land regularly)
- Cost: ~$0.25 per 5-second clip on standard, ~$0.50+ on pro
- One motion per prompt only: `robes sway, beard moves in wind, scroll glows brighter`

#### Step by step

1. Save your favorite still locally (or copy its URL from the fal output).
2. Open the Kling image-to-video model on fal.
3. Upload the still (or paste the URL).
4. Set the fields below.
5. Roll. Wait ~2-3 minutes. Download the mp4.

#### Field-by-field settings

| Field | Value |
|---|---|
| Image URL / Image | upload your still, or paste the fal CDN URL |
| Prompt | a single motion sentence — see "motion prompts" below |
| Negative Prompt | `blurry, distorted, deformed, melting, mutated, camera zoom, fast camera move, camera shake, scene change` |
| Duration | `5` seconds. Short clips animate better. Use 10 only for an establishing shot. |
| Aspect Ratio | match your still — `4:3` if you used 1024x768, else `16:9` |
| CFG Scale | `0.5` (Kling is opposite to SDXL — lower = it follows your motion prompt more loosely, which usually looks more natural) |
| Seed | `random` first roll. Reuse if you want to iterate on the prompt for the same motion. |

#### Motion prompts that work

Keep to one or two physical things only. Kling will fight you if you ask for too much.

Cover (immortal scribe):

```
The wizard slowly blinks. His beard and the ends of his robe sway gently in a slight breeze. The glowing scroll in his hand pulses brighter, then dimmer. The flame at his feet flickers. The samoyed dog tilts its head slightly.
```

Inline 1 (typing on the keyboard):

```
The wizard's hands type slowly on the keyboard. His beard sways gently. The CRT monitor flickers. The MONAD scroll above his head rotates slowly. The flame on the desk flickers.
```

Inline 2 (three immortals + crumbling arch):

```
The three immortals stand still. Their robes and beards sway in a light wind. Each scroll pulses with a soft glow. The UFO in the sky drifts slowly from left to right. The samoyed dog runs across the foreground.
```

#### Motion prompt rules

- One subject, one or two motions. More than that and Kling smears.
- Don't write camera moves (`zoom in`, `pan left`). Kling handles camera. Let it.
- Don't try to add VHS effects via the motion prompt — those need to already be in the still.
- If a clip comes out with the subject's face melting, the still had ambiguous detail there. Re-roll the still or pick a different one.

### Adding period audio (huge vibe boost)

Kling doesn't reliably do audio that fits this aesthetic. Add it in post:

1. Open **CapCut** (free, web and desktop).
2. Drop the clip(s) in.
3. Add one of these as background audio:
   - Royalty-free 90s cheesy synth (search CapCut's library for `synth`, `new age`, `mystical`)
   - YouTube Audio Library: filter by `90s`, `synth`, `cinematic` ironic
   - Or pull a 5-second loop from a known kitsch source (Wham!, Enya, generic 90s xianxia soundtrack on YouTube → download → use under fair-use commentary)
4. Add a VHS preset if your still wasn't dirty enough: CapCut → Effects → search `VHS`, `glitch`, `scan lines`. Stack at 30-50% intensity.

### Stitching multiple clips

If you generate three clips (cover, inline 1, inline 2) and want them as one video for the X post:

1. CapCut, drop all three on the timeline in order.
2. Between clips, add a hard cut (no fancy transition — the bad cuts are the vibe).
3. Optionally add a caption at the top of each clip in a chunky white font with black drop shadow (Impact / Arial Bold), like a tweet caption.
4. Export 1080p, 30fps, mp4. Done.

### Budget for the whole article

- 12 still rolls at $0.003 each = $0.04
- 3 final video clips at $0.25 each = $0.75
- Total: under a dollar.

### Re-use the same character across images

Note the seed from a successful run (fal returns it). Reuse the seed with small prompt edits to keep the same wizard across all three article images.

---

## Negative prompt (use on every image)

```
cinematic, professional, high quality, 4k, 8k, sharp focus, magazine cover, dramatic lighting, hollywood, premium, polished, glossy, hd, hdr, modern, photorealistic, dslr, smooth skin, beautiful, cgi, render, octane, unreal engine, artstation, trending, masterpiece, depth of field, bokeh, color grading, cinematic composition
```

---

## Prompt 1: Cover — the immortal scribe of the sacred scrolls

```
1992 public-access cable TV screenshot, elderly Taoist immortal with long white beard, tall pointed silver rhinestone wizard hat, ornate silver-blue brocade robes with golden trim, stares directly at camera, holding glowing parchment scroll in one hand that reads "COPY PAGE" in glowing yellow sans-serif text, making peace sign with other hand, small white samoyed dog at his feet wearing tiny matching robes, painted matte starfield backdrop, glowing halo ring of light behind subject, dry ice fog drifting across frame, practical flame effect on floor, VHS tape quality, heavy chroma bleed especially on red and blue, magenta halo around bluescreen subject, soft out-of-focus background, scan lines, head switching noise at bottom of frame, 480i, 4:3 aspect ratio, polyester costume, cardboard set, halogen stage lighting from camera-left, harsh shadow on backdrop, sincere amateur production, late-night cable fantasy variety show, found footage
```

---

## Prompt 2: Inline — the original spell (built for Monad docs)

```
1992 public-access cable TV screenshot, same elderly Taoist immortal with long white beard and tall silver rhinestone wizard hat, sitting cross-legged on a single chunk of styrofoam painted to look like a cloud, deep blue painted backdrop with stick-on glitter stars, typing on a beige 1995-era IBM keyboard balanced on his knees, a CRT monitor floats next to him with no cable attached showing green-on-black text, above his head a glowing scroll unfurls in midair with the word "MONAD" visible in glowing yellow text, intense concentration on his face, practical flame effect on the desk for no reason, VHS tape quality, heavy chroma bleed, magenta halo around bluescreen subject, soft out-of-focus background, scan lines, 480i, 4:3 aspect ratio, polyester costume, cardboard set, halogen stage lighting, sincere amateur production, late-night cable fantasy variety show, found footage
```

---

## Prompt 3: Inline — the scaffolding outlived its host

```
1992 public-access cable TV screenshot, group shot of three elderly Taoist immortals standing in a row on styrofoam clouds, each wearing slightly different colored brocade robes (one blue, one gold, one red) and tall pointed rhinestone wizard hats, each holding up a glowing scroll above their head, the scrolls read "SUI", "ETHEREUM", and "ARBITRUM" respectively in glowing yellow sans-serif text, behind them a crumbling cardboard stone arch labeled "MONAD" sits broken in the background overgrown with fake plastic vines, poorly composited UFO hovering in the starfield above, a small white samoyed dog runs across the foreground in motion blur, VHS tape quality, heavy chroma bleed, magenta halo around bluescreen subjects, soft out-of-focus background, scan lines, head switching noise at bottom of frame, 480i, 4:3 aspect ratio, polyester costumes, cardboard set, halogen stage lighting from camera-left, harsh shadow on backdrop, sincere amateur production, late-night cable fantasy variety show, found footage
```

---

## If output is still too clean

Try in this order:

1. Drop guidance scale from `7` to `5`.
2. Drop resolution to `768x768`.
3. Add to start of prompt: `low quality, lo-fi, degraded archival footage, recorded off cable in 1992 to VHS and dubbed twice`.
4. Add to negative: `clean, crisp, detailed, well-lit, balanced exposure`.
5. Switch to path 2 (SDXL + VHS LoRA).
6. Last resort: generate clean, then degrade in post (save as low-quality JPEG, run a VHS filter in CapCut / Photoshop).

---

## If output looks like a painting instead of a video tape shot

SDXL is defaulting to "fantasy illustration" mode because of the wizard keywords. You need to hammer "this is a photograph of a real costumed actor on a real set" much harder.

### 1. Front-load the prompt with photographic framing

Prepend this to the start of every prompt (before "1992 public-access..."):

```
analog photograph, live-action footage, real costumed actor on a real set, screen capture from a videotape, color photograph of a man,
```

The phrase `color photograph of a man` is doing heavy lifting. SDXL knows that style. `wizard` alone triggers illustration mode.

### 2. Add anti-painting terms to the negative prompt

Replace your negative prompt with this full version:

```
painting, illustration, drawing, sketch, artwork, digital art, concept art, watercolor, oil painting, acrylic, ink, anime, cartoon, comic, manga, render, 3d render, cgi, octane, unreal engine, artstation, deviantart, trending, masterpiece, fantasy art, character art, book cover art, cinematic, professional, high quality, 4k, 8k, sharp focus, magazine cover, dramatic lighting, hollywood, premium, polished, glossy, hd, hdr, modern, photorealistic in the modern sense, dslr, smooth skin, beautiful, depth of field, bokeh, color grading, cinematic composition
```

### 3. Reference live-action shows by name

Add to the end of the prompt:

```
visual style of Hercules: The Legendary Journeys 1995, Xena Warrior Princess, Charmed season 1, late-night Cinemax fantasy show, recorded from a CRT television
```

These are real productions SDXL has training data for. Naming them forces live-action mode.

### 4. Don't say "painting" anywhere in the positive prompt

Re-check your prompt for words like `painted matte starfield backdrop`. SDXL latches onto `painted` and turns the whole thing into a painting. Rewrite as `printed paper starfield backdrop` or `glittery starfield backdrop tacked to the wall`.

### 5. If still painterly, switch models

Try `fal-ai/stable-diffusion-v15` instead of fast-sdxl. SD 1.5 is older, less RLHF'd, and produces grungy live-action-looking outputs more reliably than SDXL.

### 6. Or add a real-photo LoRA

On Civitai search for `analog photo`, `35mm film`, `90s film photography`, or `Hercules Xena`. These LoRAs force live-action mode even with fantasy prompts. Use scale `1.0`.

---

## Notes

- Don't crank steps. More steps = cleaner. `20` to `30` is the sweet spot.
- Smaller resolution naturally looks worse. Lean into it.
- Roll 4 images per prompt, pick the best, reuse the seed.
