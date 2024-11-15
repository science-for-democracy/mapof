from mapof.core.features.mallows import phi_from_normphi, generate_mallows_votes


class TestFeatures:

    def test_phi_from_normphi(self):

        for phi in [0, 0.25, 0.33, 0.5, 0.67, 0.75, 1]:
            normphi = phi_from_normphi(phi)
            assert type(normphi) == float

    def test_generate_mallows_votes(self):

        num_voters, num_candidates, phi, weight = 10, 5, 0.2, 0
        generate_mallows_votes(num_voters, num_candidates, phi, weight)

        num_voters, num_candidates, phi, weight = 11, 6, 0.5, 0.4
        generate_mallows_votes(num_voters, num_candidates, phi, weight)

        num_voters, num_candidates, phi, weight = 1, 1, 0, 0
        generate_mallows_votes(num_voters, num_candidates, phi, weight)

        num_voters, num_candidates, phi, weight = 8, 10, 1, 0
        generate_mallows_votes(num_voters, num_candidates, phi, weight)
