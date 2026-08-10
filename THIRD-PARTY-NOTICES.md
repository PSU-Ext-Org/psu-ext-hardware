# Third-Party Notices

This document identifies library assets that are not licensed under CERN-OHL-S
v2. They remain under their stated licences. The PSU-EXT KiCad design that uses
these assets is licensed under CERN-OHL-S v2.

## OSHW gear-logo bundle

| Files | Copyright and source | Licence |
|---|---|---|
| `electronics/lib/external/footprints-oshw.pretty/logo_oshw_22x13.2mm.kicad_mod` | Macklin Chaffee, 2011. [Open Source Hardware Logo — OSHWA](https://oshwa.org/resources/open-source-hardware-logo/) | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) |

The OSHW gear logo may be used only for hardware that complies with the Open
Source Hardware Definition. It is not the OSHWA Certification Mark.

## SnapEDA / SnapMagic bundles

The four bundles below contain nine distributed SnapMagic Design Files: one
shared KiCad symbol-library file, four footprint files, and four STEP model
files. This repository must not add another SnapMagic Design File without prior
written permission from SnapMagic.

All listed SnapMagic Design Files are licensed under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) with the
[SnapMagic Design Exception 1.0](https://www.snapeda.com/about/terms/).
Attribution: SnapMagic Search and the applicable component manufacturer. The
Design Exception permits the combined PSU-EXT circuit-board design to be
conveyed under CERN-OHL-S v2; it does not relicense the library files.

| Bundle | Symbol | Footprint | 3D model | Source |
|---|---|---|---|---|
| Epson FC-135 32.7680KA-A0 | `electronics/lib/external/symbols-snapeda.kicad_sym` | `electronics/lib/external/footprints-snapeda.pretty/XTAL_FC-135_32.7680KA-A0.kicad_mod` | `electronics/lib/external/models-snapeda/FC-135_32.7680KA-A0.step` | <https://www.snapeda.com/parts/FC-135%2032.7680KA-A0/Epson/view-part/?ref=snap> |
| Hongfa HF49FD/005-1H12T | `electronics/lib/external/symbols-snapeda.kicad_sym` | `electronics/lib/external/footprints-snapeda.pretty/RELAY_HF49FD_005-1H12T.kicad_mod` | `electronics/lib/external/models-snapeda/005-1H12T-3DModel-STEP-56544.step` | <https://www.snapeda.com/parts/HF49FD/005-1H12T/Hongfa/view-part/?ref=snap> |
| RECOM RFM-0505S | `electronics/lib/external/symbols-snapeda.kicad_sym` | `electronics/lib/external/footprints-snapeda.pretty/CONV_RFM-0505S.kicad_mod` | `electronics/lib/external/models-snapeda/RFM-0505S.step` | <https://www.snapeda.com/parts/RFM-0505S/Recom+Power/view-part/?ref=snap> |
| HRO TYPE-C-31-M-12 | `electronics/lib/external/symbols-snapeda.kicad_sym` | `electronics/lib/external/footprints-snapeda.pretty/HRO_TYPE-C-31-M-12.kicad_mod` | `electronics/lib/external/models-snapeda/TYPE-C-31-M-12.step` | <https://www.snapeda.com/parts/TYPE-C-31-M-12/HRO+Electronics+Co.%252C+Ltd./view-part/?ref=snap> |

## MaxEELabs logo bundle

`electronics/lib/external/footprints-maxeelabs.pretty/logo_20x11.2mm.kicad_mod`
is original work of Maxim Pavlov and is excluded from CERN-OHL-S v2. It is
proprietary, with all rights reserved; no permission is granted to use, copy,
modify, distribute, or otherwise exploit the logo, subject only to rights that
cannot be excluded by law. This restriction applies only to the logo asset and
does not restrict the CERN-OHL-S v2 rights in the separate technical design
source. See the `proprietary/maxeelabs-logo` block in `LICENSES/dep5`.
