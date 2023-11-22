import numpy as np

import open3d as o3d
import copy

from head_reg import *


# mesh filepaths
head_model_path = "./data/head_model_.obj"
head_prior_path = "./data/head_prior.obj"

# read the meshes
head_model = read_mesh(head_model_path)
head_prior = read_mesh(head_prior_path)

# bringing the meshes to the origin
head_model = center_mesh(head_model)
head_prior = center_mesh(head_prior)

# head_model -> red, head_prior -> green
head_model.paint_uniform_color([1, 0, 0])
head_prior.paint_uniform_color([0, 1, 0])

# rotate the head_prior, to bring it to nearly same orientation, obtained by trial and error
initial_rpy = [150, -50, -10]

# apply registration, output -> blue
transformed_prior = register_heads(head_prior, head_model, initial_rpy)
transformed_prior.paint_uniform_color([0, 0, 1])

# write the transformed prior to a file
o3d.io.write_triangle_mesh("./data/transformed_prior.obj", transformed_prior)

# visualize the results
o3d.visualization.draw_geometries([head_model, transformed_prior])