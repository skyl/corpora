import uuid
from django.db import models
from django.utils import timezone
from pgvector.django import VectorField


class Corpus(models.Model):
    """
    Represents a unique corpus, often corresponding to a specific repository
    or collection of documents. A corpus can have an associated URL for
    tracking its origin, such as a GitHub repository.
    """

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text="Unique identifier for each corpus, used as the primary key.",
    )
    name = models.CharField(max_length=255)
    url = models.URLField(
        null=True,
        blank=True,
        help_text="Optional URL associated with the corpus, e.g., a GitHub repository.",
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
        help_text="Timestamp indicating when the corpus was created.",
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp indicating the last update of the corpus."
    )

    class Meta:
        verbose_name_plural = "corpora"

    def __str__(self):
        return f"Corpus: {self.name} ({self.uuid})"


class File(models.Model):
    corpus = models.ForeignKey(Corpus, on_delete=models.CASCADE, related_name="files")
    path = models.CharField(max_length=1024)
    content = models.TextField(blank=True)
    ai_summary = models.TextField(blank=True)
    vector_of_summary = VectorField(dimensions=300, null=True, blank=True)
    checksum = models.CharField(max_length=32, editable=False)  # MD5 or SHA hash
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("corpus", "path")
        ordering = ["path"]

    def __str__(self):
        return f"File {self.path} in {self.corpus.name}"


# Split model to store split content with vectorization, ordering within files
class Split(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name="splits")
    order = models.PositiveIntegerField()  # Ordering for splits within the file
    content = models.TextField(blank=True)
    vector = VectorField(dimensions=300, null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        unique_together = ("file", "order")
        ordering = ["file", "order"]

    def __str__(self):
        return f"Split {self.order} of {self.file.path} in {self.file.corpus.name}"
