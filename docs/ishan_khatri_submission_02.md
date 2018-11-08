# Ishan Khatri

## User Model
I created a custom user model that extends the Abstract User base class in Python which allows for additional fields to be stored in the User's model without creating an additional table and running a Join to look up user data that isn't included in the default Django User Model.

Currently the custom user model only supports the additional field of `phone_number` but in the future additional fields may be added.

## User Authentication
In addition I created all of the linkages between the custom User model and the default Django authentication system in order to allow for users to register, log-in, and logout. The appropiate views & buttons were also created for this with sexy styling provided by the tabler library.

## Database Diagram
