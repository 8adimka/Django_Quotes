from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F
from django.utils.translation import gettext_lazy as _


class Source(models.Model):
    class SourceType(models.TextChoices):
        FILM = "film", _("Фильм")
        BOOK = "book", _("Книга")
        OTHER = "other", _("Другое")

    title = models.CharField(_("Название источника"), max_length=255)
    type = models.CharField(
        _("Тип"), max_length=16, choices=SourceType.choices, default=SourceType.OTHER
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("title", "type")]
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} ({self.get_type_display()})"


class Quote(models.Model):
    source = models.ForeignKey(
        Source,
        on_delete=models.CASCADE,
        related_name="quotes",
        verbose_name=_("Источник"),
    )
    text = models.TextField(_("Текст цитаты"))
    # Для регистронезависимой уникальности:
    normalized_text = models.CharField(max_length=2048, unique=True, editable=False)

    base_weight = models.FloatField(_("Базовый вес"), default=1.0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-likes", "-views", "-created_at"]

        # Доп. защита от дубликатов на уровне БД (если хочется именно выражением):
        # Django 3.2+ позволяет UniqueConstraint + Lower, но мы уже держим normalized_text уникальным.
        # constraints = [
        #     models.UniqueConstraint(Lower("text"), name="uq_quote_text_lower"),
        # ]

    def clean(self):
        super().clean()
        # Лимит 3 цитаты на источник
        existing = Quote.objects.filter(source=self.source)
        if self.pk:
            existing = existing.exclude(pk=self.pk)
        if existing.count() >= 3:
            raise ValidationError(
                _("У источника «%(title)s» уже есть 3 цитаты."),
                params={"title": self.source.title},
            )

    def save(self, *args, **kwargs):
        self.normalized_text = (self.text or "").strip().lower()
        self.full_clean()
        return super().save(*args, **kwargs)

    @property
    def effective_weight(self) -> float:
        like_step = getattr(settings, "WEIGHT_LIKE_STEP", 0.2)
        dislike_step = getattr(settings, "WEIGHT_DISLIKE_STEP", 0.1)
        min_w = getattr(settings, "MIN_EFFECTIVE_WEIGHT", 0.05)
        return max(
            self.base_weight + like_step * self.likes - dislike_step * self.dislikes,
            min_w,
        )

    # Без гонок инкрементим через F-выражения:
    def add_view(self):
        Quote.objects.filter(pk=self.pk).update(views=F("views") + 1)

    def add_like(self):
        Quote.objects.filter(pk=self.pk).update(likes=F("likes") + 1)

    def add_dislike(self):
        Quote.objects.filter(pk=self.pk).update(dislikes=F("dislikes") + 1)

    def __str__(self):
        return f"«{self.text[:60]}…» — {self.source}"
