# Rotate

> Rotates one image, or two images with the same settings, by a manual or preset angle.

**Category:** Preprocessing / Classical Computer Vision

**Status:** Experimental

**Last Updated:** 14.10.2026

---

## 1. Overview

This component rotates images with OpenCV (`cv2.getRotationMatrix2D` + `cv2.warpAffine`). It has two tasks (executors), selected from the **Task** dropdown:

- **Package** (`First`): rotates a single image.
- **Dual Rotate** (`Second`): rotates two images with the same rotation settings, e.g. a frame and its mask.

The rotation is configured in one of two modes:

- **Manual**: any integer angle in `[-359, 359]`, with a choice to keep the whole image (expand the canvas) or keep the original size (corners are cut off).
- **Preset**: a fixed 90° / 180° / 270° rotation with an optional scale factor. The canvas is always expanded, so nothing is cut off.

Positive angles rotate counterclockwise, negative angles rotate clockwise.

**Typical use cases:**

- Correcting the orientation of a camera mounted sideways or upside down.
- Aligning a tilted image before OCR, measurement or detection.
- Rotating an image together with its mask or depth map so they stay aligned.

---

## 2. Inputs

| Field Name | Kind/Type | Required | Default | Description |
|---|---|---|---|---|
| `inputImage` | `Image` (object) or `List[Image]` (list) | Yes | — | Image to rotate. Used by both tasks. |
| `inputImage2` | `Image` (object) or `List[Image]` (list) | Yes (Dual Rotate only) | — | Second image, rotated with the same settings as `inputImage`. |

> Derived from `FirstInputs` / `SecondInputs`. The `type` field is set to `object` for a single image and `list` for a list.

---

## 3. Configuration Parameters

**Mode** (`RotateMode`, `dependentDropdownlist`) chooses which of the parameters below are shown.

| Parameter | Type | Field Type (UI control) | Allowed Values / Range | Default | Description |
|---|---|---|---|---|---|
| `RotateMode` (Mode) | object | `dependentDropdownlist` | Manual, Preset | — | Selects manual or preset rotation. |
| `Degree` (Angle) — *Manual* | number (int) | `textInput` | `[-359, 359]` | `0` | Rotation angle in degrees. Positive = counterclockwise. |
| `KeepSide` (Keep Sides) — *Manual* | object (bool) | `dropdownlist` | Enable (`True`), Disable (`False`) | — | **Enable**: expands the canvas so the whole rotated image fits. **Disable**: keeps the original width/height; corners outside the frame are cut off. |
| `PresetAngle` (Preset Angle) — *Preset* | object (number) | `dropdownlist` | 90°, 180°, 270° | — | Fixed rotation angle, counterclockwise. |
| `Scale` — *Preset* | number (float) | `textInput` | `(0, 5]` | `1.0` | Scale factor applied while rotating. |

> Derived from `FirstConfigs` / `SecondConfigs`. Both tasks use the same parameters. `ConfigExecutor` is not included.

---

## 4. Outputs

| Field Name | Kind/Type | Description |
|---|---|---|
| `outputImage` | `Image` (object) or `List[Image]` (list) | Rotated `inputImage`. Returned by both tasks. |
| `outputImage2` | `Image` (object) or `List[Image]` (list) | Rotated `inputImage2`. Returned only by **Dual Rotate**. |

> Derived from `FirstOutputs` / `SecondOutputs`.

---

## 5. Use Case Examples

**Use case 1: Correcting a sideways camera**

A camera source package streams frames from a camera mounted at 90°. This package runs in **Package** task, **Preset** mode with 90° (or 270°), and turns the frames upright. A detection capsule after it receives correctly oriented images.

**Use case 2: Straightening a tilted document**

An image loader provides a scanned document that is slightly tilted. This package runs in **Manual** mode with a small angle (e.g. `-7`) and **Keep Sides: Enable** so no text is cut off. An OCR package then reads the straightened image.

**Use case 3: Rotating an image and its mask together**

A segmentation package outputs an image and its mask. **Dual Rotate** rotates both with the same settings so they stay pixel-aligned. Downstream packages that overlay the mask on the image receive matching outputs.

---

## 6. Limitations and Notes

- **Output size changes** when Keep Sides is enabled and always in Preset mode (e.g. 90°/270° swap width and height). Downstream packages should not assume the input resolution.
- Empty areas created by the rotation are filled with black (`warpAffine` default border).
- In **Manual** mode the scale is fixed at `1.0`. In **Preset** mode the canvas is always expanded.
- `Degree` accepts integers only.
- The models accept a list of images, but the executors pass the input directly to `Image.get_frame`; list inputs depend on SDK support and are not iterated in this package.
- Runs on CPU with OpenCV; no model weights are loaded (`bootstrap` returns an empty dict).
