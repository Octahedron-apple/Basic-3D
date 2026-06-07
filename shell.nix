{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.stdenv.cc.cc.lib
    pkgs.zlib
    pkgs.xorg.libX11
    pkgs.xorg.libXrandr
    pkgs.xorg.libXinerama
    pkgs.xorg.libXcursor
    pkgs.xorg.libXi
    pkgs.libxkbcommon
    pkgs.wayland
    pkgs.libGL
  ];

  shellHook = ''
    export LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib:${pkgs.zlib}/lib:${pkgs.xorg.libX11}/lib:${pkgs.xorg.libXrandr}/lib:${pkgs.xorg.libXinerama}/lib:${pkgs.xorg.libXcursor}/lib:${pkgs.xorg.libXi}/lib:${pkgs.libxkbcommon}/lib:${pkgs.wayland}/lib:${pkgs.libGL}/lib:$LD_LIBRARY_PATH"
  '';
}
