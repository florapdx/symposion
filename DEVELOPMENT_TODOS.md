# Tasks Key

Please remove items from list when accomplished, and add items as they come up.

__[B]__: Denotes a beginning-level task

__[A]__: Denotes more advanced tasks

__[O]__: Some tasks are ongoing. These should be performed periodically, but not removed from the list.



## Settings

* [B] : Troubleshoot any problems that may have occurred as result of splitting settings into separate files for different environments (ie, base, local, test, production).

* [B/O] : Double-check that ```local.py``` isn’t being pushed up to Github with user settings and private keys. Remove any that have snuck in.

* [B-A] : Add/implement ```south```? Talk to Steve...

* [B-A] : Implement ```gunicorn``` settings for production? Talk to Steve...



## Sponsorship App

__General__:

* [A] : The Sponsorship app, as it is now, will be buggy if Eventbrite isn’t being used, b/c Eventbrite is so heavily baked into the sponsor-signup and management flows at this point. a) Do we think we won’t want to use Eventbrite in some cases? and, if ‘yes’, b) can we refactor to make the code work either way?


__is\_active filter__:

* [B] : In ```symposion/symposion/templates/sponsorship/_wall.html```, change ```is_active``` filter to ```has_paid```. Figure out where that page appears in your test instance, and ensure that the filter is working. You can change the ‘paid’ status of sponsors in the admin.

* [B] : Check the other templates in  ```symposion/symposion/templates/sponsorship``` and assess whether they are printing sponsor info and assets prematurely. In particular, ensure that ```_list.html_``` and all of the other _\_....html_ files show only paid sponsors. You may need to look into the way that ```level.sponsors``` is being constructed in ```models.py```, and adjust filtering there (ie, if ```is_active``` present, may need to be changed to ```has_paid```).

*  [B] : Run a search (or grep) for the ```is_active``` filter, and assess whether any of those need to be changed to ```has_paid```. Remember that anytime a sponsor’s info or assets appear on the site, they must have already submitted payment (b/c those are benefits of paid sponsorship).


__email integration__:

* [B] : On sponsor signup, an email is generated and sent to every contact listed by that sponsor (ie, as defined in the model: ```primary, invoice, and graphics```). The only one of these contacts that is required to enter on signup is the ```primary``` contact, and this person may thus leave ```invoice``` and ```graphics``` contact fields blank. Right now, confirmation emails are going out to all contacts, even if those fields were left blank (ie, emails are being sent to invoice and graphics as empty string). Locate the ```send_email``` method in the ```apply``` and ```add``` views in ```sponsorship/views.py``` and write the code to guard against sending email to empty strings.

* [B] : Double-check with Steve and Pat the copy for all of the sponsorship-related emails in the email templates directory. Make any changes they request.

* [A] : Once a sponsor has signed up and been activated by a staff member, if that sponsor has not paid after _x_ amount of time, that sponsor should continue to receive reminders until a) they pay, b) they are deactivated by staff.

* [A] : Along the same lines, once a sponsor has been paid, if they’ve yet to add/upload any of their benefits within a certain timeframe (or time-to-event), write the code to generate and send an email reminder noting the missing assets. Check with Steve and Pat on the timeline.



## Documentation

* [B] : Add documentation for staff users (ie, the staff that will be using the software) what how to sign up/manage sponsors using the new interface (for the cases where the sponsor doesn’t want to sign up themselves for whatever reason).

* [B] : Add to the ```symposion/docs/sponsorship.rst``` docfile documentation on implementing and using the Eventbrite integrations we’ve added so far — ie, ability to generate free passes and new sponsor signup workflow. Ensure that all of the Eventbrite additions to the ```settings/local.py``` (and, ultimately, to _settings/production.py_) are properly documented (ie, how to obtain credentials, and what goes where.)  Important!: Make sure that it’s made clear that, as the code in the Sponsorship app is set up now, we must be using Eventbrite for our events. Not using Eventbrite and properly configuring in Settings will produce errors. (See ‘general’ under Sponsorship above.)

* [B] : Every file in the ```symposion/docs``` directory needs fleshing out. In particular, note any methods, tags, filters, and/or properties that are used in the code. Also, as you’re working, keep track of and try to document any parts of the codebase that are particularly difficult to follow. A little explanation for future devs will go a long way!

* [A] : _Depends on setting up a test event site in symposion from scratch_. Set up a test event site in symposion from scratch, adding some dummy pages to ```symposion/symposion_project```. Document the entire process, including step-by-step instructions for how to set up site and any ‘gotchas’ that come up. Important! : remember that if prompted at any time to delete ‘stale or unused’ table ‘reviews | review’, choose ‘no’. Choosing ‘yes’ renders the Teams app unusable.

* [A] : Is there any way to avoid the aforementioned ```Teams app``` gotcha and improve the usability of the app? Come up with a plan and execute.

* [B-A/O]: Add to, correct, amend the ```DEVELOPMENT_README.md``` and any other developer-facing docs as needed.

* [B-A/O]: While not pertaining solely to Symposion development, the workflow docs (contained in the "DevTeam-TheOpenBastion/Internal_docs" repo) are in need of editing and amendment. If you're decently handy with Git, consider passing that knowledge along.



## Dashboard

__Eventbrite for users__:

* [A] : Discuss with Steve and Pat integrating user ticket-purchasing into site, and most probably to the Dashboard interface. Follow the lead for sponsorship purchases to integrate a view that allows user to purchase tickets and then print those tickets to that user’s dashboard.

* [O] : Is there any other info that we should reveal to the user here?

* [A+] : Discuss feasibility of adding ability for user to manage schedule through dashboard — ie, select events from schedule view and print them to dash for customized user schedule. [Erase if feature not desired.]



## General Improvements

* [A+] : _For the experienced only!_ Upgrade versions in requirements; most notably, to ```Django 1.5```. This will require a fair bit of refactoring of the codebase. See Caktus Group’s PyCon repo for guidance.

* [A] : Change out the ```markitup``` WYSIWYG editor that’s being used. Again, see Caktus repo as one example of switching over.


