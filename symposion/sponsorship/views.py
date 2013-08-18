from zipfile import ZipFile, ZIP_DEFLATED
import StringIO #as StringIO
import os
import json
import eventbrite
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.conf import settings

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from symposion.sponsorship.forms import SponsorApplicationForm, SponsorDetailsForm, SponsorBenefitsFormSet, SponsorPassesForm
from symposion.sponsorship.models import Sponsor, SponsorBenefit
from symposion.utils.mail import send_email


@login_required
def sponsor_apply(request):
    if request.method == "POST":
        form = SponsorApplicationForm(request.POST, user=request.user)
        if form.is_valid():
            sponsor = form.save()
            staff_members = User.objects.filter(is_staff=True)
            message_ctx = {
                "sponsor": sponsor,
            }
            for staff in staff_members:
                staff_email = staff.email
                send_email(
                    [staff_email], "sponsor_signup",
                    context = message_ctx
                )
            return redirect("sponsor_detail", pk=sponsor.pk)
    else:
        form = SponsorApplicationForm(user=request.user)

    return render_to_response("sponsorship/apply.html", {
        "form": form,
    }, context_instance=RequestContext(request))


@login_required
def sponsor_add(request):
    if not request.user.is_staff:
        raise Http404()

    if request.method == "POST":
        form = SponsorApplicationForm(request.POST, user=request.user)
        if form.is_valid():
            sponsor = form.save(commit=False)
            sponsor.save()
            return redirect("sponsor_detail", pk=sponsor.pk)
    else:
        form = SponsorApplicationForm(user=request.user)

    return render_to_response("sponsorship/add.html", {
        "form": form,
    }, context_instance=RequestContext(request))


@login_required
def sponsor_detail(request, pk):
    sponsor = get_object_or_404(Sponsor, pk=pk)

    if not request.user.is_staff:
        if sponsor.applicant != request.user:
            return redirect("sponsor_list")

    formset_kwargs = {
        "instance": sponsor,
        "queryset": SponsorBenefit.objects.filter(active=True)
    }

    if request.method == "POST":

        form = SponsorDetailsForm(request.POST, user=request.user, instance=sponsor)
        formset = SponsorBenefitsFormSet(request.POST, request.FILES, **formset_kwargs)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()

            messages.success(request, "Sponsorship details have been updated")

            return redirect("dashboard")
    else:
        form = SponsorDetailsForm(user=request.user, instance=sponsor)
        formset = SponsorBenefitsFormSet(**formset_kwargs)

    return render_to_response("sponsorship/detail.html", {
        "sponsor": sponsor,
        "form": form,
        "formset": formset,
    }, context_instance=RequestContext(request))


@login_required
def sponsor_passes(request):
    if not request.user.is_staff:
        raise Http404()

    # only execute if Eventbrite is being used for this conference
    if not settings.EVENTBRITE == True:
        messages.error("We're sorry, Eventbrite isn't being used for this conference.")
    elif settings.EB_APP_KEY == '' or settings.EB_USER_KEY == '' or settings.EB_EVENT_ID == '':
        messages.error("Eventbrite client has not been configured properly in settings. Please contact conference organizer about this issue.")
    else:
        # get eventbrite credentials from settings
        eb_event_id = settings.EB_EVENT_ID
        eb_auth_tokens = {
            'app_key': settings.EB_APP_KEY,
            'user_key': settings.EB_USER_KEY
        }
        # initiate client with credentials and grab event data
        eb_client = eventbrite.EventbriteClient(eb_auth_tokens)
        response = eb_client.event_get({
            'id': eb_event_id
            })

        # We'll need the event name and url for our email
        event_title = response['event']['title']
        event_url = response['event']['url']

        # get ticket choices for this event and make list for form display
        TICKET_CHOICES = []
        tickets = response['event']['tickets']
        for tkt in tickets:
            ticket = tkt['ticket']
            try:
                price = ticket['price']
            except KeyError:
                price = '0'

        # Don't include tickets of type 'donation' (== 1; fixed-price tickets are type 0)
            if ticket['type'] != 1:
                TICKET_CHOICES.append(((ticket['name'], price), ticket['name'] + ' -- $' + price))

        # make a list of *active* sponsors to add to our form
        SPONSOR_CHOICES = []
        for sponsor in Sponsor.objects.filter(active=True):
            SPONSOR_CHOICES.append((sponsor, sponsor))


        if request.method == "POST":
            form = SponsorPassesForm(request.POST, tickets=TICKET_CHOICES, sponsors=SPONSOR_CHOICES)
            if form.is_valid():
                sponsor = form.cleaned_data["sponsor"]
                ticket_type_id = 0
                discount_code = str(sponsor[:5] + '_' + ticket[:5])

                # grab the list of existing discounts to check against
                response = eb_client.event_list_discounts({
                    'id': eb_event_id
                    })

                # Alert user if discount already exists, and reset form
                for discount in response['discounts']:
                    if discount['code'] == discount_code:
                        messages.error(response, "Oops, looks like that discount already exists")
                        return redirect('')
                    else:
                        # generate eventbrite request
                        response = eb_client.discount_new({
                            'event_id': eb_event_id,
                            'code': discount_code,
                            'amount_off': int(form.cleaned_data["amount_off"]),
                            'quantity_available': int(form.cleaned_data["number_of_passes"]),
                            'tickets': ticket_type_id,
                        })

                # send auto-email to sponsor contact
                    for sponsor in Sponsor.objects.filter(name = sponsor):
                        contact_name = sponsor.contact_name
                        contact_email = sponsor.contact_email

                    message_ctx = {
                        "event_name": event_title,
                        "sponsor": sponsor,
                        "contact_name": contact_name,
                        "discount_code": discount_code,
                        "event_url": event_url,
                    }
                    send_email(
                    [contact_email], "sponsor_passes",
                    context = message_ctx
                )

                return redirect("dashboard")
        else:
            form = SponsorPassesForm(sponsors=SPONSOR_CHOICES, tickets=TICKET_CHOICES)

        return render_to_response("sponsorship/passes.html", {
            "form": form,
        }, context_instance=RequestContext(request))


# with print logos and json reformat
@login_required
def export_sponsors(request):
    if not request.user.is_staff:
        raise Http404()

    # use StringIO to make zip in memory, rather than on disk
    f = StringIO.StringIO()
    z = ZipFile(f, "w", ZIP_DEFLATED)
    data = []

    # collect the data and write web and print logo assets for each sponsor
    for sponsor in Sponsor.objects.all():
        data.append({
            "name": sponsor.name,
            "website": sponsor.external_url,
            "description": sponsor.listing_text,
            "contact name": sponsor.contact_name,
            "contact email": sponsor.contact_email,
            "level": str(sponsor.level),
            }),
        if sponsor.website_logo:
            path = sponsor.website_logo.path
            z.write(path, str(sponsor.name).replace(" ", "")+"_weblogo"+os.path.splitext(path)[1])
        if sponsor.print_logo:
            path = sponsor.print_logo.path
            z.write(path, str(sponsor.name).replace(" ", "")+"_printlogo"+os.path.splitext(path)[1])

    # write sponsor data to text file for zip
    with open("sponsor_data.txt", "wb") as d:
       json.dump(data, d, encoding="utf-8", indent=4)
    z.write("sponsor_data.txt")

    z.close()

    response = HttpResponse(mimetype = "application/zip")
    response["Content-Disposition"] = "attachment; filename=sponsor_file.zip"
    f.seek(0)
    response.write(f.getvalue())
    f.close()
    return response
