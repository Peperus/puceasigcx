import pytest
from django.core.exceptions import ValidationError

from apps.grading.services import letter_from_score


@pytest.mark.parametrize(
    ("score", "letter"),
    [
        (0, "D"),
        ("29.99", "D"),
        (30, "C"),
        ("39.99", "C"),
        (40, "B"),
        ("44.99", "B"),
        (45, "A"),
        (50, "A"),
    ],
)
@pytest.mark.django_db
def test_letter_from_score_boundaries(score, letter):
    assert letter_from_score(score) == letter


@pytest.mark.parametrize("score", [-1, "50.01"])
@pytest.mark.django_db
def test_letter_from_score_rejects_out_of_range(score):
    with pytest.raises(ValidationError):
        letter_from_score(score)
