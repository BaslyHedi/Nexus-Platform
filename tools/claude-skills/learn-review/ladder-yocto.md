# Yocto ladder

The concepts of the learning review, in the order they are introduced. Used by Nexus-IMX91S-Yocto, the Yocto build of the Linux image for the FRDM-IMX91S, on Yocto 6.0 (Wrynose) with NXP's `meta-imx` BSP. A concept is `new`, `seen` (a review explained it) or `mastered` (Hedi used it right without help). The review takes the first `new` concept that fits the work that was done.

Yocto is learned more by setting up and deciding than by writing code, so a session can also give exercises (a goal, the tools allowed, and a "done when" check Hedi can verify alone) and design questions (the trade-off is explained, Hedi decides). A decision that matters for the project goes to Nexus-Platform as an SW decision.

## 1. Foundations: how a build is put together

| Concept | Status |
|---|---|
| BitBake, recipes, layers, tasks: the vocabulary | seen |
| The three axes: MACHINE, DISTRO, image | seen |
| Poky split into bitbake, openembedded-core and meta-yocto (6.0) | seen |
| Pinning upstream layers: submodules, `repo`, kas, `bitbake-setup` | seen |
| The build directory: `local.conf` and `bblayers.conf`, what is local and what is committed | seen |
| Layer dependencies: `LAYERDEPENDS`, `LAYERSERIES_COMPAT`, the order in `BBLAYERS` | seen |
| `.bbappend`, the `%` wildcard, dangling appends | seen |
| Shared `DL_DIR` and sstate, hash equivalence | seen |
| The task chain: `do_fetch` to `do_rootfs`, `WORKDIR`, task logs in `tmp/work` | new |
| Asking BitBake instead of guessing: `bitbake-getvar`, `bitbake -e`, `bitbake-layers show-appends` and `show-overlayed` | new |

## 2. The metadata language

| Concept | Status |
|---|---|
| Assignment: `=`, `:=`, `?=`, `??=`, `+=` and `.=`, and when each is evaluated | new |
| Overrides: `:append`, `:remove`, machine overrides such as `:mx91` | new |
| Inline Python `${@...}` and `bb.utils.contains` | new |
| Variable flags, such as `UBOOT_CONFIG[nand]` | new |
| `include`, `require`, `inherit` and classes | new |

## 3. Writing recipes

| Concept | Status |
|---|---|
| Recipe anatomy: `SRC_URI`, `S`, `B`, `D`, `LICENSE`, `LIC_FILES_CHKSUM` | new |
| Fetching a git repository at a release tag: `tag=` and `SRCREV` | new |
| Build classes: `cmake`, `meson`, `cargo` (for the Rust apps) | new |
| `DEPENDS` versus `RDEPENDS`, `PACKAGES` and `FILES` | new |
| `devtool`: `add`, `modify`, `finish` | new |
| Patches and kernel config fragments in a `.bbappend`, `FILESEXTRAPATHS` | new |

## 4. Our own layer and distro

| Concept | Status |
|---|---|
| Creating a layer: `layer.conf`, priority, `yocto-check-layer` | new |
| A distro config instead of `local.conf` | new |
| Image recipes and packagegroups: `IMAGE_INSTALL`, `IMAGE_FEATURES` | new |
| Init system: systemd or sysvinit, `INIT_MANAGER` | new |
| Development and release images: users, debug features | new |

## 5. The board (BSP)

| Concept | Status |
|---|---|
| Reading a machine config: the FRDM-IMX91S file in `meta-imx-bsp` | new |
| The i.MX 91 boot chain: `imx-boot`, ELE firmware, TF-A, U-Boot | new |
| Kernel: `linux-imx`, `KERNEL_DEVICETREE`, device tree changes for CAN | new |
| WIC images and `.wks` partition layouts | new |
| Flashing: SD card and NXP's `uuu` tool | new |

## 6. Production practice

| Concept | Status |
|---|---|
| Reproducible builds: lock files, `BB_NO_NETWORK`, mirrors | new |
| Licence compliance: `INCOMPATIBLE_LICENSE`, SPDX and SBOM | new |
| CVE tracking for the image | new |
| The SDK for app developers | new |
| A/B updates and a read-only root file system (prepares OTA) | new |
| Secure boot on the i.MX 91 (AHAB) | new |
| Building in CI: `kas-container`, a shared sstate | new |
| Moving to a new Yocto release: the migration guides | new |
