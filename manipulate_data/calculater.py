import numpy as np

class Calculater:

    def alignment(self, target_vec, rotation_matrix, translation_vector):
        transformed_vec = np.dot(target_vec, rotation_matrix) + translation_vector
        return transformed_vec

    def calculate_rmsd(self, coord1, coord2):
        """
        Calculate RMSD between two sets of coordinates.
        """
        diff = coord1 - coord2
        rmsd = np.sqrt(np.mean(np.sum(diff**2, axis=1)))
        return rmsd

    def superimpose_coordinates(self, coord1, coord2):
        """
        Superimpose two sets of coordinates using the least squares method.
        Returns the rotated and translated coordinates of coord2.
        """
        # Centering coordinates
        center1 = np.mean(coord1, axis=0)
        center2 = np.mean(coord2, axis=0)
        coord1_centered = coord1 - center1
        coord2_centered = coord2 - center2

        # Calculating the covariance matrix
        covariance_matrix = np.dot(coord1_centered.T, coord2_centered)

        # Singular Value Decomposition (SVD) to find the rotation matrix
        u, s, v = np.linalg.svd(covariance_matrix)
        rotation_matrix = np.dot(u, v)

        # If the determinant of the rotation matrix is -1, correct for inversion
        if np.linalg.det(rotation_matrix) < 0:
            v[:, -1] *= -1
            rotation_matrix = np.dot(u, v)

        # Calculate the translation vector
        translation_vector = center1 - np.dot(center2, rotation_matrix)

        # Apply the rotation and translation to coord2
        coord2_transformed = np.dot(coord2, rotation_matrix) + translation_vector

        return coord2_transformed, (rotation_matrix, translation_vector)
