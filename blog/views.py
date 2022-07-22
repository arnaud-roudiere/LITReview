from itertools import chain
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import SignupForm, TicketForm, ReviewForm
from . import forms, models
from django.contrib import messages
from .models import UserFollows, Ticket, Review
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


@login_required
def follow_users(request):
    form = forms.FollowUsersForm(instance=request.user)
    if request.method == 'POST':
        form = forms.FollowUsersForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'blog/follow_users_form.html',
                  context={'form': form})


@login_required
def create_ticket_and_review_view(request):
    """ Create ticket and review at the same time. """
    ticket_form = TicketForm()
    review_form = ReviewForm()

    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)

        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.has_review = True
            ticket.save()
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.ticket.has_review = True
            review.user = request.user
            review.save()
            messages.success(request, "Le ticket et le critique sont créés.")
            return redirect("posts")

    context = {"ticket_form": ticket_form, "review_form": review_form}

    return render(request, "blog/create_ticket_review.html", context=context)


@login_required
def create_ticket_view(request):
    """ Create a ticket """
    form = TicketForm()
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, "Votre ticket a été créé.")
            return redirect("posts")
    context = {"form": form}
    return render(request, "blog/create_ticket.html", context=context)


@login_required
def posts_view(request):
    """ Get tickets and reviews for the post page"""
    tickets = Ticket.objects.filter(Q(user=request.user))
    print('TICKET :', tickets)
    reviews = Review.objects.filter(Q(user=request.user))
    print('REVIEWS :', reviews)
    tickets_and_reviews = sorted(chain(tickets, reviews),
                                 key=lambda obj: obj.time_created,
                                 reverse=True)

    return render(request, "blog/posts.html",
                  context={"tickets_and_reviews": tickets_and_reviews})


@login_required
def flux(request):
    """ Main page - The tickets and reviews
    of the user itself and user the user follows """
    users_followers = UserFollows.objects.filter(user=request.user)
    users = []
    for user in users_followers:
        users.append(user.followed_user)
    tickets = Ticket.objects.filter(Q(has_review=False)
                                    & (Q(user=request.user)
                                       | Q(user__in=users)))
    reviews = Review.objects.filter(Q(user=request.user)
                                    | Q(user__in=users))

    tickets_and_reviews = sorted(chain(tickets,
                                       reviews),
                                 key=lambda obj: obj.time_created,
                                 reverse=True)
    return render(request, "blog/flux.html",
                  context={"content": tickets_and_reviews})


@login_required
def follow_users_view(request):
    """ Follow a user and get user followers """
    following_users = UserFollows.objects.filter(user=request.user.id)
    users_followers = UserFollows.objects.filter(followed_user=request.user.id)
    if request.POST:
        if 'following' in request.POST:
            user = User.objects.filter(
                username=request.POST["following"]).first()
            if str(request.user) == request.POST["following"]:
                messages.error(request, "Vous ne pouvez pas suivre vous même")
                return redirect("follow")

            try:
                form = UserFollows()
                form.user = request.user
                form.followed_user = user
                form.save()
                messages.success(
                    request, f"Vous avez bien ajouté "
                             f"{request.POST['following']} à votre liste.",
                )
            except:
                if user is None:
                    messages.error(request, "Cet utilisateur n'existe pas.")
                else:
                    messages.error(request, f"Vous suivez déjà {user}")

            return redirect("follow")

    context = {"following": following_users, "followers": users_followers}
    return render(request, "blog/follow.html", context=context)


@login_required
def remove_following_user_view(request, id):
    """ Remove a follower """
    user = get_object_or_404(User, id=id)
    remove_user = UserFollows.objects.get(
        user=request.user.id, followed_user=user)
    remove_user.delete()
    return redirect("follow")


@login_required
def create_review(request, ticket_id):
    """ Create a review of a ticket """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if ticket.has_review:
        messages.error(request, "Ce ticket à déjà une critique.")
        return redirect("posts")
    form = ReviewForm()
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            ticket.has_review = True
            ticket.save()
            messages.success(request, "Votre critique est créée.")
            return redirect("posts")

    context = {"ticket": ticket, "form": form}

    return render(request, "blog/create_review.html", context=context)


@login_required
def delete_ticket(request, ticket_id):
    """ Delete user ticket """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket.delete()
    messages.success(request,
                     f"Votre ticket {ticket.title} est bien supprimé.")
    return redirect("posts")


@login_required
def delete_review(request, review_id):
    """ Delete user review """
    review = get_object_or_404(Review, id=review_id)
    ticket = get_object_or_404(Ticket, id=review.ticket.id)
    ticket.has_review = False
    ticket.save()
    review.delete()
    messages.success(request,
                     f"Votre critique '{review.headline}'"
                     f" a bien été supprimée.")
    return redirect("posts")


@login_required
def update_review(request, review_id):
    """ Update a user review"""
    context = {}
    review = get_object_or_404(Review, id=review_id)
    context["form"] = ReviewForm(instance=review)
    if request.method == "POST":
        update_form = ReviewForm(request.POST, instance=review)
        if update_form.is_valid():
            update_form.save()
            messages.success(request, "Votre ticket a été modifié.")
            return redirect("posts")

    context["review"] = review

    return render(request, "app/update_review.html", context=context)


@login_required
def update_ticket(request, id):
    """ Update a user ticket """
    context = {}
    ticket = get_object_or_404(Ticket, id=int(id))
    context["form"] = TicketForm(instance=ticket)
    if request.method == "POST":
        update_form = TicketForm(request.POST, request.FILES, instance=ticket)
        if update_form.is_valid():
            update_form.save()
            messages.success(request, "Votre ticket a été modifié.")
            return redirect("posts")

    context["ticket"] = ticket

    return render(request, "blog/update_ticket.html", context=context)


def signup_view(request):
    """ Create user account """
    form = SignupForm()
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre compte a été créé.")
            return redirect(settings.LOGIN_URL)
    return render(request, "blog/signup.html", context={"form": form})
