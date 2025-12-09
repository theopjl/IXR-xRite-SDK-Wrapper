# xRite i1Pro Test Results Report 🎯

**Date:** 2025-12-05  
**Tester:** tpjl-ujm  
**Device:** xRite i1Pro — Serial: 1022803  
**SDK (when reported):** 4.2.7.5976

---

📝 Executive summary
- ✅ Wrapper + SDK + hardware: functional and stable for the exercised modes.  
- ⚠️ Minor UX/resource issues: "Device already open" (Error 20) and sensor saturation (Error 1).  
- 🔬 Measurement integrity: Reflectance, ambient-light, and scanning tests are consistent and physically plausible.  
- 🔁 Repeatability: Good when same procedure is followed; low-light Y readings are near noise floor and can be slightly negative (small offset).

---

## Table of contents
1. Quick checklist ✅  
2. Observations & behavior notes 🧭  
3. Measurement details & deltas 📊  
4. Reflectance & ambient analyses 🌈  
5. Errors, UX and reliability ⚙️  
6. Recommendations & action items 🛠️  
7. Final verdict ⭐

---

## 1) Quick checklist ✅

	• Device enumeration (unplugged / plugged): OK ✅  
	• Calibration must be on white tile: OK ✅  
	• CLI invalid input handling: OK ✅  
	• Measurement loop (Ctrl+C): OK ✅  
	• Scan mode (device button): OK ✅  
	• Plotting & saving: OK ✅  
	• Reflectance verification (white tile ~90%): PASSED ✅

---

## 2) Observations & behavior notes 🧭

- LED status on device matches documented states:
	- Solid white → not calibrated (waiting)  
	- Blinking white → calibrated (ready)  
- Calibration only accepted on white tile — expected and correct.  
- When re-entering modes without closing device: Error 20 appears ("Device already open") — UX workaround exists but wrapper should manage resources.  
- Low-luminance Y measurements near zero show small negative values (e.g., -0.06 cd/m²) — treat as noise floor / baseline offset.

---

## 3) Measurement details & deltas 📊

### Simple repeated measurements (same patch/session)
Measured triplet (session 1):
- M1: x = 0.5936, y = 0.5230, Y = -0.06 cd/m²  
- M2: x = 0.5147, y = 0.4482, Y = -0.06 cd/m²  
- M3: x = 0.5219, y = 0.4351, Y = -0.05 cd/m²

Deltas:
- M1 ↔ M2: Δx = 0.0789, Δy = 0.0748, ΔY = 0.00 → large chromatic change → likely different patch/align.
- M2 ↔ M3: Δx = 0.0072, Δy = -0.0131, ΔY = +0.01 → good repeatability.
- M1 ↔ M3: Δx = 0.0717, Δy = 0.0879, ΔY = +0.01 → confirms M1 differs substantially.

Interpretation:
- M1 is inconsistent with M2/M3; suspect different measurement target or misalignment.
- M2/M3 are consistent — repeatability OK if procedure identical.
- Negative Y values (−0.05…−0.07 cd/m²) are within instrument noise at very low luminance — clamp/flag in UI.

---

### Multi-measurements (5 reads) — statistics
Reported Ys:
- -0.07, -0.02, -0.06, -0.05, -0.05

Reported summary:
- x: mean = 0.2943 (std = 0.0699)  
- y: mean = 0.3584 (std = 0.0377)  
- Y: mean = -0.05 cd/m² (std = 0.02)

Notes:
- Absolute std dev for Y is small (0.02 cd/m²); relative std is large because mean ≈ 0.
- For low-light, increase integration or averages to lower noise.

---

## 4) Reflectance & ambient analyses 🌈

### Reflectance results (selected)
- Example sample:
	- x = 0.4256, y = 0.2739, Y = 20.05%  
	- Spectral stats: Min = 9.10%, Max = 85.28%, Mean = 38.96%, Std = 27.49%

- White tile (verification):
	- x = 0.3488, y = 0.3621, Y = 89.76%  
	- Spectral: Min = 71.97%, Max = 91.25%, Mean = 88.08%, Std = 4.14%  
	- Verdict: Verification passed ✔️ (expected ~85–95%)

- White vs sample (pink):
	- White Y = 90.05% ; Sample Y = 20.08% → relative reflectance ≈ 22.3% → logical and consistent.

- White vs white sample:
	- White tile: 90.08% ; White sample: 88.08% → relative ≈ 97.8% → small difference, expected.

Interpretation:
- Reflectance mode: consistent, repeatable, and physically plausible.
- Spectra shapes align with color (pink → higher red-band; white tile → flat high reflectance).

---

### Ambient light (monitor white) — summary
Two measurements:
- A: 3579.7 lux — x=0.3078, y=0.3275, CCT ≈ 6792 K  
- B: 3713.6 lux — x=0.3067, y=0.3276, CCT ≈ 6853 K  

Δ:
- Δlux ≈ 133.9 lx (≈3.7%) — acceptable for repositioning/handheld
- ΔCCT ≈ 61 K (≈0.9%) — negligible

Spectral composition (example):
- Blue (380–480 nm): ~34.2%  
- Green (480–580 nm): ~43.2%  
- Red (580–730 nm): ~22.6%  
- Peak: ~460 nm → consistent with LED-backlit display

Conclusion:
- Ambient-light mode produces consistent, actionable values for lighting assessments.

---

## 5) Errors, UX, and reliability ⚙️

- Error 1 — Sensor saturated:
	- Trigger: measuring a too-bright sample immediately after white tile.
	- Behavior: SDK throws Error 1. Expected hardware limitation.
	- Mitigation: reduce brightness, add neutral density filter, or increase distance. Wrapper could auto-retry with reduced exposure.

- Error 20 — Device already open:
	- Trigger: re-entering a measurement mode without closing the previous context.
	- Behavior: UX workaround exists but code should fix.
	- Mitigation: ensure wrapper closes handles and supports safe re-open; provide friendly message.

- Negative Y at low-light:
	- Likely baseline/dark-current subtraction overshoot or noise.
	- Mitigation: clamp small negatives to 0 for presentation; allow raw/unbiased mode for debugging.

- Scan mode:
	- Scanned 1580 patches successfully; Y values consistent (4.09–4.52%) → trusted for high-throughput scans.

---

## 6) Recommendations & action items 🛠️

High priority:
- 🔧 Ensure wrapper properly closes device contexts (prevent Error 20).  
- 🔧 Catch saturation error and provide user guidance + optional auto-retry with reduced exposure.

Medium priority:
- 🧾 Clamp or flag small negative Y values in UI; expose option to view raw values.  
- ➕ Add automatic suggestions: "increase integration" for low-light, "reduce brightness" for saturation.

Low priority:
- ✨ Add optional wrapper-level Ra calculation (when applicable).  
- 📚 Expand documentation: error code table, measurement-mode tips, calibration requirements.

Testing suggestions:
- Repeatability matrix: n=10 runs at low/medium/high illuminance.  
- Saturation boundary detection test: measure white tile while progressively reducing neutral density until no saturation.  
- Resource cleanup test: enter/exit all modes sequentially to confirm no resource leak.

---

## 7) Final verdict ⭐

- Stability: **Excellent** (scan, reflectance, ambient, calibrations work reliably).  
- Accuracy: **Consistent & physically plausible** (white tile verification passed).  
- UX: **Good**, with two actionable improvements (saturation handling and safe reopen).  
- Production readiness: **Yes**, after small wrapper fixes for resource lifecycle and user-friendly error handling.

---

🔚 Appendix — Quick numeric summary

	• Serial: 1022803  
	• White tile (verification): Y ≈ 89.76% (Mean reflectance ≈ 88.08%, Std 4.14%)  
	• Sample (pink): Y ≈ 20.08% → relative ≈ 22.3% of white tile  
	• Ambient monitor white: 3579.7–3713.6 lux, CCT ≈ 6792–6853 K, peak ≈ 460 nm  
	• Low-light Y: mean ≈ -0.05 cd/m² (treat as noise floor)  
	• Scan: 1580 patches scanned; patch Y ~ 4.09–4.52%

---

If you want, I can now:
- ✅ Generate a condensed one-page PDF-friendly summary, or  
- 🧩 Provide code snippets for handling Error 1 (saturation) and Error 20 (device already open).  

Which would you like next?