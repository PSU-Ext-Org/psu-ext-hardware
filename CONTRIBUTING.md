# Contributing

Thanks for helping improve PSU-EXT Hardware. This repository contains the
hardware design, enclosure, labels, and manufacturing outputs for an inline
bench-power-supply extension.

## Licence

The original design source is licensed under the
[CERN Open Hardware Licence Version 2 - Strongly Reciprocal](LICENCE)
(CERN-OHL-S v2). By submitting a pull request, patch, or other contribution,
you confirm that you have the right to submit it under that licence.

Bundled third-party assets are identified separately in
[THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md). Do not add, copy, or modify a
third-party library asset without recording its applicable licence, copyright,
and attribution.

## Developer Certificate of Origin (DCO)

This project uses the [Developer Certificate of Origin](https://developercertificate.org/)
(DCO), not a separate Contributor License Agreement. Every commit in a pull
request must include a `Signed-off-by` trailer, certifying that you wrote the
change or otherwise have the right to submit it.

Create signed-off commits with:

```text
git commit -s -m "Your commit message"
```

This adds a trailer such as:

```text
Signed-off-by: Your Name <your.email@example.com>
```

Use your real name and a reachable email address. To correct a missed sign-off,
use `git commit --amend -s` before opening or updating a pull request.

## Design files and generated outputs

Use the repository's recorded or compatible tool versions: **KiCad 10.0.1** for the PCB and
schematics, and **FreeCAD 1.1.1** for the enclosure.

When a KiCad project file changes, commit the corresponding generated outputs
in the same change:

- Re-export [`electronics/exports/schematic.pdf`](electronics/exports/schematic.pdf)
  when schematics change.
- Regenerate the applicable files in [`manufacturing/`](manufacturing/)—Gerbers,
  BOM, and/or CPL—when a PCB or manufacturing-relevant project change affects
  them.

When [`mechanical/enclosure/psu-ext-enclosure.FCStd`](mechanical/enclosure/psu-ext-enclosure.FCStd)
changes, re-export every affected `.3mf` model in
[`mechanical/enclosure/exports/`](mechanical/enclosure/exports/). Do not commit
editor lock files, backups, or local history directories.

## DEP-5 licence metadata

[`LICENSES/dep5`](LICENSES/dep5) is the authoritative, machine-readable record
of file copyright and licence metadata. Every newly tracked file must be added
to an appropriate `Files` block in the same pull request. If the file uses a
new licence or ownership category, also update
[`THIRD-PARTY-NOTICES.md`](THIRD-PARTY-NOTICES.md) when attribution is needed.

[`LICENSES/dep5.py`](LICENSES/dep5.py) is a small repository utility that lists
the available DEP-5 blocks, adds existing files to a block without changing its
legal metadata, creates a new licence section when necessary, and validates the
metadata against the checkout.

Run it from the repository root:

```text
python LICENSES/dep5.py list
python LICENSES/dep5.py validate
```

To add a project-owned file to the existing CERN-OHL-S block:

```text
python LICENSES/dep5.py add --section cern-ohl-s-2.0 --block original-source path/to/file
```

Use `create-section` only for a genuinely new licence section; it deliberately
does not alter existing legal declarations. Run `python LICENSES/dep5.py --help`
for its complete command reference.

## Before opening a pull request

- Use DCO-signed commits.
- Include required KiCad, FreeCAD, and manufacturing exports with their source
  changes.
- Add a dated, concise entry to [`CHANGES.txt`](CHANGES.txt) describing the
  changes in the pull request; do not remove earlier entries.
- Add all new tracked files to `LICENSES/dep5` and run
  `python LICENSES/dep5.py validate`.
- Review the diff for accidental generated backups, lock files, or unrelated
  design changes.
