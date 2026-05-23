"""Export a MATLAB_Code/Dark.m first-plane reference using MATLAB Engine.

This script is intentionally Python 3.6 compatible because MATLAB Engine is
available in the local ``matlab_py36`` environment.
"""

import sys

import matlab.engine


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: export_matlab_first_plane.py <repo-root> <output.mat>")

    root = sys.argv[1]
    output = sys.argv[2]
    eng = matlab.engine.start_matlab()
    try:
        eng.addpath(root + "/MATLAB_Code/helpfunctions", nargout=0)
        eng.eval("cd('{0}')".format(root), nargout=0)
        eng.eval(
            """
image0 = double(imstackread('MATLAB_Code/input/Mousekidney_561nm_1.49NA_65nm.tif'));
image0 = 255*(image0 - min(min(min(image0))))./(max(max(max(image0)))-min(min(min(image0))));
[Nx,Ny,Nz] = size(image0);
pad_size = 15;
for jz = 1:Nz
    image(:,:,jz) = padarray(image0(:,:,jz),[floor(Nx/pad_size)+1,floor(Ny/pad_size)+1],'symmetric');
end
[params.Nx,params.Ny,~] = size(image);
params.NA = 1.49;
params.emwavelength = 610;
params.pixelsize = 65;
params.factor = 2;
[Hi,Lo,lp,EL] = separateHiLo(squeeze(image(:,:,1)),params,6,0.5);
block_size = confirm_block(params,lp);
Lo_process = dehaze_fast2(Lo, 0.95, block_size, EL,3,70);
result = Lo_process + Hi;
result_crop = result(floor(Nx/pad_size)+2:floor(Nx/pad_size)+Nx+1,floor(Ny/pad_size)+2:floor(Ny/pad_size)+Ny+1);
save('{0}','result_crop','block_size');
""".format(output),
            nargout=0,
        )
    finally:
        eng.quit()


if __name__ == "__main__":
    main()
