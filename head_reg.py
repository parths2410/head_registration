import open3d as o3d
import numpy as np
import scipy

import copy

from probreg import cpd
from nricp import nonrigidIcp

def read_mesh(path):
    mesh = o3d.io.read_triangle_mesh(path)
    mesh.compute_vertex_normals()
    return mesh

def center_mesh(mesh):
    mean = np.mean(np.asarray(mesh.vertices), axis=0)
    mesh.vertices = o3d.utility.Vector3dVector(np.asarray(mesh.vertices) - mean)
    return mesh

def rotate_mesh(mesh, rpy):
    rpy = np.deg2rad(rpy)
    R = o3d.geometry.get_rotation_matrix_from_xyz(rpy)
    mesh.rotate(R, center=(0, 0, 0))
    return mesh

def calc_error(source, target):
    target_KDTree = scipy.spatial.KDTree(np.asarray(target.vertices))
    dist, _ = target_KDTree.query(np.asarray(source.vertices))
    return np.mean(dist)

def apply_rigid_cpd(source, target):
    transformed_source = copy.deepcopy(source)
    
    source_pcd = o3d.geometry.PointCloud()
    source_pcd.points = o3d.utility.Vector3dVector(np.asarray(source.vertices))

    target_pcd = o3d.geometry.PointCloud()
    target_pcd.points = o3d.utility.Vector3dVector(np.asarray(target.vertices))

    transformed_source_pcd = o3d.geometry.PointCloud()
    transformed_source_pcd.points = o3d.utility.Vector3dVector(np.asarray(transformed_source.vertices))

    tf_param, _, _ = cpd.registration_cpd(source_pcd, target_pcd)
    transformed_source_pcd.points = tf_param.transform(transformed_source_pcd.points)

    transformed_source.vertices = o3d.utility.Vector3dVector(np.asarray(transformed_source_pcd.points))
    return transformed_source

def register_heads(head_prior_, head_model_, initial_rpy):
    head_prior = copy.deepcopy(head_prior_)
    head_model = copy.deepcopy(head_model_)

    head_prior = center_mesh(head_prior)
    head_model = center_mesh(head_model)

    head_prior = rotate_mesh(head_prior, initial_rpy)
    
    print("Step 1: Rigid CPD")
    transformed_head_cpd = apply_rigid_cpd(head_prior, head_model)

    print("Step 2: Non-rigid ICP")
    transformed_head_nricp = nonrigidIcp(transformed_head_cpd, head_model)

    return transformed_head_nricp

def visualize_meshes(meshes):
    o3d.visualization.draw_geometries(meshes)

def visualize_pointclouds(meshes):
    pointclouds = []
    for mesh in meshes:
        pointcloud = o3d.geometry.PointCloud()
        pointcloud.points = o3d.utility.Vector3dVector(np.asarray(mesh.vertices))
        pointclouds.append(pointcloud)    
    o3d.visualization.draw_geometries(pointclouds)