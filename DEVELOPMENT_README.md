## Overview

Symposion is a software platform for publicizing and managing events. It runs on Django, and includes dependencies and apps originally developed by [Eldarion](http://eldarion.com/). Their version of the project can be found [on Github](https://github.com/pinax/symposion).

The version of the project being maintained by The Open Bastion in our [public repo](https://github.com/TheOpenBastion/symposion) contains modifications and features that, while possibly useful for other organizations, are driven by our organization’s specific needs. These include (so far):

* Exporting routine event-management tasks from the admin to the dashboard
* Integrating Eventbrite (generating discount codes and selling sponsorships)
* Re-engineering the directory structure for current dev-stage-deploy routines (incl. separate files for base, local, testing, and production settings and requirements)
* Adding documentation as much as possible and wherever most needed to cover Eldarion’s source code, and adding complete documentation for any new features/changes we add/make to the codebase
* Making various other usability improvements


## Project Structure

The Symposion directory tree, in essence, looks something like this:

    —symposion
        —docs
        —requirements
        —tests
        —symposion_project
            —settings
            —static
            —etc...
        —symposion
            —proposals
            —reviews
            —sponsorship
            —etc...



The important thing to note here is that _symposion_ and _symposion\_project_ contain different sets and kinds of files.

Any modifications to the codebase that are meant to persist throughout future project sites (ie, specific implementations of the software for different conference and event sites), should be made in [TheOpenBastion/symposion repo](https://github.com/TheOpenBastion/symposion). In general, these modifications will be made to files contained in the ```symposion/symposion``` directory.

The ```symposion/symposion_project``` directory, on the other hand, contains files that are pertinent to specific project implementations and should be developed in repositories produced specifically for individual events. One notable exception to this rule is the ```symposion/symposion_project/settings``` directory, which contains all of our settings files. These files will likely be modified from time to time, as needed. Additionally, you may need to add CSS here and there in ```symposion/symposion_project/static/symposion/css```.


## Development of Symposion software itself


### Apps:
The following apps appearing in ```symposion/symposion``` are most likely to be the focus of development efforts:

* _Reviews_: app that handles user reviews of presenter proposals
* _Schedule_: app that handles auto-creation of conference schedule (and contains _presentation_ model, which represents accepted proposals)
* _Speakers_: handles the management of presenters
* _Sponsorship_: app that handles creation of sponsorships, sponsor levels, and sponsor benefits; contains Eventbrite integrations
* _Teams_: app that handles the creation and management of teams of reviewers



### Files:
Each app contains the following files:

* [__models.py__](https://docs.djangoproject.com/en/1.4/topics/db/models/): Models the data to be stored in the database. A model will generally contain a number of attributes, each of which is defined by a data type that’s been built into Django (ex, CharField, PositiveIntegerField, BooleanField, ForeignKey), and that may or may not additionally contain one or more args (arguments) and kwargs (keyword arguments). Models may also contain...
    * [_Meta classes_](https://docs.djangoproject.com/en/1.4/ref/models/options/): Meta classes allow you to define the way modeled data will be represented in your application and in the admin; common use is to alphabetize, or to convert hashed usernames to last_name, etc
    * [_@property_](http://docs.python.org/2/library/functions.html#property): definitions that are callable in the same way as any attribute of that model (ie, model.property); if you find yourself making the same multi-step query over and over again (say to get all ids of a foreignKey on a set of model instances that conform to a certain criteria), creating an @property representing that query is usually the way to go
    * [_model methods_](https://docs.djangoproject.com/en/1.4/topics/db/models/#model-methods): like @property definitions, except for abstracting the processing of model information instead of creating new kinds of data


* [__views.py__](https://docs.djangoproject.com/en/1.4/topics/http/views/): Contains the application logic. Your views essentially do two things: receive requests from the user (or other pieces of code), and send responses containing any data that you’ve made available in your view code (passing that data to templates or to other views, or redirecting the user to another page, etc). Most of your energies will be focused here.


* [__forms.py__](https://docs.djangoproject.com/en/1.4/topics/forms/): Contains the code that defines your forms, generating the fields (if form) or fields-as-forms (if formset). Any pre-processing of form data, such as changing of data types and/or defining special validation methods, is part of this file as well.


* [__admin.py__](https://docs.djangoproject.com/en/1.4/ref/contrib/admin/): Contains the code that defines the fields that appear in the Django admin. Remember: any new attributes that you might add to a model should also be added as a field in that model’s corresponding modelAdmin.

* [__urls.py__](https://docs.djangoproject.com/en/1.4/topics/http/urls/#id2): The urls.py file in each app contains url patterns that correspond to each of your app’s views. Each pattern is made up of a regex matching pattern, a corresponding view to call when a url is matched to that pattern, and (probably) a name=’’ clause. The name clause is used in the {% url <name clause> %} template tag, and mitigates against the case where two url patterns might call the same view (ie, this is why the name=’’ sometimes is and sometimes isn’t the same as the name of the view).

* [__templatetags directory__](https://docs.djangoproject.com/en/1.4/howto/custom-template-tags/) Directory containing custom template tags and filters that are being used in our templates (ex, {{ sponsor | is_active }}.


### Templates

Note that among the apps contained in ```symposion/symposion``` is a directory called ```templates```. The ```templates``` directory contains a directory of \<html> templates for each app, plus, most notably, ```dashboard.html``` and ```emails``` (contains another set of directories of subject and message email templates belonging to each of our apps.)

__Using Django templates__:

Django [templates](https://docs.djangoproject.com/en/1.4/topics/templates/) are, in general, relatively easy to learn to use. The most important things to remember are:

* Most templates will {% extend a\_parent\_template %} at the top of the page, and then will wrap code to be inserted in those parent templates in ```{% block %}{% endblock %}``` tags, per their definition in the parent (ie, {% block content %}, etc.).
* Use {% syntax %} for logic:
    * ```{% for x in y %}...{% endfor %}```
    * ```{% if x in y %}...{% endif %}```
* Use {{ syntax }} for variables:
    * ex: ```<label>{{ name }}</label>```
* You only have access to {{ variables }} in your templates that you a) pass in through your view’s _render_ method, or b) define in a template tag. You can pass in model instances, however, and then call their attributes (ex: pass ```sponsor``` in through ```render_to_response``` in view, and then call ```{{ sponsor.name }}``` in template).
* Use _filters_ to filter data as needed (this is most often used to specify data that meets a certain status criterion (ie, all _active_ sponsors or all _staff_ users).

Because proportionally more time is spent by the program rendering them, it’s generally good practice to keep as much logic as possible out of your templates (ie, handle as much as you can in your views).


### Testing
__Types of testing__:

* _Unit testing_: tests the individual components of a program, such as particular methods
* _Integration testing_: tests the interactions among various components (units and systems) of a program
* _Functional testing_: test the functionality of a program from the user’s point of view (for the most part)
* _User-testing_: Unlike the above, isn’t automated; this is essentially been the method of testing thus far (and usually by the same person developing the software). Ideally, you’ll be working on automated tests in the near future.


__Running a local email server__:

In _symposion\_project/settings/local.py, edit EMAIL settings:

```
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = ‘localhost’
EMAIL_PORT = 1025
```

Enter in a new Terminal window (no virtualenv required):

```python -m smtpd -n -c DebuggingServer localhost\:1025)```

You won’t see anything printed to the Terminal after hitting ‘enter’, which is fine—keep it open. As you are testing your code, any email successfully generated by your views will print to this window. Note: each email will print twice—once in plaintext and once in html.


__Eventbrite test accounts__:

Eventbrite is integrated into the _Sponsorship_ app in our version of Symposion, and any modifications and additions to this functionality will require testing against a live Eventbrite account. I’ve found the following to be helpful:

* Sign up for Eventbrite with your own email and password, and create a _PRIVATE_ event called TestCon (or something similar). Create a variety of tickets for the event (ex: Full Pass, Half Pass, Early Bird, Student, Single Event, Donation, etc.). As long as you have selected the option to make your event private, it will not be findable or accessible by anyone else (unless you explicitly invite them). Keep the Eventbrite page up in your browser

* In your Eventbrite account’s settings, generate an ```app_key``` and a ```user_key```. Copy these and add them to the ```symposion_project/settings/local.py``` file under ```EB_APP_KEY``` and ```EB_USER_KEY```. Next, make sure you’re on a page pertaining to your private event on Eventbrite (“Edit” or “Manage”, for example). Take note of the number in the URL following ```eid=```. This number is your event’s id. Copy and paste into ```symposion_project/settings/local.py``` under ```EB_EVENT_ID```.

Next, when you’re fairly confident that you have your feature working as it should, see if you can make a copy of a real event being run by The Open Bastion (search for instructions on doing this if needed). Make sure the event copy is set to private, and make sure to change the EB settings in _local.py_.



## Developing a Symposion-based site for a conference or other event


If you are part of a team that is working on an instance of the software for a specific event, you’ll want to copy the source code contained in our public repo over into a private repo, named for the event. So, for example, if you’re tasked with building a symposion-based site for DjangoCon:

* create a new repo on Github __in our DevTeam-TheOpenBastion__ account (!important) named something like ‘DjangoCon2014’, and mark it as _private_. Github will ask you if you want to initiate the project with a README—selecting ‘yes’ will cause a merge conflict later, so select ‘no’.
* cd to whichever directory on your local machine _contains_ the top-level symposion directory and:

```

    # Copy symposion source code over into event project directory
    $ cp symposion <path/_to/_DjangoCon/_project/_directory/symposion>

    # change directories so that you’re inside the top level of this new symposion project:
    $ cd <path/_to/_DjangoCon/_project/_directory/symposion>

    # initiate a new repository
    $ git init

    # set origin to match the repository that you created on Github for this project
    # Note: the git address you enter will be different depending on the name you give your repository and whether or not you are using SSH$ git remote add origin https://github.com/DevTeam-TheOpenBastion/DjangoCon2014

    # Push this new repository up to your empty repo on Github
    $ git push -u origin master

```

You should now have a separate repository and codebase for developing for the specific conference or event, and one that is _private_ on Github (important!).

At this point you will want to form a team and assign permissions, or add an existing team to the repository on our Github account. Do so by accessing the “Settings” menu to the right of the repo page (crossed-tools symbol) and clicking “Collaborators” from the menu on the left of the resulting page. Select the team members (or invite others not already listed), and be sure to add the repository to that team. By creating a team, you will all have access to the codebase and will receive email updates from github every time a commit is made to the repo or pull request is issued.


### Special Notes:

* As it stands now, there isn’t proper (any?) documentation on setting up an event site in symposion, as the _symposion\_project_ directory (among other things) isn’t documented. We aim to fix this situation in the coming months (see “Symposion To Do List”).

* Important! Read the documentation on setting up the Teams app on startup at ```symposion/docs/teams.rst```, which will explain how to run the command line tool to set up this functionality. Once completed, if at any time in the course of development/deployment you are prompted to drop ‘stale or unused’ table ‘Reviews | Review’, respond by typing ‘no’. Entering ‘yes’ will disable the Teams functionality. Most likely to happen on ‘syncdb’ or during migrations.

