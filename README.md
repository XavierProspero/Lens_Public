# Glass Imaging Lens Model
A small ray tracing model with a biconvex lense, point source and sensor.

## Specifications

1. Optical simulation (ray tracing):
Create a software simulation (in a language of your choosing, though we suggest Python or C) of a simple biconvex lens element, tracing a grid of rays from a source scene point through the lens and onto a discrete sensor plane. 

Assume that the following variables are provided as inputs (D, R1, T, R2, D2, OD, all in mm; lambda in nm; integers N, M, h):
- The point source object is on-axis at distance D.
- The lens is a simple lens with radius R1 on the subject side, thickness T in its center, radius R2 on its back side (facing the sensor). 
- Distance D2 between surface 2 and sensor plane. (D2 should be constrained in a reasonable range such that scene points between an approximate minimum focus distance and the infinity may be in focus)
- The aperture of the lens is OD. (Need to make sure it’s not too large that the radii would intersect)
- Use a single wavelength, lambda (e.g. 500nm by default). 
- Use a uniformly sampled in angle grid of N rays (e.g. 15 by default, but you may want to increase this)
- Assume an image sensor with size h x h mm and MxM pixels (choose h to be a reasonable size for the maximum PSF size to fill the image, and M can be e.g. 100 by default)

## Testing
to test the following classes follow the steps below. 
Clone repo. 

`cd Glass_Imaging_lens`

`python3 -m pytest gitest.py`

## Running
to run the program make sure all dependencies are installed.

`cd Glass_Imaging_lens`

`python3 app.py $(cat args.txt)`

to run with non default arguments run

`python3 app.py -h`

then edit arguments in `args.txt`
