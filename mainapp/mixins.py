from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.urls import reverse


class SubscriptionRequiredMixin(AccessMixin):
    """Verify that the current user has an active subscription."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.has_active_subscription():
            return redirect(reverse('subscription'))
        return super().dispatch(request, *args, **kwargs)
