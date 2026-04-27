import os
from collections import Counter

labels_dir = "dataset/detection/labels"
class_counts = Counter()

for file in os.listdir(labels_dir):
    if file.endswith(".txt"):
        with open(os.path.join(labels_dir, file), "r") as f:
            lines = f.readlines()
            for line in lines:
                class_id = line.split()[0]
                class_counts[class_id] += 1

print(class_counts)
