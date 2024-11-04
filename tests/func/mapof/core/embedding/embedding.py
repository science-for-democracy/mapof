import pytest

from mapof.core.embedding.embed import embed


list_of_embedding_algorithms = {
    'fr',
    'kk',
    'mds',
}


class TestEmbedding:

    @pytest.mark.parametrize("embedding_id", list_of_embedding_algorithms)
    def test_embedding(self, mocker, embedding_id):
        experiment = mocker.patch('mapof.core.objects.Experiment.Experiment')

        experiment.distances = {'ID': {'UN': 1, 'a': 0.75, 'b': 0.5},
                                'UN': {'ID': 1, 'a': 0.25, 'b': 0.5},
                                'a': {'ID': 0.75, 'UN': 0.25, 'b': 0.13},
                                'b': {'ID': 0.5, 'UN': 0.5, 'a': 0.13}}

        experiment.is_exported = False

        embed(experiment, embedding_id=embedding_id, dim=2)

        assert len(experiment.coordinates) == len(experiment.distances)