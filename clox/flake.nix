{
  description = "Clang development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

        dart219 = pkgs.stdenv.mkDerivation {
          pname = "dart";
          version = "2.19.6";
          src = pkgs.fetchurl {
            url = "https://storage.googleapis.com/dart-archive/channels/stable/release/2.19.6/sdk/dartsdk-linux-x64-release.zip";
            sha256 = "0fdff25e6acba3d6094155a7e341634f8de3477e86c2fda4ad47232c1adf704f";
          };
          nativeBuildInputs = [ pkgs.unzip ];
          installPhase = ''
            mkdir -p $out
            unzip $src -d $out
            ln -s $out/dart-sdk/bin $out/bin
          '';
        };
      in
      {
        devShells.default = pkgs.clangStdenv.mkDerivation {
          name = "clang-nix-develop";

          nativeBuildInputs = with pkgs; [
            clang-tools
            cmake
            ninja
            gnumake
            dart219
            jdk
          ];

          buildInputs = with pkgs; [
            # add libraries here
            glibc.dev
          ];

          shellHook = ''
            echo "Clang development environment loaded"
            echo "Clang version: $(clang --version | head -n1)"
          '';
        };
      }
    );
}
