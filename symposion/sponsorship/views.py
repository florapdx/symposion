from zipfile import ZipFile, ZIP_DEFLATED
import StringIO #as StringIO
import os
import json
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from symposion.sponsorship.forms import SponsorApplicationForm, SponsorDetailsForm, SponsorBenefitsFormSet
from symposion.sponsorship.models import Sponsor, SponsorBenefit


@login_required
def sponsor_apply(request):
    if request.method == "POST":
        form = SponsorApplicationForm(request.POST, user=request.user)
        if form.is_valid():
            sponsor = form.save()
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
        try:
            logo = sponsor.website_logo
            path = logo.path
            z.write(path, str(sponsor.name)+"_weblogo"+os.path.splitext(path)[1])
        except AttributeError:
            pass
        try:
            print_logo = sponsor.print_logo
            path = print_logo.path
            z.write(path, str(sponsor.name)+"_printlogo"+os.path.splitext(path)[1])
        except AttributeError:
            pass

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
