import pytest
from django.http import Http404
from corpora.lib.dj.decorators import async_raise_not_found
from django.core.exceptions import ObjectDoesNotExist


# A sample async function to simulate normal and failing behavior
class SampleModel:
    """Mock model to simulate async ORM operations."""

    async def get_object(self, should_fail=False):
        if should_fail:
            raise ObjectDoesNotExist("Simulated missing object")
        return "Success"


# Decorate the sample function to apply the async_raise_not_found decorator
@async_raise_not_found
async def get_sample_object(should_fail=False):
    model = SampleModel()
    return await model.get_object(should_fail=should_fail)


@pytest.mark.asyncio
async def test_async_raise_not_found_success():
    """Test that the decorator returns the result correctly when no exception occurs."""
    result = await get_sample_object(should_fail=False)
    assert result == "Success"


@pytest.mark.asyncio
async def test_async_raise_not_found_raises_404():
    """Test that the decorator raises Http404 when ObjectDoesNotExist is raised."""
    with pytest.raises(Http404, match="Object not found"):
        await get_sample_object(should_fail=True)
