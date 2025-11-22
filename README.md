# Secret Santa Emailer
This program allows for any number of people to be auto matched with other people in a group to be directed to who they should buy presents for. The number of presents that each person buys and gets can be varied all the way up to but not including the number of people in the group.\
\
The program either takes in a .txt file for the structure of the email and a .csv file with all the people, their emails, and optionally their addresses or the program takes in the same information over the console.
Then, the program matches up people with others to gift in a round based format, such that no one is gifting to themselves, or buying more than one gift for a single person.
Finally, the program reads an .env file for the email and password of the email service it will be using to send out emails to all participants, and then emails each person in the group with their results and who they will be gifting for, in the structure of the message passed to the program.

Any failed email attempts are brought to the attention of the user of the program. There is also an option to save the results in a .txt file, such that the user does not have to see who got him in secrete santa, but still allows them to double check who is gifting who when confusion occurs.\
\
Some limitations that were added to ensure logical operation include checks that all emails are unique, all names or nicknames are unique (so that the end user knows who the email is talking about), and that the message passed into the program has one slot at least for the name of the person the reciever of the email needs to buy a gift for (so that the secret santa process is functional).

To run the program, simply install the requirements.txt, setup an .env file with your EMAIL_ADDRESS and PASSWORD parameters, optionally create a .csv file with your group members and a .txt file with the message that will be in the email, and run the program.
