from django import forms
from django.core.exceptions import ValidationError

from .models import Quote, Source


class AddQuoteForm(forms.Form):
    source_type = forms.ChoiceField(
        label="Тип источника", choices=Source.SourceType.choices
    )
    source_title = forms.CharField(label="Название источника", max_length=255)
    text = forms.CharField(
        label="Текст цитаты", widget=forms.Textarea(attrs={"rows": 4})
    )
    base_weight = forms.FloatField(label="Базовый вес", min_value=0.0, initial=1.0)

    def clean(self):
        cleaned = super().clean()
        text = (cleaned.get("text") or "").strip()
        normalized = text.lower()
        if Quote.objects.filter(normalized_text=normalized).exists():
            raise ValidationError("Такая цитата уже существует (дубликаты запрещены).")

        # Проверка лимита на источник (<=3)
        stype = cleaned.get("source_type")
        stitle = (cleaned.get("source_title") or "").strip()
        if stype and stitle:
            source, _ = Source.objects.get_or_create(type=stype, title=stitle)
            if source.quotes.count() >= 3:
                raise ValidationError(f"У источника «{stitle}» уже есть 3 цитаты.")
        return cleaned

    def save(self) -> Quote:
        stype = self.cleaned_data["source_type"]
        stitle = self.cleaned_data["source_title"].strip()
        source, _ = Source.objects.get_or_create(type=stype, title=stitle)
        quote = Quote.objects.create(
            source=source,
            text=self.cleaned_data["text"].strip(),
            base_weight=self.cleaned_data["base_weight"],
        )
        return quote
