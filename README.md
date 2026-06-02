# forgerender

The forge **render contract**. Holds `ChartSpec` and its element dataclasses —
the universal, JSON-serializable, theme-neutral specification that solvers
*emit* and renderers *consume*.

This is NOT the renderer. The `render()` dispatcher, SVG/Plotly renderers,
chart builders, and themes live in `forgeviz`. `forgerender` is upstream of
all of them: it is the shared schema both producers and consumers agree on.

Zero third-party dependencies — a solver can import it without pulling in
anything heavy.
