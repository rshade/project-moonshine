# 💻 Software Roadmap: "The Automated Distiller"

This roadmap runs parallel to the hardware [ROADMAP.md](ROADMAP.md), focusing on the software infrastructure, simulation engine, and "Software-Defined Hardware" (SDH) tools.

## 🥅 Goals
1.  **Data-Driven Design:** Decouple physics parameters from code. Use YAML specs to drive simulations.
2.  **Generative Documentation:** Automatically generate diagrams (SVG/Mermaid) and BOMs from the YAML spec.
3.  **Reproducible Physics:** Ensure every simulation result is versioned and reproducible via CI/CD.

## 🚧 Phase 1: The Foundation (Current)
*   [x] **Structure:** Create `data/` directory and move hardcoded feedstock values to `data/feedstocks.yaml`.
*   [x] **Refactor:** Update `moonshine.impact` to load feedstocks dynamically.
*   [x] **Dependencies:** Add `PyYAML` to `pyproject.toml`.

## 🔮 Phase 2: Generative Diagrams
*   [ ] **The Spec:** Define `moonshine_v1.yaml` (Shaft length, gear ratios, materials).
*   [ ] **The Renderer:** Create a script to generate Mermaid/SVG diagrams from the spec.
*   [ ] **The Link:** Connect `moonshine-sim` to read from `moonshine_v1.yaml` instead of internal variables.

## 🧪 Phase 3: Continuous Physics
*   [ ] **CI/CD:** Run `test_gearbox_thermal.py` and `analyze_sourcing.py` in GitHub Actions.
*   [ ] **Regression Testing:** Fail the build if a design change reduces thermal efficiency below threshold.
