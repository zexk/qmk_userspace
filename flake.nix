{
  description = "QMK userspace dev environment (Corne/crkbd 'zexk' keymap + あやめ avatar)";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs =
    { self, nixpkgs }:
    let
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];
      forAllSystems =
        f:
        nixpkgs.lib.genAttrs systems (
          system:
          f (
            import nixpkgs {
              inherit system;
              config.allowUnfree = true; # zpix-pixel-font is marked unfree
            }
          )
        );
    in
    {
      devShells = forAllSystems (pkgs: {
        default = pkgs.mkShell {
          packages = with pkgs; [
            qmk # build + flash CLI; pulls in avr-gcc, avr-binutils, avrdude
            avrdude # flashing (explicit)
            clang-tools # clangd / clang-format for the C keymap (.clangd is in-tree)
            git

            # avatar sprite generator (keyboards/crkbd/rev1/keymaps/zexk/gen_avatar.py)
            (python3.withPackages (ps: [ ps.pillow ]))
            zpix-pixel-font # hiragana pixel font for the あやめ name plate
          ];

          # The generator auto-discovers zpix, but pin it explicitly for reproducibility.
          NAME_FONT = "${pkgs.zpix-pixel-font}/share/fonts/truetype/zpix.ttf";

          shellHook = ''
            km=keyboards/crkbd/rev1/keymaps/zexk
            echo "qmk userspace dev shell  (crkbd/rev1:zexk)"
            echo "  build      qmk userspace-compile"
            echo "  size       avr-size -C --mcu=atmega32u4 \$QMK_HOME/.build/crkbd_rev1_zexk.elf"
            echo "  flash      qmk flash -kb crkbd/rev1 -km zexk   # reset a half into the bootloader"
            echo "  avatar     python3 $km/gen_avatar.py --png out.png      # preview moods"
            echo "  regen art  python3 $km/gen_avatar.py --emit > $km/avatar.h"
            echo
            echo "first-time setup if 'qmk userspace-compile' can't find the firmware tree:"
            echo "  qmk setup            # or: qmk config user.qmk_home=/path/to/qmk_firmware"
            echo "  qmk config user.overlay_dir=\$PWD"
          '';
        };
      });
    };
}
