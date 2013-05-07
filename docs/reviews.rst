Reviews App
=============

The ``reviews`` app provides users with appropriate permissions (as defined either by addition to a Team or by assignment via Groups membership) the ability to vote on and/or substantively review proposals from other users. 

Reviewers and staff are able to access all reviews, reviews they've submitted, and proposals they have not reviewed by section from within the Reviews pane in the dashboard. Ability to toggle between these options persists on the results page.

Results pages show lists of reviews by section and status (as above), along with current vote tallies for each proposal. Clicking on proposals in this view produces a single-review page, containing review title, author, and summary as well as tabs showing review stats and comments.

These pages also contain a sidebar with links to pages that show cumulative votes per section; review assignments, if any; and result notifications for accepted, rejected, and standby proposals.

For more information on designating and managing reviewers, see the teams.rst doc.


Models
------


ProposalScoreExpression
~~~~~~~~~~~~~~~~~~~~~~~~~

Returns score expressions as strings


Votes
~~~~~~~

Defines voting rubric with scoring values


ReviewAssignment
~~~~~~~~~~~~~~~~~~~

Review assignments define assignment types (auto assigned initial/later and opt-in) and assign proposals to users who are members defined in the "reviewers" Group. This model may not be used if Teams are being utilized to handle reviewers and reviews.


ProposalMessage
~~~~~~~~~~~~~~~~~~

Used for modeling the additional speakers on a proposal in additional to the
submitting speaker. The status of an additional speaker may be ``Pending``,
``Accepted`` or ``Declined``.

To read more about addition speakers, see the speakers.rst doc


Review
~~~~~~~~

Models a review with all of its associated data: proposal, vote(s), comments, metadata.
Also defines a set of methods for managing reviews: saving, deleting, adding CSS classes, and adding parent section as a property.


LatestVote
~~~~~~~~~~~~

Stores user reviews according to date submitted


ProposalResult
~~~~~~~~~~~~~~~~

Stores the results of all voting for each proposal object reviewed.
Includes methods for calculating results and for updating votes.


Comment
~~~~~~~~~

Models comments submitted to proposal review threads, including whether comment is public or private.


NotificationTemplate
~~~~~~~~~~~~~~~~~~~~~~

Defines a template for result notifications.


ResultNotification
~~~~~~~~~~~~~~~~~~~~

Associates result with proposal object and adds email args
Includes methods for defining "accepted" status and for promotion of proposals



Template Tags
---------------

The ``review_assignments`` tag allows for iteration over user's assignments. 

