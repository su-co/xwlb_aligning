import numpy as np
import textsearch

query = "LOVE"
target = "ILOVEYOU"

##########################
# create suffux array
##########################
print("""##########################
# create suffux array
##########################""")

# concatenate query and target to a long sequence
sequence = np.fromstring(query + target, dtype=np.int8)

# construct suffix array
# the sentinel letter $ is lexicographically larger than all other characters 
# and we call the sentinel letter EOS.
suffix_array = textsearch.create_suffix_array(sequence)
print(suffix_array)

for i in suffix_array[:-1]:
    print(i) # print order
    print(sequence[i:].tobytes().decode("utf-8") + "$") # print suffix

##########################
# find close match
##########################
print("""##########################
# find close match
##########################""")

# close match
close_matches = textsearch.find_close_matches(
    suffix_array=suffix_array,
    query_len=len(query),
)

print("n\t\tpos\t\ttype\t\tsubstring (sort lexicographically)")
print("-" * 65)
for i in range(suffix_array.size - 2):
    t = "query" if suffix_array[i] < len(query) else "target"
    sub = sequence[suffix_array[i] :].tobytes().decode("utf-8")
    print(i, suffix_array[i], t, sub, sep="\t\t")

for i in range(len(query)):
    print(f"Query {query[i]} precede and follow postion is {str(close_matches[i])}")
