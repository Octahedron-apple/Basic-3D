{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  buildInputs = with pkgs; [
    python3 python3Packages.tkinter pkg-config

    # Core C/C++ (libc, libm, libdl, libpthread, librt, libstdc++, libgcc_s)
    glibc stdenv.cc.cc.lib
    # Fortran runtime (libgfortran, libquadmath) — numpy/scipy
    gfortran.cc.lib

    # Compression
    bzip2 xz zlib
    # Crypto / TLS
    openssl
    # Database
    sqlite
    # Terminal
    ncurses readline
    # FFI / Build
    libffi expat gdbm mpdecimal

    # Graphics
    libGL freetype harfbuzz libpng libjpeg libtiff libwebp
    # SDL2 (pygame-ce)
    SDL2 SDL2_image SDL2_mixer SDL2_ttf
    # X11
    libx11 libxcursor libxext libxfixes
    libxi libxinerama libxrandr libxrender
    # Wayland
    wayland libxkbcommon

    # Audio
    alsa-lib pulseaudio jack2
    flac libogg libvorbis libopus mpg123
    libsndfile libmodplug fluidsynth portmidi

    # Math / Science (blas, lapack, openblas)
    openblas lapack
  ];
  LD_LIBRARY_PATH = with pkgs; lib.makeLibraryPath [
    glibc stdenv.cc.cc.lib gfortran.cc.lib
    bzip2 xz zlib openssl sqlite ncurses readline
    libffi expat gdbm mpdecimal
    libGL freetype harfbuzz libpng libjpeg libtiff libwebp
    SDL2 SDL2_image SDL2_mixer SDL2_ttf
    libx11 libxcursor libxext libxfixes
    libxi libxinerama libxrandr libxrender
    wayland libxkbcommon
    alsa-lib pulseaudio jack2
    flac libogg libvorbis libopus mpg123
    libsndfile libmodplug fluidsynth portmidi
    openblas lapack
  ];
  shellHook = ''
    source $HOME/.Virtual-Environment/normal/bin/activate
    echo "[✓] Normal venv activated."
  '';
}
