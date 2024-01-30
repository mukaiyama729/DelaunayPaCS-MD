import numpy as np

class Calculater:

    def alignment(self, target_vec, rotation_matrix, translation_vector):
        transformed_vec = np.dot(rotation_matrix, target_vec.T).T + translation_vector
        return transformed_vec

    def calculate_rmsd(self, coord1, coord2):
        diff = coord1 - coord2
        rmsd = np.sqrt(np.mean(np.sum(diff**2, axis=1)))
        return rmsd

    def superimpose_coordinates(self, coord1, coord2):
        center1 = np.mean(coord1, axis=0)
        center2 = np.mean(coord2, axis=0)
        coord1_centered = coord1 - center1
        coord2_centered = coord2 - center2

        covariance_matrix = np.dot(coord1_centered.T, coord2_centered)
        u, s, v = np.linalg.svd(covariance_matrix)
        rotation_matrix = np.dot(v, u)
        if np.linalg.det(rotation_matrix) < 0:
            rotation_matrix[:, -1] *= -1
        translation_vector = center1 - np.dot(rotation_matrix, center2.T).T

        coord2_transformed = np.dot(rotation_matrix, coord2.T).T + translation_vector

        return coord2_transformed, (rotation_matrix, translation_vector)
