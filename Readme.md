Python League Manager Webscraper
===============

This python script was used to collate (selected) managerial appointment and termination dates for English clubs as recorded in the League Manager's Association (LMA) website: www.leaguemanagers.com. 

This script is now updated and should work with the current incarnation of the LMA website (though there are still some broken links, which the script will take a note of and then skip).

The data collected is provided in mantable.csv.

It contains:

- Over 4000 entries, each listing manager, club, role, appointment and termination dates
- Over 1500 unique managers (those managers listed on the LMA website as having managed a current league side at some point)
- Most errors that occur in the original website! For example, the appointment/end dates are incorrect for Bill Ayre (Halifax Town). And as noted above, some manager page links are broken. Furthermore, the list of positions for each manager does not appear to be exhaustive, for example John Toshack lists only appointments at Swansea City and Wales, despite a long managerial career with non-British clubs.

