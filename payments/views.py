import uuid
from django.utils import timezone

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods

import stripe

from .models import FeeItem, Payment
from .services import create_fee_checkout_session, retrieve_checkout_session


@login_required
def fee_list(request):
    if request.user.role != 'parent':
        return HttpResponseForbidden('Parents only.')

    fees = FeeItem.objects.filter(parent=request.user).select_related('school')
    outstanding = fees.exclude(status=FeeItem.STATUS_PAID)
    paid = fees.filter(status=FeeItem.STATUS_PAID)

    return render(request, 'payments/fees.html', {
        'outstanding': outstanding,
        'paid': paid,
        'publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    })


@login_required
@require_POST
def create_checkout(request, fee_id):
    if request.user.role != 'parent':
        return HttpResponseForbidden('Parents only.')

    fee = get_object_or_404(FeeItem, pk=fee_id, parent=request.user)
    if fee.status == FeeItem.STATUS_PAID:
        messages.info(request, 'This fee is already paid.')
        return redirect('payments:fee_list')

    success_url = (
        request.build_absolute_uri(reverse('payments:success'))
        + '?session_id={CHECKOUT_SESSION_ID}'
    )
    cancel_url = request.build_absolute_uri(reverse('payments:cancel'))

    try:
        session = create_fee_checkout_session(
            fee_item=fee,
            success_url=success_url,
            cancel_url=cancel_url,
            customer_email=request.user.email or None,
        )
        return redirect(session.url, code=303)
    except stripe.error.StripeError as exc:
        messages.error(request, f'Payment could not be started: {exc}')
        return redirect('payments:fee_list')


@login_required
def payment_success(request):
    session_id = request.GET.get('session_id')
    payment = None

    if session_id:
        try:
            session = retrieve_checkout_session(session_id)
            if session.payment_status != 'paid':
                messages.warning(request, 'Payment not completed yet.')
                return redirect('payments:fee_list')

            if not Payment.objects.filter(stripe_session_id=session_id).exists():
                fee_id = session.metadata.get('fee_item_id')
                fee = get_object_or_404(FeeItem, pk=fee_id, parent=request.user)

                payment = Payment.objects.create(
                    fee_item=fee,
                    parent=request.user,
                    stripe_session_id=session_id,
                    stripe_payment_intent=session.payment_intent or '',
                    amount_pence=session.amount_total,
                    currency=(session.currency or 'gbp').upper(),
                    status=Payment.STATUS_COMPLETE,
                    receipt_reference=uuid.uuid4().hex[:12].upper(),
                    paid_at=timezone.now(),
                )
                fee.status = FeeItem.STATUS_PAID
                fee.save(update_fields=['status'])
            else:
                payment = Payment.objects.get(stripe_session_id=session_id)

        except stripe.error.StripeError:
            messages.error(request, 'Could not verify payment with Stripe.')
            return redirect('payments:fee_list')

    return render(request, 'payments/success.html', {'payment': payment})


@login_required
def payment_cancel(request):
    messages.info(request, 'Payment cancelled — no charge was made.')
    return render(request, 'payments/cancel.html')


@csrf_exempt
@require_POST
def stripe_webhook(request):
    """Stripe sends payment events here — verify signature in production."""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')

    from .services import configure_stripe
    configure_stripe()
    try:
        if settings.STRIPE_WEBHOOK_SECRET:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET,
            )
        else:
            import json
            event = stripe.Event.construct_from(json.loads(payload), stripe.api_key)
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponseForbidden('Invalid payload')

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        _mark_fee_paid_from_session(session)

    return HttpResponse(status=200)


def _mark_fee_paid_from_session(session):
    session_id = session.get('id')
    if not session_id or Payment.objects.filter(stripe_session_id=session_id).exists():
        return

    fee_id = session.get('metadata', {}).get('fee_item_id')
    if not fee_id:
        return

    try:
        fee = FeeItem.objects.get(pk=fee_id)
    except FeeItem.DoesNotExist:
        return

    Payment.objects.create(
        fee_item=fee,
        parent=fee.parent,
        stripe_session_id=session_id,
        stripe_payment_intent=session.get('payment_intent') or '',
        amount_pence=session.get('amount_total') or fee.amount_pence,
        currency=(session.get('currency') or 'gbp').upper(),
        status=Payment.STATUS_COMPLETE,
        receipt_reference=uuid.uuid4().hex[:12].upper(),
        paid_at=timezone.now(),
    )
    fee.status = FeeItem.STATUS_PAID
    fee.save(update_fields=['status'])


# ---------------------------------------------------------------------------
# earlier attempts (kept for my own notes during debugging)
# ---------------------------------------------------------------------------
# BUG: fee_list used FeeItem.objects.all() so every parent saw every school's fees.
# BUG: checkout used unit_amount=fee.amount_pence // 100 — stripe charged pennies not pounds.
# BUG: forgot configure_stripe() before Session.create — got "No API key provided".
# BUG: success view saved Payment even when session.payment_status was 'unpaid' on refresh.
# BUG: cancel_url was '/payments/cancelled/' but url name is payments:cancel.
