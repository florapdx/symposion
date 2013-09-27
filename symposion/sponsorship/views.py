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
from symposion.sponsorship.models import Sponsor, BenefitLevel, SponsorBenefit, SponsorLevel
from symposion.utils.mail import send_email

## Note: We really need to collapse these two views (add/apply) if possible--not DRY
@login_required
def sponsor_apply(request):

    CHOICES = []
    for s in SponsorLevel.objects.all():
        CHOICES.append(( s, s.name + ': ' + ', '.join([b.benefit.name for b in BenefitLevel.objects.filter(level = s)]) ))

    if request.method == "POST":
        form = SponsorApplicationForm(request.POST, user=request.user, choices=CHOICES)
        if form.is_valid():
            sponsor = form.save()

            event_name = settings.EVENT_NAME
            event_website = settings.EVENT_WEBSITE
            event_email = settings.EVENT_EMAIL
            event_phone = settings.EVENT_PHONE

            message_ctx = {
                "sponsor": sponsor,
                "event_name": event_name,
                "event_website": event_website,
                "event_email": event_email,
                "event_phone": event_phone
            }

            for c in sponsor.sponsor_contacts:
                sponsor_email = c
                send_email(
                    [sponsor_email], "sponsor_signup_conf",
                    context = message_ctx
                )
            staff_members = User.objects.filter(is_staff=True)
            for staff in staff_members:
                staff_email = staff.email
                send_email(
                    [staff_email], "sponsor_signup",
                    context = message_ctx
                )
            return redirect("sponsor_detail", pk=sponsor.pk)
    else:
        form = SponsorApplicationForm(user=request.user, choices=CHOICES)

    return render_to_response("sponsorship/apply.html", {
        "form": form,
    }, context_instance=RequestContext(request))


@login_required
def sponsor_add(request):
    if not request.user.is_staff:
        raise Http404()

    CHOICES = []
    for s in SponsorLevel.objects.all():
        CHOICES.append(( s, s.name + ': ' + ', '.join([b.benefit.name for b in BenefitLevel.objects.filter(level = s)]) ))

    if request.method == "POST":
        form = SponsorApplicationForm(request.POST, user=request.user, choices=CHOICES)

        if form.is_valid():
            sponsor = form.save(commit=False)
            sponsor.save()

            event_name = settings.EVENT_NAME
            event_website = settings.EVENT_WEBSITE
            event_email = settings.EVENT_EMAIL
            event_phone = settings.EVENT_PHONE

            message_ctx = {
                "sponsor": sponsor,
                "event_name": event_name,
                "event_website": event_website,
                "event_email": event_email,
                "event_phone": event_phone
            }

            for c in sponsor.sponsor_contacts:
                sponsor_email = c
                send_email(
                    [sponsor_email], "sponsor_signup_conf",
                    context = message_ctx
                )
            staff_members = User.objects.filter(is_staff=True)
            for staff in staff_members:
                staff_email = staff.email
                send_email(
                    [staff_email], "sponsor_signup",
                    context = message_ctx
                )
            return redirect("sponsor_detail", pk=sponsor.pk)
    else:
        form = SponsorApplicationForm(user=request.user, choices=CHOICES)

    return render_to_response("sponsorship/add.html", {
        "form": form,
    }, context_instance=RequestContext(request))


## Not DRY. Can we pull the checks and code generation, etc out into helper function?
## ex, eventbrite_check() helper function, which we'd put in utils and import from there...
@login_required
def sponsor_detail(request, pk):
    sponsor = get_object_or_404(Sponsor, pk=pk)

    if not request.user.is_staff and request.user.email not in sponsor.sponsor_contacts:
        return redirect("sponsor_list")

    if not sponsor in Sponsor.objects.filter(active=True) and not request.user.is_staff:
        messages.warning(request, "Thank you for your interest. Your sponsorship is pending approval. We'll be in touch soon.")
        return redirect("dashboard")

    # The non-staff user should never see these types of error messages...figure something out
    # Turn back if eventbrite not being used or if config data missing from settings
    if not settings.EVENTBRITE == True:
        messages.error(request, "We're sorry, Eventbrite isn't being used for this conference.")
        return redirect('details')

    elif settings.EB_APP_KEY == '' or settings.EB_USER_KEY == '' or settings.EB_EVENT_ID == '':
        messages.error(request, "Eventbrite client has not been configured properly in settings. Please contact conference organizer about this issue.")
        return redirect('details')

    else:
        if not sponsor.paid:
            level = sponsor.level

            # grab authentication credentials
            eb_event_id = settings.EB_EVENT_ID
            eb_auth_tokens = {
                'app_key': settings.EB_APP_KEY,
                'user_key': settings.EB_USER_KEY
            }

            # Initialize client
            eb_client = eventbrite.EventbriteClient(eb_auth_tokens)

            # Make request for basic event and ticket info
            response = eb_client.event_get({
                'id':eb_event_id,
            })

            event_url = response['event']['url']
            tickets = response['event']['tickets']

            for tckt in tickets:
                if str(level) in tckt['ticket']['name']:
                    ticket_id = tckt['ticket']['id']

            code = str(level) + '_Sponsor'

            ## First check to see if code exists as access code on EB
            ## if not, handle exception and create new access code
            try:
                access_codes = eb_client.event_list_access_codes({'id': eb_event_id})
            except EnvironmentError:
                # if no access codes registered at all...
                add_new_code = eb_client.access_code_new({
                    'event_id': eb_event_id,
                    'code': code,
                    'tickets': ticket_id
                })
                access_codes = eb_client.event_list_access_codes({'id': eb_event_id})

            codes_list = [cd['access_code']['code'] for cd in access_codes['access_codes']]

            if not code in codes_list:
                new_code = eb_client.access_code_new({
                    'event_id': eb_event_id,
                    'code': code,
                    'tickets': ticket_id
                })

            ## Construct url for user to add to template
            eb_ticket_url = event_url.rstrip('?ref=ebapi') + '?access=' + code

        else:
            # If already paid, pass empty value to avoid error on render_to_response
            eb_ticket_url = ''

    formset_kwargs = {
        "instance": sponsor,
        "queryset": SponsorBenefit.objects.filter(active=True)
    }

    if request.method == "POST":

        form = SponsorDetailsForm(request.POST, user=request.user, instance=sponsor)
        formset = None

        if form.is_valid():
            form.save()
            messages.success(request, "Sponsorship details have been updated")
            return redirect("sponsor_detail", pk=sponsor.pk)

        if sponsor in Sponsor.objects.filter(active=True):
            formset = SponsorBenefitsFormSet(request.POST, request.FILES, **formset_kwargs)
            if formset.is_valid():
                formset.save()
                messages.success(request, "Sponsorship benefits have been updated")
                return redirect("sponsor_detail", pk=sponsor.pk)

    else:
        form = SponsorDetailsForm(user=request.user, instance=sponsor)
        formset = SponsorBenefitsFormSet(**formset_kwargs)

    benefits = [b.benefit for b in sponsor.sponsor_benefits.all()]

    return render_to_response("sponsorship/detail.html", {
        "sponsor": sponsor,
        "form": form,
        "formset": formset,
        "benefits": benefits,
        "eb_ticket_url": eb_ticket_url
    }, context_instance=RequestContext(request))



@login_required
def eventbrite_confirm(request):
    user = request.user
    for spsr in Sponsor.objects.filter(active=True):
        if user.email in spsr.sponsor_contacts:
            sponsor = spsr
            if not request.GET['oid'] == '':
                    sponsor.paid = True
                    sponsor.save()
            return redirect("sponsor_detail", pk=sponsor.pk)
        elif user.is_staff:
            messages.warning(request, "Remember to set paid to 'True' in admin for this sponsor.")
            return redirect("dashboard")


@login_required
def sponsor_passes(request):
    if not request.user.is_staff:
        raise Http404()

    # Turn back if eventbrite not being used or if config data missing from settings
    if not settings.EVENTBRITE == True:
        messages.error(request, "We're sorry, Eventbrite isn't being used for this conference.")
        return redirect('dashboard')
    elif settings.EB_APP_KEY == '' or settings.EB_USER_KEY == '' or settings.EB_EVENT_ID == '':
        messages.error(request, "Eventbrite client has not been configured properly in settings. Please contact conference organizer about this issue.")
        return redirect('dashboard')
    else:
        # grab authentication credentials
        eb_event_id = settings.EB_EVENT_ID
        eb_auth_tokens = {
            'app_key': settings.EB_APP_KEY,
            'user_key': settings.EB_USER_KEY
        }

        # Make first request for basic event and ticket info
        eb_client = eventbrite.EventbriteClient(eb_auth_tokens)
        response = eb_client.event_get({
            'id': eb_event_id
            })

        # Make choices list of ticket names and prices for our form
        TICKET_CHOICES = []
        ticket_dict = {}
        tickets = response['event']['tickets']
        for tkt in tickets:
            ticket = tkt['ticket']
            # don't include donation ('type' == 1) tickets
            if ticket['type'] != 1:
                ticket_name = ticket['name']
                ticket_id = ticket['id']
                price = ticket['price']

            # Make dict of name/id pairs for discount generation
                ticket_dict[ticket_name] = ticket_id

            # Make our choices list for form
                TICKET_CHOICES.append(( ticket_name, ticket_name + ' -- $' + price ))

        # Next, make a list of *active* sponsors to add to our form
        SPONSOR_CHOICES = []
        for sponsor in Sponsor.objects.filter(active=True):
            SPONSOR_CHOICES.append((sponsor, sponsor))

        # we also need event title and url for our email
        event_title = response['event']['title']
        event_url = response['event']['url']


        # If form is valid, process form and generate discount
        if request.method == "POST":
            form = SponsorPassesForm(request.POST, tickets=TICKET_CHOICES, sponsors=SPONSOR_CHOICES)

            if form.is_valid():
                sponsor = form.cleaned_data["sponsor"]
                ticket_names = form.cleaned_data["ticket_names"]
                amount_off = form.cleaned_data["amount_off"]
                percent_off = form.cleaned_data["percent_off"]

                # match selected ticket types to ticket ids from our dict
                tickets_list = ','.join(str(v) for k, v in ticket_dict.iteritems() if k in ticket_names)


                # Eventbrite will only accept one of the following: amount_off or percent_off
                # Create variables to pass into our request one or other depending on staff input
                if amount_off != None and percent_off == None:
                    discount_n = 'amount_off'
                    discount_v = amount_off
                elif percent_off != None and amount_off == None:
                    discount_n = 'percent_off'
                    discount_v = percent_off

                # Generate discount code
                discount_code = (sponsor[:6] + '_' + event_title[:6]).replace(' ', '')

                # Alert user if discount already exists
                # Except case where no discounts exist to check against
                try:
                    response = eb_client.event_list_discounts({
                        'id': eb_event_id
                    })
                    for dsct in response['discounts']:
                        discount = dsct['discount']
                        if discount['code'] == discount_code:
                            messages.error(request, "Oops, looks like that discount code already exists")
                            return redirect("sponsor_passes")

                except EnvironmentError:
                    response = ''
                    pass

                # Send request to eventbrite to register the discount code w/params
                response = eb_client.discount_new({
                    'event_id': eb_event_id,
                    'code': discount_code,
                    discount_n : discount_v,
                    'quantity_available': int(form.cleaned_data["number_of_passes"]),
                    'tickets': tickets_list
                })

                # Auto-email to sponsor contact with discount code
                for spsr in Sponsor.objects.filter(name = sponsor):
                    contact_name = spsr.contact_name
                    contact_email = spsr.contact_email

                event_email = settings.EVENT_EMAIL
                event_phone = settings.EVENT_PHONE

                message_ctx = {
                    "event_name": event_title,
                    "sponsor": sponsor,
                    "contact_name": contact_name,
                    "discount_code": discount_code,
                    "event_url": event_url,
                    "event_contact_email": event_email,
                    "event_contact_phone": event_phone
                }
                send_email(
                    [contact_email], "sponsor_passes",
                    context = message_ctx
                )

                messages.success(request, "Discount code was generated and has been emailed to sponsor contact")

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
