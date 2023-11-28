import numpy as np

class Calculater:

    def alignment(self, target_vec, rotation_matrix, translation_vector):
        transformed_vec = np.dot(target_vec, rotation_matrix) + translation_vector
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
        rotation_matrix = np.dot(u, v)
        if np.linalg.det(rotation_matrix) < 0:
            v[:, -1] *= -1
            rotation_matrix = np.dot(u, v)
        translation_vector = center1 - np.dot(center2, rotation_matrix)

        coord2_transformed = np.dot(coord2, rotation_matrix) + translation_vector

        return coord2_transformed, (rotation_matrix, translation_vector)
