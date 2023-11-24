import random

# Seed
random.seed(1993) # 1996, 2023, 2022

y_chromosome_length = 57227415

# random select
random_regions = []
for _ in range(10):
    start = random.randint(1, y_chromosome_length - 1000000)
    end = start + 999999
    random_regions.append((start, end))
print('Y chromosome')
print(random_regions)

# Set the random seed for reproducibility
random.seed(2023)

# Human chromosome lengths in base pairs from chromosome 1 to 22
chromosome_lengths = {
    1: 248956422,
    2: 242193529,
    3: 198295559,
    4: 190214555,
    5: 181538259,
    6: 170805979,
    7: 159345973,
    8: 145138636,
    9: 138394717,
    10: 133797422,
    11: 135086622,
    12: 133275309,
    13: 114364328,
    14: 107043718,
    15: 101991189,
    16: 90338345,
    17: 83257441,
    18: 80373285,
    19: 58617616,
    20: 64444167,
    21: 46709983,
    22: 50818468
}

# Randomly select segments from each chromosome
selected_segments = {}
for chromosome, length in chromosome_lengths.items():
    # Ensure the segment is within the chromosome range
    start = random.randint(1, length - 1000000)
    end = start + 1000000
    selected_segments[chromosome] = (start, end)

print('Autosome chromosome')

print(selected_segments)