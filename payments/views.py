"""
payments/views.py
Parent-facing fee list, Stripe Checkout redirect, success/cancel, webhook.
"""
import uuid
from django.utils import timezone

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

import stripe

from pages.portal import build_portal_context
from pages.decorators import role_required

from .forms import SchoolFeeForm
from .models import FeeItem, Payment, SubscriptionPayment
from .school_fees import build_school_fee_overview, create_fees_for_students
from .services import (
    create_fee_checkout_session,
    create_subscription_checkout_session,
    retrieve_checkout_session,
    stripe_is_configured,
)
from .subscription_plans import PLANS, plan_for_tier
from .subscription_sync import apply_subscription_from_session
from schools.models import School


@login_required
def fee_list(request):
    """GET /payments/ — parents see their fees; school admins go to school fee manager."""
    if request.user.role == 'school_admin':
        return redirect('payments:school_fees')

    if request.user.role != 'parent':
        return HttpResponseForbidden('Parents only.')

    fees = FeeItem.objects.filter(parent=request.user).select_related('school')
    outstanding = fees.exclude(status=FeeItem.STATUS_PAID)
    paid = fees.filter(status=FeeItem.STATUS_PAID)
    payment_by_fee = {
        p.fee_item_id: p
        for p in Payment.objects.filter(
            parent=request.user, status=Payment.STATUS_COMPLETE,
        )
    }
    paid_rows = [
        {'fee': fee, 'payment': payment_by_fee.get(fee.pk)}
        for fee in paid
    ]

    return render(request, 'payments/fees.html', {
        'outstanding': outstanding,
        'paid': paid,
        'paid_rows': paid_rows,
        'publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        'stripe_configured': stripe_is_configured(),
        **build_portal_context(request, 'School fees', 'Outstanding and paid invoices for your children.'),
    })


@role_required('school_admin')
def school_fees(request):
    """School admin — all students, fee status, and create fees."""
    school = request.user.school
    rows, totals = build_school_fee_overview(school)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'mark_paid':
            fee = get_object_or_404(FeeItem, pk=request.POST.get('fee_id'), school=school)
            fee.status = FeeItem.STATUS_PAID
            fee.save(update_fields=['status'])
            messages.success(request, f'Marked {fee.child_name} — {fee.title} as paid.')
            return redirect('payments:school_fees')

        form = SchoolFeeForm(school, request.POST)
        if form.is_valid():
            student = form.cleaned_data.get('student')
            created = create_fees_for_students(
                school,
                title=form.cleaned_data['title'],
                amount_pence=form.amount_pence(),
                due_date=form.cleaned_data['due_date'],
                student=student,
            )
            messages.success(request, f'Created {len(created)} fee invoice(s).')
            return redirect('payments:school_fees')
    else:
        form = SchoolFeeForm(school)

    ctx = build_portal_context(
        request,
        'School fees',
        'Track payments for all students — set fees and mark cash payments received.',
    )
    from .connect import connect_status
    ctx.update({
        'rows': rows,
        'totals': totals,
        'form': form,
        'student_count': len(rows),
        'connect': connect_status(school),
        'stripe_configured': stripe_is_configured(),
    })
    return render(request, 'payments/school_fees.html', ctx)


@login_required
@require_POST
def create_checkout(request, fee_id):
    """POST /payments/checkout/<id>/ — redirect to Stripe hosted checkout."""
    if request.user.role != 'parent':
        return HttpResponseForbidden('Parents only.')

    fee = get_object_or_404(FeeItem, pk=fee_id, parent=request.user)
    if fee.status == FeeItem.STATUS_PAID:
        messages.info(request, 'This fee is already paid.')
        return redirect('payments:fee_list')

    if not stripe_is_configured():
        messages.error(request, 'Stripe is not configured. Add STRIPE_SECRET_KEY and STRIPE_PUBLISHABLE_KEY to enable payments.')
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


@role_required('school_admin')
def stripe_connect_start(request):
    """Start Stripe Connect Express onboarding for the school."""
    school = request.user.school
    if not stripe_is_configured():
        messages.error(request, 'Stripe is not configured on this server.')
        return redirect('payments:school_fees')

    from .connect import create_connect_onboarding_link
    return_url = request.build_absolute_uri(reverse('payments:connect_return'))
    refresh_url = request.build_absolute_uri(reverse('payments:connect_refresh'))
    try:
        url = create_connect_onboarding_link(
            school=school, return_url=return_url, refresh_url=refresh_url,
        )
        return redirect(url)
    except stripe.error.StripeError as exc:
        messages.error(request, f'Could not start Stripe Connect: {exc}')
        return redirect('payments:school_fees')


@role_required('school_admin')
def stripe_connect_return(request):
    messages.success(request, 'Stripe Connect onboarding submitted — check status on the fees page.')
    return redirect('payments:school_fees')


@role_required('school_admin')
def stripe_connect_refresh(request):
    return stripe_connect_start(request)


@login_required
def payment_receipt(request, payment_id):
    """Printable receipt — use browser Print → Save as PDF."""
    payment = get_object_or_404(
        Payment, pk=payment_id, status=Payment.STATUS_COMPLETE,
    )
    if request.user.role == 'parent' and payment.parent_id != request.user.id:
        return HttpResponseForbidden('Not your receipt.')
    if request.user.role == 'school_admin' and payment.fee_item.school_id != request.user.school_id:
        return HttpResponseForbidden('Not your school.')
    from .receipt import receipt_context
    return render(request, 'payments/receipt.html', receipt_context(payment))


@role_required('school_admin')
def subscription_page(request):
    """School admin — view plans and pay via Stripe Checkout."""
    school = request.user.school
    if not school:
        return redirect('pages:dashboard')

    ctx = build_portal_context(
        request,
        'Subscription',
        'Upgrade your school plan — pay securely with Stripe test mode.',
    )
    ctx.update({
        'plans': PLANS.values(),
        'current_tier': school.subscription_tier,
        'stripe_configured': stripe_is_configured(),
        'payment_history': SubscriptionPayment.objects.filter(
            school=school, status=SubscriptionPayment.STATUS_COMPLETE,
        )[:10],
    })
    return render(request, 'pages/features/subscription.html', ctx)


@role_required('school_admin')
@require_POST
def subscription_checkout(request):
    """POST — start Stripe Checkout for Standard or Premium."""
    if not stripe_is_configured():
        messages.error(request, 'Stripe is not configured on this server.')
        return redirect('pages:subscription')

    tier = request.POST.get('tier')
    plan = plan_for_tier(tier)
    if not plan:
        messages.error(request, 'Invalid plan selected.')
        return redirect('pages:subscription')

    school = request.user.school
    if school.subscription_tier == plan['tier']:
        messages.info(request, f'You are already on the {plan["name"]} plan.')
        return redirect('pages:subscription')

    success_url = (
        request.build_absolute_uri(reverse('payments:success'))
        + '?session_id={CHECKOUT_SESSION_ID}'
    )
    cancel_url = request.build_absolute_uri(reverse('payments:subscription_cancel'))

    try:
        session = create_subscription_checkout_session(
            school=school,
            tier=plan['tier'],
            plan_name=plan['name'],
            amount_pence=plan['amount_pence'],
            success_url=success_url,
            cancel_url=cancel_url,
            customer_email=request.user.email or None,
            admin_user_id=request.user.pk,
        )
        return redirect(session.url, code=303)
    except stripe.error.StripeError as exc:
        messages.error(request, f'Payment could not be started: {exc}')
        return redirect('pages:subscription')


@login_required
def subscription_cancel(request):
    messages.info(request, 'Subscription payment cancelled — no charge was made.')
    return redirect('pages:subscription')


@login_required
def payment_success(request):
    """GET /payments/success/?session_id=... — verify with Stripe, save payment once."""
    session_id = request.GET.get('session_id')
    payment = None
    subscription_payment = None
    redirect_url = 'payments:fee_list'

    if session_id:
        if not stripe_is_configured():
            messages.error(request, 'Stripe is not configured.')
            return redirect('pages:dashboard')

        try:
            session = retrieve_checkout_session(session_id)
            if session.payment_status != 'paid':
                messages.warning(request, 'Payment not completed yet.')
                return redirect('payments:fee_list')

            payment_type = session.metadata.get('payment_type', 'fee')
            if payment_type == 'subscription':
                subscription_payment = _complete_subscription_from_session(session, request.user)
                redirect_url = 'pages:subscription'
                if subscription_payment:
                    messages.success(
                        request,
                        f'Subscription upgraded to {subscription_payment.tier.title()}.',
                    )
            else:
                payment = _complete_fee_from_session(session, request.user)

        except stripe.error.StripeError:
            messages.error(request, 'Could not verify payment with Stripe.')
            return redirect(redirect_url)

    return render(request, 'payments/success.html', {
        'payment': payment,
        'subscription_payment': subscription_payment,
    })


def _complete_fee_from_session(session, user):
    session_id = session.get('id')
    if Payment.objects.filter(stripe_session_id=session_id).exists():
        return Payment.objects.get(stripe_session_id=session_id)

    fee_id = session.metadata.get('fee_item_id')
    if not fee_id:
        return None

    fee = get_object_or_404(FeeItem, pk=fee_id, parent=user)
    payment = Payment.objects.create(
        fee_item=fee,
        parent=user,
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
    from .notifications import notify_platform_fee_payment
    notify_platform_fee_payment(payment)
    return payment


def _complete_subscription_from_session(session, user):
    if user.role == 'school_admin':
        school_id = session.metadata.get('school_id')
        if school_id and str(user.school_id) != str(school_id):
            return None
    payment = apply_subscription_from_session(session)
    return payment


@login_required
def payment_cancel(request):
    """GET /payments/cancel/ — user cancelled on Stripe page."""
    messages.info(request, 'Payment cancelled — no charge was made.')
    return render(request, 'payments/cancel.html')


@csrf_exempt
@require_POST
def stripe_webhook(request):
    """
    POST /payments/webhook/ — Stripe server-to-server events.
    Verifies signature when STRIPE_WEBHOOK_SECRET is set.
    """
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
        payment_type = session.get('metadata', {}).get('payment_type', 'fee')
        if payment_type == 'subscription':
            _mark_subscription_paid_from_session(session)
        else:
            _mark_fee_paid_from_session(session)

    return HttpResponse(status=200)


def _mark_fee_paid_from_session(session):
    """Shared logic for webhook and success page — idempotent by session id."""
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

    payment = Payment.objects.create(
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
    from .notifications import notify_platform_fee_payment
    notify_platform_fee_payment(payment)


def _mark_subscription_paid_from_session(session):
    if session.get('payment_status') and session.get('payment_status') != 'paid':
        return
    apply_subscription_from_session(session)
