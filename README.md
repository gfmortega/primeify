# Prime-ify!
This program has two main functions
- Convert images into pixel art that has a limited number of RGB colors in its palette.  This uses a (very bad) implementation of Lloyd's Algorithm for $k$-clustered means, as described on the Wikipedia article.
- Convert the pixel-art into a prime number!  This uses an implementation of the Miller-Rabin primality test, as described in CLRS.

All handling of images is done using PIL (Python Image Library)
