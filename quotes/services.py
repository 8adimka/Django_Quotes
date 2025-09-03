import random
from typing import List, Optional, Tuple

from django.conf import settings
from django.db.models import F, FloatField, Value
from django.db.models.functions import Cast

from .models import Quote


def select_random_quote() -> Optional[Quote]:
    """
    Выбор одной цитаты по весам.
    Эффективный вес: base_weight + like_step*likes - dislike_step*dislikes (ограничен снизу).
    """
    like_step = getattr(settings, "WEIGHT_LIKE_STEP", 0.2)
    dislike_step = getattr(settings, "WEIGHT_DISLIKE_STEP", 0.1)
    min_w = getattr(settings, "MIN_EFFECTIVE_WEIGHT", 0.05)

    qs = Quote.objects.annotate(
        eff=F("base_weight")
        + Value(like_step) * F("likes")
        - Value(dislike_step) * F("dislikes")
    ).annotate(eff_clip=Cast(F("eff"), FloatField()))

    pairs: List[Tuple[int, float]] = []
    for q in qs.only("id"):
        w = max(float(getattr(q, "eff_clip", 0.0)), float(min_w))
        pairs.append((q.id, w))

    if not pairs:
        return None

    total = sum(w for _, w in pairs)
    r = random.uniform(0.0, total)
    acc = 0.0
    chosen_id = pairs[-1][0]
    for qid, w in pairs:
        acc += w
        if r <= acc:
            chosen_id = qid
            break

    return Quote.objects.select_related("source").get(pk=chosen_id)
