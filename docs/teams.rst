Teams App
==========

****Teams functionality needs to be enabled by running command in terminal and by correctly setting up a PostgreSQL database. See "Usage Notes" below.****

Models
------


Team
~~~~~~

Models team objects with manager and member permissions fields and associated methods to handle different member type (applicant, invitee, member, manager). In addition to permissions M2M field, every team has a slug, name, description, and access type. Default access types are: "open": anyone can automatically join team
"application": anyone can apply to join a team
"invite": users must be invited to join team (by entering email address)


Membership
~~~~~~~~~~~~

Each team member has a user, a team, a state (member, manager, invited, applied, declined, rejected), and a message, which is a private field for associating a message about that particular user-member.


Views
------

In addition to being able to view a list of Teams in the dashboard (for users with appropriate permissions), staff and team managers can view team member lists that give them the ability to promote or demote members as well as access stats on each member's reviewing activities (by clicking on member email).



Usage Notes
--------------------------

The teams functionality is dependent on enabling a set of custom permissions that permit access to certain proposal types for normal (non-staff) users. Here's how to set up the correct database and permissions structures to enable teams feature:

1. Use a postgres db; SQLite3 db will throw errors on command-run;

2. You must create the conference sections/proposal sections for each permission type first: common options are Talks, Tutorials, Posters, etc.

3. Once you have set these up in the admin, return to your terminal and change directories into symposion/reviews/management/commands and run ``$ python ../../../../manage.py create_review_permissions``. You should see a set of permissions printed for "manage" and "review" of each proposal section type printed to stdout.

4. Return to your Symposion instance, and either create a team in your dashboard or navigate to the admin and use the Teams link. If the former, go to the Teams admin now (otherwise stay put). In the Teams admin, from the list of "Permissions" choose "reviews|reviews|Can review <proposaltype>" for each type that you would like members of that team to review; similarly, from the "Manager permissions" section choose "reviews|reviews|Can manage <proposaltype>" for each type you would like managers to manage for that team.

5. VERY IMPORTANT: Return to your terminal and change into top-level directory (containing manage.py). Run ``$ python manage.py syncdb``. You will be told "The following content type is stale and needs to be deleted: reviews|"---DO NOT DELETE! (In other words, type "No" when prompted). This "reviews" type is the custom contenttype that we are using to feed proposals to teams for review.