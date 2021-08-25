# a simple and scuffed implementation of naive k-means clustering
# https://en.wikipedia.org/wiki/K-means_clustering#Standard_algorithm_(naive_k-means)
# there's probably a better implementation of this already in some library

import numpy as np
from random import sample, choice

# yes, I know numpy has an argmin built in already, but I don't want to keep converting to np.array
def argmin(arr):
    ans = [0]
    for i in range(len(arr)):
        if arr[i] < arr[ans[0]]:
            ans = [i]
        elif arr[i] == arr[ans[0]]:
            ans.append(i)
    return choice(ans)

def get_means(k, pixels, reps=100):
    means = sample(pixels, k)  # choose k pixels as our initial guess
    for _ in range(reps):
        partitions = [[] for i in range(len(means))]
        for pixel in pixels:
            partitions[argmin([np.linalg.norm(pixel-mean) for mean in means])].append(pixel)
        means = [sum(partition)/len(partition) for partition in partitions if len(partition) > 0]
        
    return [tuple(int(x) for x in mean) for mean in means]

def cluster(k, pixels_raw):
    pixels = [np.array(pixel) for pixel in pixels_raw]
    means = get_means(k, pixels, reps=500)
    for i in range(len(pixels)):
        pixels[i] = means[argmin([np.linalg.norm(pixels[i]-mean) for mean in means])]
    
    return pixels

if __name__ == '__main__': # quick test
    from random import randint
    pixels = sorted([(1,2,3), (3,4,5), (5,6,7)])
    for pixel in pixels:
        print(pixel)
    print(cluster(2, pixels))