Schedule App
===========

The Schedule app provides the functionality necessary for planning and publishing conference schedules. Most conferences will contain more than one "schedule", one for each section type--talks, tutorials, posters, etc.--and each schedule will be made up of one or more "slot"--defined by day, slot kind, and start and end times.

Models
---------

Schedule
~~~~~~~~~

A schedule has the following attributes: section, published, and hidden (Boolean).

Day
~~~~

Contains a date and a foreign-key to a schedule; meta class also defines "unique_together" for schedule and date.

Room
~~~~~

Contains foreign-key to a schedule and has a name and order (as a positive integer value).

SlotKind
~~~~~~~~~

Represents what kind a slot is--ie, 3-hr tutorial, 1hr talk, 45min talk, break, lunch, etc.
Has a label and a foreign-key to a schedule.

Slot
~~~~~

A slot is the basic unit of a schedule and has a day, kind, start (time), end (time), and a markup field for content overrides. Model methods include assign()--to assign the given content to the slot--and unassign()--to unassign content from the slot. The slot model also has properties "content" (ie, the presentations associated with the slot), and "rooms" (returning the rooms associated with the slot.)

SlotRoom
~~~~~~~~~

Links a slot with a room.

Presentation
~~~~~~~~~~~~~~

Once a proposal is accepted, it begins a new life as a presentation. A presentation has a title, slot, description, abstract, speaker, additional speakers, section, status ("cancelled"), and proposal object ("proposal_base"). Presentations also have properties number and proposal.


Use of Schedule app
---------------------

Use of the schedule app primarily takes place through the admin interface. See below for special note on editing presentations below.


A Note About Editing Presentations v. Proposals
-------------------------------------------------

Once a proposal becomes a presentation, any changes that need to be made need to be made directly to the presentation (and not to the proposal in the dashboard). In order to do this, logged-in staff users will need to navigate to the presentation detail page on the website (most likely by selecting the talk to be edited from the conference schedule page), and click the "Edit" button. This will reveal the presentation in a form, which can then be edited--including the inclusion and deletion of additional speakers (follow instructions to select one or more; deselect and save to remove a speaker). Once changes to the presentation have been saved, they will be reflected in the presentation on the conference site as well as in instances of the proposal in the dashboard.
