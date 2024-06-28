##########################
# Get levenshtein alignment between text and transcript (ASR转译和文本对齐)
##########################


import numpy as np
import textsearch

q = "LOVE"
t = "ILOVEYOU"
query = np.fromstring(q, dtype=np.int8).astype(np.int32)
target = np.fromstring(t, dtype=np.int8).astype(np.int32)
distance, alignments = textsearch.levenshtein_distance(query, target)
print(distance)
print(alignments)
aligns = textsearch.get_nice_alignments(alignments, q, t)
print(aligns[0])
print("-." * 10)
