from django.contrib import messages
from django.db.models import Count, Sum
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .forms import AddQuoteForm
from .models import Quote
from .services import select_random_quote


def index(request: HttpRequest) -> HttpResponse:
    quote = select_random_quote()
    eff_weight = None
    if quote:
        quote.add_view()
        quote.refresh_from_db(fields=["views", "likes", "dislikes"])

        eff_weight = quote.effective_weight

    return render(
        request, "quotes/index.html", {"quote": quote, "eff_weight": eff_weight}
    )


# def index(request: HttpRequest) -> HttpResponse:
#     quote = select_random_quote()
#     context = {"quote": quote}
#     if quote:
#         quote.add_view()
#     return render(request, "quotes/index.html", context)


def top_quotes(request: HttpRequest) -> HttpResponse:
    qs = Quote.objects.select_related("source").order_by(
        "-likes", "-views", "-created_at"
    )[:10]
    return render(request, "quotes/top.html", {"quotes": qs})


def dashboard(request: HttpRequest) -> HttpResponse:
    # Группировки по источникам
    by_source = (
        Quote.objects.values("source__title", "source__type")
        .annotate(
            quotes_count=Count("id"),
            total_likes=Sum("likes"),
            total_dislikes=Sum("dislikes"),
            total_views=Sum("views"),
        )
        .order_by("-quotes_count")
    )

    # Данные для графиков Chart.js
    labels = [f"{row['source__title']} ({row['source__type']})" for row in by_source]
    quotes_count = [row["quotes_count"] or 0 for row in by_source]
    total_likes = [row["total_likes"] or 0 for row in by_source]
    total_dislikes = [row["total_dislikes"] or 0 for row in by_source]
    total_views = [row["total_views"] or 0 for row in by_source]

    return render(
        request,
        "quotes/dashboard.html",
        {
            "labels": labels,
            "quotes_count": quotes_count,
            "total_likes": total_likes,
            "total_dislikes": total_dislikes,
            "total_views": total_views,
        },
    )


@require_http_methods(["GET", "POST"])
def add_quote(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = AddQuoteForm(request.POST)
        if form.is_valid():
            quote = form.save()
            messages.success(request, "Цитата добавлена.")
            return redirect("quotes:index")
    else:
        form = AddQuoteForm()
    return render(request, "quotes/add.html", {"form": form})


@require_http_methods(["POST"])
def like_quote(request: HttpRequest, pk: int) -> HttpResponse:
    try:
        quote = Quote.objects.get(pk=pk)
        quote.add_like()
    except Quote.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse("quotes:index"))


@require_http_methods(["POST"])
def dislike_quote(request: HttpRequest, pk: int) -> HttpResponse:
    try:
        quote = Quote.objects.get(pk=pk)
        quote.add_dislike()
    except Quote.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse("quotes:index"))
