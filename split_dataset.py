import os
import random
import shutil

# Paths
input_dir = "clearcut_woodspecies"   # inside Clearcut-Data
output_dir = "dataset_species"       # new folder will be created here
split_ratios = (0.7, 0.2, 0.1)       # train, val, test

# Create output folders
for split in ["train", "val", "test"]:
    for species in os.listdir(input_dir):
        os.makedirs(os.path.join(output_dir, split, species), exist_ok=True)

# Split images
for species in os.listdir(input_dir):
    species_path = os.path.join(input_dir, species)
    images = os.listdir(species_path)
    random.shuffle(images)

    n_total = len(images)
    n_train = int(n_total * split_ratios[0])
    n_val = int(n_total * split_ratios[1])
    
    train_imgs = images[:n_train]
    val_imgs = images[n_train:n_train+n_val]
    test_imgs = images[n_train+n_val:]

    for img in train_imgs:
        shutil.copy(os.path.join(species_path, img), os.path.join(output_dir, "train", species, img))
    for img in val_imgs:
        shutil.copy(os.path.join(species_path, img), os.path.join(output_dir, "val", species, img))
    for img in test_imgs:
        shutil.copy(os.path.join(species_path, img), os.path.join(output_dir, "test", species, img))

print("✅ Dataset split completed!") 
