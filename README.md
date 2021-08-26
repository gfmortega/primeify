# Prime-ify!
This program has two main functions
- Convert images into pixel art that has a limited number of RGB colors in its palette.  This uses a (very bad) implementation of Lloyd's Algorithm for k-means clustering, as described on the Wikipedia article.
- Convert the pixel-art into a prime number!  This uses an implementation of the Miller-Rabin primality test, as described in CLRS.

All handling of images is done using PIL (Python Image Library)

For reasonable waiting times, try to prime-ify pixelart that only has a few thousand pixels.
