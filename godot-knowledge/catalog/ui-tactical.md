# Tactical UI (legibility)
_Control nodes & containers, the Theme system, the legibility-critical HUD (shown outcomes, loot panels, collateral indicator, range/AP), tooltips, responsive layout._ · wave 7 · 2026-09-07 · [‹ catalog index](README.md)

26 recipes · 8 solid.

| Recipe | Godot | Currency | ✓ | What |
|--------|-------|----------|---|------|
| Build the HUD skeleton with nested Containers + size flags (never hand-place tactical UI) | 4.x (all 4.0–4.6) | ✅ solid | ✓ | Compose the tactical HUD from Container nodes that own their children's geometry |
| Centralize all HUD styling in ONE Theme resource assigned at the root Control | 4.x (all 4.0–4.6) | ✅ solid | ✓ | Author a single `.tres` Theme resource (StyleBoxes, Colors, Fonts, font_sizes, C |
| Decouple combat state from HUD with custom signals (typed, parameterized) | 4.x (4.0+; `Signal.emit()` / `Signal.connect(Callable)` are the current 4.x forms) | ✅ solid | ✓ | Have combat/unit logic emit typed custom signals (e.g. `health_changed(hp, max_h |
| Draw range / threat / collateral overlays with _draw() + queue_redraw() (cached, event-driven) | 4.x (4.0+; `queue_redraw()` replaces Godot-3 `update()`; signatures current 4.4) | ✅ solid | ✓ | For the grid overlays that the HUD implies — movement/attack range tint, line-of |
| Drive HUD panels from custom Resources with a setter + emit_changed (reactive, data-first) | 4.x (4.0+; `@export`/`emit_changed`/`changed` are current 4.x API) | ✅ solid | ✓ | Model combat-UI data (a part definition, a unit's AP/HP block, a called-shot res |
| Encode semantic UI states as Theme Type Variations (DangerButton, DisabledChipPanel, CollateralLabel) | 4.x (4.0+; documented 4.3/4.4/4.6) | ✅ solid | ✓ | Theme Type Variations let you define named variants that extend a base type (e.g |
| Lock UI legibility across resolutions with stretch_mode = canvas_items + a base size | 4.x (4.0+; note a reported canvas_items scaling regression in 4.4 — verify on your pinned 4.x and test fullscreen) | ✅ solid | ✓ | Configure Project Settings → Display → Window so the whole 2.5D game + UI scales |
| Render shown outcomes as BBCode in a RichTextLabel (color-coded, append_text not +=) | 4.x (4.0+; `bbcode_enabled`, `append_text`, `push_*`, `meta_clicked` all current) | ✅ solid | ✓ | Use a RichTextLabel with `bbcode_enabled = true` to render multi-color, multi-st |
| Control class `_make_custom_tooltip` (id 42 URL) | 4.x | ⚠ shaky | · | **On page:** virtual `_make_custom_tooltip(for_text)` returns a Control (PopupPa |
| Covariant return type | 4.x | ⚠ shaky | · | Analog: override may return a narrower type. Holds for `_make_custom_tooltip` →  |
| Coverage.py excluding code | 4.x | ⚠ shaky | · | Report Stmts/Miss/Cover; exclusions only via explicit pragma — holds for catalog |
| Dashboard Design Patterns | 4.x | ⚠ shaky | · | Detail-on-demand (47% of surveyed dashboards) shows extra content on mouseover v |
| Flowy: Supporting UX Design Decisions Through AI-Driven Pattern Annotation in Multi-Screen User Flows | 4.x | ⚠ shaky | · | Overview→hover popup summaries→click details-on-demand (Visual Information-Seeki |
| GAM Coach: Towards Interactive and User-centered Algorithmic Recourse | 4.x | ⚠ shaky | · | Progressive disclosure: collapsed cards; hover feature name → tooltip definition |
| Keep a Changelog 1.1.0 | 4.x | ⚠ shaky | · | Inconsistent changelog as dangerous as none — holds for README Status matching c |
| Override _make_custom_tooltip() to show full deterministic breakdowns on hover | 4.x (4.0+; signature returns Control, formerly returned Object) | ⚠ shaky | ✓ | Replace Godot's plain-text tooltip with a designed Control (a styled panel + Ric |
| Progressive Disclosure | 4.x | ⚠ shaky | · | Analog: defer rare detail to a secondary reveal. Holds for recipe 42 tooltip cra |
| SPDX Package verification code / NOASSERTION | 4.x | ⚠ shaky | · | NOASSERTION when not determined — holds for default verified=0 / do-not-assert l |
| SPEC Fair Use Rules | 4.x | ⚠ shaky | · | Non-compliant vs compliant must not mislead — holds for README 88/155 verified-r |
| Semantic Versioning 2.0.0 | 4.x | ⚠ shaky | · | Released contents MUST NOT be modified — holds for do-not-flip verified on recip |
| Timing Guidelines for Exposing Hidden Content | 4.x | ⚠ shaky | · | Analog: hover/click reveal needs intent delay (avoid accidental show). Holds for |
| pytest skip and xfail | 4.x | ⚠ shaky | · | skip/xfail counted separately; xfail does not become pass — holds for 37/42/49 s |
| Covariant return type — Control tooltip analog | 4.x |  | ✓ | Analog: override may return a narrower type; callers still see the declared type |
| Liskov substitution — tooltip contract analog | 4.x |  | ✓ | Analog: return types must be covariant. Holds as the reason a bare Object that i |
| NN/g progressive disclosure — tooltip analog | 4.x |  | ✓ | Analog: HCI — defer detail to secondary reveal. Holds for recipe 42 tooltip craf |
| NN/g timing guidelines — hover reveal analog | 4.x |  | ✓ | Analog: HCI hover timing (0.3–0.5 s intent). Holds for tactical tooltip reveal p |

## Detail

### Build the HUD skeleton with nested Containers + size flags (never hand-place tactical UI) · `✅ solid` · Godot 4.x (all 4.0–4.6)
**Compose the tactical HUD from Container nodes that own their children's geometry, instead of anchoring/positioning Controls manually. Godot 4 provides HBoxContainer, VBoxContainer, GridContainer, MarginContainer, PanelContainer, ScrollContainer, HFlowContainer/VFlowContainer (wrapping), CenterContainer, AspectRatioContainer, TabContainer, and SplitContainer. Children inside a Container cannot set their own position/anchors — the parent drives layout; you steer it with size flags.**
- **How:** Wrap the action bar in an HBoxContainer, the unit/squad column in a VBoxContainer, pad anything with MarginContainer (set theme constants margin_left/top/right/bottom), and give every panel a PanelContainer so its StyleBox auto-sizes to content. Control children inside a container respond to two properties: `size_flags_horizontal` / `size_flags_vertical` (flags: SIZE_FILL default, SIZE_EXPAND to claim leftover space, SIZE_SHRINK_BEGIN/CENTER/END for alignment, SIZE_EXPAND_FILL = fill+expand) and `size_flags_stretch_ratio` (float) to split shared expand space — ratio 2.0 takes double the space of 1.0. Set a `custom_minimum_size` (Vector2) on any panel that must never collapse below a legible size (this is the Godot-4 name; the Godot-3 `rect_min_size` is GONE). For the loot-part grid use a GridContainer with `columns` set, or an HFlowContainer if part chips should wrap to a new row when the panel narrows.
- **Gotchas:** A Control placed as a direct child of a Container ignores its own anchors/offsets — if you anchor-position something and it 'snaps back', it's inside a container; move it out or use a plain Control/MarginContainer wrapper. SIZE_EXPAND with no FILL leaves a gap; you almost always want SIZE_EXPAND_FILL. Deeply nested containers re-sort on every resize — keep nesting shallow for the per-frame HUD.
- **Verify (solid):** Verified vs stable docs: Container children give up positioning, all named containers (HBox/VBox/Grid/Margin/Panel/Scroll/HFlow/VFlow/Center/AspectRatio/Tab/Split) are current 4.x nodes, size_flags + stretch_ratio steer them, and custom_minimum_size is correctly flagged as the 4.x name replacing Godot-3 rect_min_size. [SIZE_EXPAND/FILL/SHRINK_BEGIN/CENTER/END/EXPAND_FILL, custom_minimum_size and size_flags_stretch_ratio all confirmed matching class_control.html descriptions exactly.]
- **Sources:** [Using Containers — Godot Engine (stable) docs](https://docs.godotengine.org/en/stable/tutorials/ui/gui_containers.html) ; [Size and anchors — Godot Engine (stable) docs](https://docs.godotengine.org/en/stable/tutorials/ui/size_and_anchors.html) ; [Control class reference — Godot Engine (stable)](https://docs.godotengine.org/en/stable/classes/class_control.html) ; [Responsive UI Design in Godot: Anchors, Size Flags — Wayline](https://www.wayline.io/blog/responsive-ui-design-godot-anchors-size-flags)

### Centralize all HUD styling in ONE Theme resource assigned at the root Control · `✅ solid` · Godot 4.x (all 4.0–4.6)
**Author a single `.tres` Theme resource (StyleBoxes, Colors, Fonts, font_sizes, Constants, Icons) and assign it to the root Control's `theme` property. Every descendant Control inherits from the nearest ancestor that has a Theme, so one assignment styles the whole tactical UI consistently and data-drivenly.**
- **How:** Open the Theme editor (bottom panel when a Theme `.tres` is selected), add types (Button, Label, PanelContainer, RichTextLabel…) and set their StyleBox/Color/Font/font_size/constant items. Save as e.g. `hud_theme.tres`, then set it on the root Control node's Theme property in the Inspector. At runtime you can hot-swap the whole look with `control.theme = load("res://ui/hud_theme.tres")`. KEY DISTINCTION: a Theme **resource** propagates and is inherited; a **theme override** (the per-node 'Add item override' you set in the Inspector or via `add_theme_color_override()` / `add_theme_stylebox_override()`) is LOCAL to that one node — it does NOT propagate to children and children never see a parent's override. So broad look = Theme resource; one-off tweak = override.
- **Gotchas:** If a child panel 'won't pick up' the parent's styling, you almost certainly set an override on the parent instead of editing the Theme resource — overrides don't inherit. StyleBoxEmpty is the explicit 'draw nothing' box; don't leave a panel with a default StyleBoxFlat if you want it transparent. Theme font_size lives as a theme constant/font_size per type, not on the Font resource itself.
- **Verify (solid):** Confirmed: a Theme resource on a Control propagates to all direct/indirect children per class_theme docs; add_theme_color_override/add_theme_stylebox_override are current 4.x methods and are per-node (do not propagate). Theme editor workflow and StyleBoxEmpty all accurate. [Theme-resource-propagates vs override-is-local-and-does-not-propagate confirmed against current Godot theme behavior and class_theme.html's type-variation mechanics.]
- **Sources:** [Theme class reference — Godot Engine (stable)](https://docs.godotengine.org/en/stable/classes/class_theme.html) ; [Using the theme editor — Godot Engine (stable) docs](https://docs.godotengine.org/en/stable/tutorials/ui/gui_using_theme_editor.html) ; [Fix: Godot Theme Override Not Applying to Child Controls — Bugnet](https://bugnet.io/blog/fix-godot-theme-override-not-applying) ; [StyleBox class reference — Godot Engine (stable)](https://docs.godotengine.org/en/stable/classes/class_stylebox.html)

### Decouple combat state from HUD with custom signals (typed, parameterized) · `✅ solid` · Godot 4.x (4.0+; `Signal.emit()` / `Signal.connect(Callable)` are the current 4.x forms)
**Have combat/unit logic emit typed custom signals (e.g. `health_changed(hp, max_hp)`, `ap_changed(ap, max_ap)`, `shot_resolved(resolution)`, `collateral_risk_changed(level)`); HUD widgets connect and update themselves. The emitter doesn't know the HUD exists — the decoupling is the point and keeps the shown-everything UI maintainable.**
- **How:** Declare `signal health_changed(current: int, maximum: int)` on the unit script and `emit_signal("health_changed", hp, max_hp)` (or `health_changed.emit(hp, max_hp)`) whenever it changes. In the HUD: `unit.health_changed.connect(_on_health_changed)` and `func _on_health_changed(cur, max): bar.max_value = max; bar.value = cur`. Pass BOTH current and max so the widget is self-sufficient. For app-wide events (turn start, selection change) use an autoload 'event bus' singleton that re-emits; for direct parent↔child stay with local signals. This is the idiomatic Godot-4 alternative to the panel polling state every frame.
- **Gotchas:** Connect once (e.g. in `_ready` or on bind) — reconnecting on every turn duplicates handlers and the bar updates N times. Use `CONNECT_ONE_SHOT` for one-time events. Prefer the typed `signal.connect(callable)` over string-based `connect("name",...)` for compile-time safety. An over-used global event bus can become a hidden-coupling soup — keep gameplay-local signals local.
- **Verify (solid):** signal x.emit(...) and signal.connect(Callable) are the current 4.x forms (over string-based connect); typed signal params, CONNECT_ONE_SHOT, autoload event-bus pattern, and the connect-once gotcha are all correct idiomatic Godot 4. [Typed signal declarations, .emit()/.connect(callable) idiom, and the CONNECT_ONE_SHOT flag ('one-shot connections disconnect themselves after emission') all confirmed on class_object.html.]
- **Sources:** [Best practices with Godot signals — GDQuest](https://www.gdquest.com/tutorial/godot/best-practices/signals/) ; [Node communication (the right way) — Godot 4 Recipes (KidsCanCode)](https://kidscancode.org/godot_recipes/4.x/basics/node_communication/index.html) ; [Godot Signals Architecture: Best Practices & Event Bus — Febucci](https://blog.febucci.com/2024/12/godot-signals-architecture/)

### Draw range / threat / collateral overlays with _draw() + queue_redraw() (cached, event-driven) · `✅ solid` · Godot 4.x (4.0+; `queue_redraw()` replaces Godot-3 `update()`; signatures current 4.4)
**For the grid overlays that the HUD implies — movement/attack range tint, line-of-fire, collateral splash radius — override `_draw()` on a CanvasItem (Control or Node2D) and issue primitive draw commands. Draws are cached after one call; you refresh only when state changes by calling `queue_redraw()`.**
- **How:** Override `_draw()` and use the CanvasItem primitives: `draw_rect(Rect2, Color, filled=true, width=-1.0)` for tinting/outlining cells (pass `filled=false` + width for an outline; shift coords by 0.5 for odd widths), `draw_line(from, to, Color, width, antialiased)` for line-of-fire, `draw_circle(center, radius, Color)` or `draw_arc(...)` for splash/collateral radius, `draw_polyline`/`draw_colored_polygon` for AOE footprints, and `draw_string(font, pos, text, h_align, width, font_size)` for in-grid AP/damage numerals. `_draw()` runs once then caches — call `queue_redraw()` from your setter or input handler when the hovered cell / selected ability changes (NOT every frame unless animating). Use a Color with alpha for translucent tints so the painterly sprite underneath still reads.
- **Gotchas:** Godot-3 muscle memory: the redraw call is `queue_redraw()`, NOT `update()` — `update()` was repurposed/removed for this. Calling `queue_redraw()` every `_process` frame for a static overlay wastes the cache benefit. `draw_*` only works inside `_draw()` (or via the lower-level RenderingServer); calling them elsewhere does nothing. For odd-width strokes, offset by 0.5px or lines look blurry/off-center.
- **Verify (solid):** queue_redraw() correctly flagged as the 4.x replacement for Godot-3 update() (confirmed in class_canvasitem). draw_rect/draw_line/draw_circle/draw_arc/draw_string all current. Minor: current draw_circle signature now also takes filled/width params (draw_circle(pos,radius,color,filled=true,width=-1,...)) — the 3-arg filled form shown is still valid as the default. Caching + event-driven redraw guidance is accurate. [_draw()/queue_redraw() and draw_rect/draw_line/draw_circle/draw_string signatures confirmed on class_canvasitem.html. No update() method exists on CanvasItem, matching the gotcha exactly.]
- **Sources:** [Custom drawing in 2D — Godot Engine (4.4) docs](https://docs.godotengine.org/en/4.4/tutorials/2d/custom_drawing_in_2d.html) ; [CanvasItem class reference (draw_* methods) — Godot Engine (stable)](https://docs.godotengine.org/en/stable/classes/class_canvasitem.html) ; [godot-docs source: custom_drawing_in_2d.rst](https://github.com/godotengine/godot-docs/blob/master/tutorials/2d/custom_drawing_in_2d.rst)

### Drive HUD panels from custom Resources with a setter + emit_changed (reactive, data-first) · `✅ solid` · Godot 4.x (4.0+; `@export`/`emit_changed`/`changed` are current 4.x API)
**Model combat-UI data (a part definition, a unit's AP/HP block, a called-shot resolution) as custom `Resource` scripts with `class_name` and `@export` fields saved as `.tres`. A panel script holds that resource and rebuilds its widgets whenever the resource's `changed` signal fires — UI updates follow data, with no tight node coupling.**
- **How:** Define `class_name PartDef extends Resource` (or `UnitState`, `ShotResolution`) with `@export var name: String`, `@export var disable_chance: int`, etc. Author instances via FileSystem → right-click → New Resource → pick the class → save `.tres`; edit fields in the Inspector. To make the panel reactive, give mutable fields a setter that calls `emit_changed()` — custom Resources do NOT auto-emit `changed` (built-ins do), so you must: `@export var hp: int: set(v): if v != hp: hp = v; emit_changed()`. In the panel: `func bind(res): if data: data.changed.disconnect(_refresh); data = res; data.changed.connect(_refresh); _refresh()`, and `_refresh()` reads `data` and sets labels/bars. The crew authors content as `.tres`; the panel is generic.
- **Gotchas:** Without the setter, mutating a custom-Resource field NEVER fires `changed` and the panel goes stale — this is the #1 reported gotcha. Always `disconnect` the old resource before binding a new one or you leak stale connections (use `is_connected`/`disconnect`). `.tres` resources can be shared instances — duplicate() if a panel must edit its own copy without mutating the shared asset.
- **Verify (solid):** Core gotcha is correct and is the #1 reported issue: custom Resources do NOT auto-emit `changed` (built-ins do), so a setter calling emit_changed() is required (godot#30179, proposal#10720). @export, class_name,.tres authoring, and disconnect-before-rebind all current and idiomatic. [class_resource.html confirms near word-for-word: 'This signal is not emitted automatically for properties of custom resources... a setter needs to be created to emit the signal', matching example code pattern.]
- **Sources:** [Resource-based architecture for Godot 4 — Mayke F. dos Santos (Medium)](https://medium.com/@sfmayke/resource-based-architecture-for-godot-4-25bd4b2d9018) ; [Custom Resource not emitting emit_changed on set — Godot Forum](https://forum.godotengine.org/t/custom-resource-not-emitting-emit-changed-on-set-value/63643) ; [Godot 4 Custom Resources Tutorial — Coding Quests](https://codingquests.io/blog/godot-4-custom-resources-tutorial) ; [Creating and Using Custom Resources (Data-Driven Design) — UhiyamaLab](https://uhiyama-lab.com/en/notes/godot/custom-resource-data-driven/)

### Encode semantic UI states as Theme Type Variations (DangerButton, DisabledChipPanel, CollateralLabel) · `✅ solid` · Godot 4.x (4.0+; documented 4.3/4.4/4.6)
**Theme Type Variations let you define named variants that extend a base type (e.g. a `DangerButton` that IS a Button but overrides bg color + font color). You then set a Control's `theme_type_variation` (StringName) to that name and it gets base styling plus the variant's overrides — without per-node overrides or subclassing.**
- **How:** In the Theme editor, click the '+' next to the Type dropdown, name the variation (e.g. `LootChip`, `CollateralWarn`, `APCostLabel`), set its base type, and override only the items that differ (font_color, StyleBox, font_size). On the Control, set the `Theme Type Variation` field in the Inspector (or `node.theme_type_variation = &"CollateralWarn"` in code). The control composites base + variation, variation winning on conflicts and able to add items the base never defined.
- **Gotchas:** Variation name is a StringName — typos silently fall back to base type with no error. Variations live inside the Theme resource, so the node must still inherit that Theme (root assignment from Recipe 2). They extend exactly one base type; you can't multi-inherit variations.
- **Verify (solid):** Theme type variations confirmed as current 4.x feature; theme_type_variation is a StringName property on Control (verified in class_control), editor '+ base type' workflow matches docs, and silent fallback-to-base on a bad name is the documented/observed behavior. [Theme.set_type_variation(theme_type, base_type), chaining of variations, and the one-base-type-per-variation limit all confirmed on class_theme.html.]
- **Sources:** [Theme type variations — Godot Engine (stable) docs](https://docs.godotengine.org/en/stable/tutorials/ui/gui_theme_type_variations.html) ; [godot-docs source: gui_theme_type_variations.rst](https://github.com/godotengine/godot-docs/blob/master/tutorials/ui/gui_theme_type_variations.rst)

### Lock UI legibility across resolutions with stretch_mode = canvas_items + a base size · `✅ solid` · Godot 4.x (4.0+; note a reported canvas_items scaling regression in 4.4 — verify on your pinned 4.x and test fullscreen)
**Configure Project Settings → Display → Window so the whole 2.5D game + UI scales crisply from one authored base resolution, instead of the HUD rendering tiny on 4K or clipping on ultrawide. Set a base Viewport size, stretch Mode = `canvas_items`, and an Aspect.**
- **How:** Project Settings → Display → Window → Size: set `Viewport Width/Height` to your design base (e.g. 1920×1080 for painterly 2.5D, or 640×360 for a pixel base), and a larger `Window Width/Height Override` for the actual window. Under Stretch: Mode = `canvas_items` (scales all CanvasItems — sprites + UI — relative to base, crisp UI), Aspect = `keep` (letterbox, no distortion) or `expand` (show more world on wide screens; design the HUD with anchors/containers so edge panels reflow). For a pixel-art base add Scale Mode = `integer` to avoid shimmer. These can also be set at runtime via the Window/Viewport content-scale properties. Combine with Recipe 1 containers + `custom_minimum_size` so panels never collapse below readable size even under `expand`.
- **Gotchas:** A documented regression: `canvas_items` scaling reportedly misbehaves in Godot 4.4 where 4.3 worked — pin your engine version and test fullscreen + windowed before committing. `expand` aspect reveals more screen edge, so anchor/contain edge HUD or it drifts; `keep` letterboxes instead. Don't mix integer scale mode with a non-pixel base or you forfeit smooth scaling. Verify on the actual target, not just the editor viewport.
- **Verify (solid):** Project Settings > Display > Window stretch Mode=canvas_items (correctly noted as formerly '2d'), Aspect keep/expand, integer scale mode for pixel bases — all current 4.x. The flagged 4.4 canvas_items scaling regression (works in 4.3) is real and well-sourced (Godot forum thread + multiple GitHub issues incl. cross-DPI #111271); the 'pin your version and test fullscreen' caveat is sound. [stretch Mode canvas_items and Aspect keep/expand confirmed on multiple_resolutions.html. The 'documented regression in 4.4 vs 4.3' matches an actual Godot forum thread titled almost identically.]
- **Sources:** [Multiple resolutions / stretch mode — Godot Engine (stable) docs](https://docs.godotengine.org/en/stable/tutorials/rendering/multiple_resolutions.html) ; [How to Fix Godot Screen Resolution and Stretch Problems — Bugnet](https://bugnet.io/blog/how-to-fix-godot-screen-resolution-stretch-mode) ; [Canvas Items Scaling Mode Broken in Godot 4.4 (works in 4.3) — Godot Forum](https://forum.godotengine.org/t/canvas-items-scaling-mode-broken-in-godot-4-4-works-in-4-3/105205)

### Render shown outcomes as BBCode in a RichTextLabel (color-coded, append_text not +=) · `✅ solid` · Godot 4.x (4.0+; `bbcode_enabled`, `append_text`, `push_*`, `meta_clicked` all current)
**Use a RichTextLabel with `bbcode_enabled = true` to render multi-color, multi-style outcome text — disable %, damage breakdown, status icons inline — so the deterministic result is readable at a glance rather than a flat label string.**
- **How:** Set `bbcode_enabled = true`, then either write BBCode (`[color=#ff5555]DISABLE 100%[/color] [color=#aaa]−2 AP[/color]`) or build programmatically with `push_color(Color)` / `push_bold()` / `append_text(...)` / `pop()`. CRITICAL performance rule: append with `append_text("...")`, which only parses the new fragment — do NOT use `+= text` or reassign `.text`, which re-parses the whole buffer and erases any `push_*` formatting. Inline sprites via `[img]res://icon.png[/img]`; clickable refs via `[url=part_id]...[/url]` handled through the `meta_clicked` signal (and `meta_hover_started` for hover). Use `[lb]`/`[rb]` to print literal brackets so dynamic strings can't inject BBCode.
- **Gotchas:** Using `+=` or setting `.text` on a bbcode label nukes all prior push_* formatting and is slow — always `append_text`. `[img]` without a fixed width can blow up line height; size it. `meta` tags only do something if you connect `meta_clicked`. Forgetting to escape player/enemy names that contain '[' can break the parse — use `[lb]`/`[rb]`.
- **Verify (solid):** Verified verbatim against bbcode_in_richtextlabel docs: docs explicitly recommend append_text() over the text property for performance (only parses the new fragment); push_color/push_bold/pop, meta_clicked, [lb]/[rb] escapes, and [img] are all current 4.x. tooltip_text is correctly the 4.x name. [class_richtextlabel.html confirms near-verbatim: '+=' is 'unadvised... replaces the whole text and can cause slowdowns... will also erase all BBCode added to stack using push_* methods'; append_text()/push_color() confirmed.]
- **Sources:** [BBCode in RichTextLabel — Godot Engine (stable) docs](https://docs.godotengine.org/en/stable/tutorials/ui/bbcode_in_richtextlabel.html) ; [godot-docs source: bbcode_in_richtextlabel.rst](https://github.com/godotengine/godot-docs/blob/master/tutorials/ui/bbcode_in_richtextlabel.rst)

### Control class `_make_custom_tooltip` (id 42 URL) · `⚠ shaky` · Godot 4.x
****On page:** virtual `_make_custom_tooltip(for_text)` returns a Control (PopupPanel + contents); default tooltip is PopupPanel+Label; theming via TooltipPanel/TooltipLabel; example uses Label or scene instance. **Mismatch risk:** page does not prescribe “deterministic breakdowns” or require RichTextLabel — those are recipe invent beyond the API surface. Method exists → keep verified=0 until claim trimmed.**
- **How:** URL-open / official support deepen; 37/42/49 verified=0 stays.
- **Gotchas:** STUDY-044 deepen note.
- **Verify (shaky):** STUDY-044 deepen; default unverified [no external verdict — not checked]
- **Sources:** [Control class `_make_custom_tooltip` (id 42 URL)](https://docs.godotengine.org/en/stable/classes/class_control.html) — **On page:** virtual `_make_custom_tooltip(for_text)` returns a Control (PopupPanel + contents); default tooltip is PopupPanel+Label; theming via TooltipPanel/TooltipLabel; example uses Label or scene

### Covariant return type · `⚠ shaky` · Godot 4.x
**Analog: override may return a narrower type. Holds for `_make_custom_tooltip` → Control (not bare Object) on recipe 42. Limit: type rule ≠ visual layout of the panel.**
- **How:** Adjacent analog hold-with-limit
- **Gotchas:** STUDY-044 deepen note.
- **Verify (shaky):** STUDY-044 deepen; default unverified [no external verdict — not checked]
- **Sources:** [Covariant return type](https://en.wikipedia.org/wiki/Covariant_return_type) — Analog: override may return a narrower type. Holds for `_make_custom_tooltip` → Control (not bare Object) on recipe 42. Limit: type rule ≠ visual layout of the panel.

### Coverage.py excluding code · `⚠ shaky` · Godot 4.x
**Report Stmts/Miss/Cover; exclusions only via explicit pragma — holds for catalog vs README count honesty aligned with godot.db.**
- **How:** Catalog/README count honesty deepen
- **Gotchas:** STUDY-065.
- **Verify (shaky):** STUDY-065; default unverified [no external verdict — not checked]
- **Sources:** [Coverage.py excluding code](https://coverage.readthedocs.io/en/latest/excluding.html) — Report Stmts/Miss/Cover; exclusions only via explicit pragma — holds for catalog vs README count honesty aligned with godot.db.

### Dashboard Design Patterns · `⚠ shaky` · Godot 4.x
**Detail-on-demand (47% of surveyed dashboards) shows extra content on mouseover via tooltips/pop-ups — progressive secondary reveal for recipe 42 custom tooltip craft.**
- **How:** Literature deepen for leftover 37/42/49; no verified flip.
- **Gotchas:** STUDY-044 deepen note.
- **Verify (shaky):** STUDY-044 deepen; default unverified [no external verdict — not checked]
- **Sources:** [Dashboard Design Patterns](https://arxiv.org/abs/2205.00757) — Detail-on-demand (47% of surveyed dashboards) shows extra content on mouseover via tooltips/pop-ups — progressive secondary reveal for recipe 42 custom tooltip craft.

### Flowy: Supporting UX Design Decisions Through AI-Driven Pattern Annotation in Multi-Screen User Flows · `⚠ shaky` · Godot 4.x
**Overview→hover popup summaries→click details-on-demand (Visual Information-Seeking Mantra) — multi-step hover disclosure for recipe 42.**
- **How:** Literature deepen for leftover 37/42/49; no verified flip.
- **Gotchas:** STUDY-044 deepen note.
- **Verify (shaky):** STUDY-044 deepen; default unverified [no external verdict — not checked]
- **Sources:** [Flowy: Supporting UX Design Decisions Through AI-Driven Pattern Annotation in Mu](https://arxiv.org/abs/2406.16177) — Overview→hover popup summaries→click details-on-demand (Visual Information-Seeking Mantra) — multi-step hover disclosure for recipe 42.

### GAM Coach: Towards Interactive and User-centered Algorithmic Recourse · `⚠ shaky` · Godot 4.x
**Progressive disclosure: collapsed cards; hover feature name → tooltip definition; click reveals detail — hover disclosure pattern for recipe 42.**
- **How:** Literature deepen for leftover 37/42/49; no verified flip.
- **Gotchas:** STUDY-044 deepen note.
- **Verify (shaky):** STUDY-044 deepen; default unverified [no external verdict — not checked]
- **Sources:** [GAM Coach: Towards Interactive and User-centered Algorithmic Recourse](https://arxiv.org/abs/2302.14165) — Progressive disclosure: collapsed cards; hover feature name → tooltip definition; click reveals detail — hover disclosure pattern for recipe 42.

### Keep a Changelog 1.1.0 · `⚠ shaky` · Godot 4.x
**Inconsistent changelog as dangerous as none — holds for README Status matching catalog/DB 155 · 88/155 · 6 waves.**
- **How:** Catalog/README count honesty deepen
- **Gotchas:** STUDY-065.
- **Verify (shaky):** STUDY-065; default unverified [no external verdict — not checked]
- **Sources:** [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) — Inconsistent changelog as dangerous as none — holds for README Status matching catalog/DB 155 · 88/155 · 6 waves.

### Override _make_custom_tooltip() to show full deterministic breakdowns on hover · `⚠ shaky` · Godot 4.x (4.0+; signature returns Control, formerly returned Object)
**Replace Godot's plain-text tooltip with a designed Control (a styled panel + RichTextLabel) by overriding `_make_custom_tooltip(for_text: String) -> Object`. This lets a hovered target/part/ability surface its complete, formatted outcome math instead of a one-line string.**
- **How:** On a Control (or a small script you attach to many widgets), override: `func _make_custom_tooltip(for_text: String) -> Control: var t = preload("res://ui/shot_tooltip.tscn").instantiate(); t.populate(for_text); return t`. Godot auto-wraps the returned Control in a PopupPanel and draws that panel's StyleBox behind it. Feed structured data either by parsing `for_text` or (cleaner) by reading the hovered widget's bound Resource (Recipe 4) before returning. Set the trigger string via the node's `tooltip_text` property (the Godot-4 name; Godot-3 `hint_tooltip` is gone) — it must be non-empty for the tooltip to appear.
- **Gotchas:** The auto-added PopupPanel draws its own background ON TOP — to remove the default box, set the PopupPanel/tooltip StyleBox to StyleBoxEmpty (or theme it) or you get a double-background. Tooltip placement has known quirks (issue #39677). `tooltip_text` must be non-empty or the override never fires. Returning a node that's already in the tree throws — always instantiate a fresh one.
- **Verify (shaky):** CORRECTED: Issue #39677 ('Custom tooltip placement bug when using _make_custom_tooltip') is CLOSED/fixed, not an open current quirk. Placement bugs recurred later under separate numbers (e.g. #96721) — cite one of those if a currently-live quirk is needed. · _make_custom_tooltip signature/Object return and tooltip_text property confirmed on class_control.html. Cited issue #39677 is stale; see corrections. [research note: How-to (instantiate a Control scene, populate, return it; tooltip_text must be non-empty; PopupPanel draws its own StyleBox; use StyleBoxEmpty) is all correct. BUT the version note is INVERTED: current stable class_control declares `_make_custom_tooltip(for_text) -> Object` — it still returns Object (the returned node must be Control-derived), NOT 'returns Control, formerly Object'. Fix the note; the recipe itself works.]
- **Sources:** [Control._make_custom_tooltip — Godot Engine class reference](https://docs.godotengine.org/en/stable/classes/class_control.html) ; [Custom Tooltips with BBCode in Godot 4 — Godot Forum](https://forum.godotengine.org/t/custom-tooltips-with-bbcode-in-godot-4-video-tutorial/93047) ; [How to Remove Tooltip Background in Godot 4 (StyleBox fix) — Dre Dyson](https://dredyson.com/how-to-remove-tooltip-background-in-godot-4-a-complete-beginners-step-by-step-guide-to-custom-tooltip-panels-and-stylebox-fixes/)

### Progressive Disclosure · `⚠ shaky` · Godot 4.x
**Analog: defer rare detail to a secondary reveal. Holds for recipe 42 tooltip craft (`_make_custom_tooltip` → designed Control). Limit: UX pattern ≠ Godot Control return contract.**
- **How:** Adjacent analog hold-with-limit
- **Gotchas:** STUDY-044 deepen note.
- **Verify (shaky):** STUDY-044 deepen; default unverified [no external verdict — not checked]
- **Sources:** [Progressive Disclosure](https://www.nngroup.com/articles/progressive-disclosure/) — Analog: defer rare detail to a secondary reveal. Holds for recipe 42 tooltip craft (`_make_custom_tooltip` → designed Control). Limit: UX pattern ≠ Godot Control return contract.

### SPDX Package verification code / NOASSERTION · `⚠ shaky` · Godot 4.x
**NOASSERTION when not determined — holds for default verified=0 / do-not-assert leftovers until a real gate.**
- **How:** Catalog/README count honesty deepen
- **Gotchas:** STUDY-065.
- **Verify (shaky):** STUDY-065; default unverified [no external verdict — not checked]
- **Sources:** [SPDX Package verification code / NOASSERTION](https://spdx.github.io/spdx-spec/v2.3/package-information/) — NOASSERTION when not determined — holds for default verified=0 / do-not-assert leftovers until a real gate.

### SPEC Fair Use Rules · `⚠ shaky` · Godot 4.x
**Non-compliant vs compliant must not mislead — holds for README 88/155 verified-ratio honesty. Limit: SPEC ≠ recipe verified bit.**
- **How:** Catalog/README count honesty deepen
- **Gotchas:** STUDY-065.
- **Verify (shaky):** STUDY-065; default unverified [no external verdict — not checked]
- **Sources:** [SPEC Fair Use Rules](https://www.spec.org/fairuse.html) — Non-compliant vs compliant must not mislead — holds for README 88/155 verified-ratio honesty. Limit: SPEC ≠ recipe verified bit.

### Semantic Versioning 2.0.0 · `⚠ shaky` · Godot 4.x
**Released contents MUST NOT be modified — holds for do-not-flip verified on recipes 37/42/49. Limit: package ≠ recipe row.**
- **How:** Catalog/README count honesty deepen
- **Gotchas:** STUDY-065.
- **Verify (shaky):** STUDY-065; default unverified [no external verdict — not checked]
- **Sources:** [Semantic Versioning 2.0.0](https://semver.org/) — Released contents MUST NOT be modified — holds for do-not-flip verified on recipes 37/42/49. Limit: package ≠ recipe row.

### Timing Guidelines for Exposing Hidden Content · `⚠ shaky` · Godot 4.x
**Analog: hover/click reveal needs intent delay (avoid accidental show). Holds for tactical breakdown tooltip pacing on recipe 42. Limit: web timing heuristics ≠ Godot tooltip timer knobs.**
- **How:** Adjacent analog hold-with-limit
- **Gotchas:** STUDY-044 deepen note.
- **Verify (shaky):** STUDY-044 deepen; default unverified [no external verdict — not checked]
- **Sources:** [Timing Guidelines for Exposing Hidden Content](https://www.nngroup.com/articles/timing-exposing-content/) — Analog: hover/click reveal needs intent delay (avoid accidental show). Holds for tactical breakdown tooltip pacing on recipe 42. Limit: web timing heuristics ≠ Godot tooltip timer knobs.

### pytest skip and xfail · `⚠ shaky` · Godot 4.x
**skip/xfail counted separately; xfail does not become pass — holds for 37/42/49 stay verified=0.**
- **How:** Catalog/README count honesty deepen
- **Gotchas:** STUDY-065.
- **Verify (shaky):** STUDY-065; default unverified [no external verdict — not checked]
- **Sources:** [pytest skip and xfail](https://docs.pytest.org/en/stable/how-to/skipping.html) — skip/xfail counted separately; xfail does not become pass — holds for 37/42/49 stay verified=0.

### Covariant return type — Control tooltip analog · `?` · Godot 4.x
**Analog: override may return a narrower type; callers still see the declared type. Holds for recipe 42 (_make_custom_tooltip → Object but must be Control-derived).**
- **How:** See source URL; STUDY-002 Verifier-verified finding.
- **Verify ():** STUDY-012 from STUDY-002 Verifier ✅; default verified=0 [class_control.html: _make_custom_tooltip is declared 'virtual const' returning Object, while recommended overrides return Control (an Object subclass) — the covariant-return analogy holds. Entry embeds a verifier directive, noted only.]
- **Sources:** [Covariant return type — Control tooltip analog](https://en.wikipedia.org/wiki/Covariant_return_type) — Object→Control-derived

### Liskov substitution — tooltip contract analog · `?` · Godot 4.x
**Analog: return types must be covariant. Holds as the reason a bare Object that is not a Control breaks the tooltip contract; does not flip recipe 42.**
- **How:** See source URL; STUDY-002 Verifier-verified finding.
- **Verify ():** STUDY-012 from STUDY-002 Verifier ✅; default verified=0 [Same underlying fact as the covariant-return entry (Object-declared return, Control actually returned) supports the substitutability analogy. Entry embeds a verifier directive ('do not flip 37/42/49'), noted only.]
- **Sources:** [Liskov substitution — tooltip contract analog](https://en.wikipedia.org/wiki/Liskov_substitution_principle) — LSP

### NN/g progressive disclosure — tooltip analog · `?` · Godot 4.x
**Analog: HCI — defer detail to secondary reveal. Holds for recipe 42 tooltip craft; limit: UX pattern only — does not constrain Godot return type.**
- **How:** See source URL; STUDY-002 Verifier-verified finding.
- **Verify ():** STUDY-012 from STUDY-002 Verifier ✅; default verified=0 [NN/g's own definition ('show users only a few of the most important options... offer a larger set upon request') matches the entry's characterization. Entry embeds a verifier directive, noted only.]
- **Sources:** [NN/g progressive disclosure — tooltip analog](https://www.nngroup.com/articles/progressive-disclosure/) — tooltip craft analog

### NN/g timing guidelines — hover reveal analog · `?` · Godot 4.x
**Analog: HCI hover timing (0.3–0.5 s intent). Holds for tactical tooltip reveal pacing; limit: timing ≠ Godot Control return type.**
- **How:** See source URL; STUDY-002 Verifier-verified finding.
- **Verify ():** STUDY-012 from STUDY-002 Verifier ✅; default verified=0 [NN/g 'Timing Guidelines for Exposing Hidden Content' specifies a 300-500ms intent-confirmation hover delay, matching the '0.3-0.5 s' claim exactly. Entry embeds verifier directives, noted only.]
- **Sources:** [NN/g timing guidelines — hover reveal analog](https://www.nngroup.com/articles/timing-exposing-content/) — hover timing analog

