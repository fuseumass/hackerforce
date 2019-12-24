# Environment Variables

## Production

`PRODUCTION` set to `true` for sane defaults when running in production.

`DEBUG` enables [Django debug mode](https://docs.djangoproject.com/en/2.0/ref/settings/#std:setting-DEBUG) .
Set when `PRODUCTION` is not set.

`SECRET_KEY` a random value for cryptographic signing by [Django](https://docs.djangoproject.com/en/2.0/ref/settings/#std:setting-SECRET_KEY) .

`REGISTRATION_TOKEN` a random string used to prevent registration by random people.
If set, users cannot access the registration page without knowing the token.
It must be set as the GET parameter `token` when opening the registration page.

E.g. if the token for `hackerforce.example.com` is `mytoken`, then new users
would register at `hackerforce.example.com/register/?token=mytoken` .

If not set, anyone can register from the home page.

## Emails

`FROM_EMAIL` the address emails HackerForce sends appear to come from.

`REPLY_TO_EMAIL` the address responses to your emails are sent to.

`BCC_EMAIL` An address all emails you send are sent to.

### Sending Emails

`SENDGRID_API_KEY` set if you want to send emails through [SendGrid](https://sendgrid.com/) .

`AWS_ACCESS_KEY_ID` set if you want to send emails through [AWS Simple Email Service](https://aws.amazon.com/ses/) .

## Database

`DATABASE_URL` the location of the database used by HackerForce.
Consumed by [dj_database_url](https://github.com/jacobian/dj-database-url) .

## Sponsorship Packet

`SPONSORSHIP_PACKET_URL`
The URL for the sponsorship packet, to download if `SPONSORSHIP_PACKET_FILE`
does not exist in the filesystem.

`SPONSORSHIP_PACKET_FILE`
The local name of the sponsorship packet, to be stored in the website/static
folder. If this file exists, it will be used. Otherwise, it will be
re-downloaded from `SPONSORSHIP_PACKET_URL`.
Must be set regardless of whether `SPONSORSHIP_PACKET_URL` is set.
