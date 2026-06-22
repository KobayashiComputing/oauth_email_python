# OAuth Authentication with Flask
This example is based on the blog article [OAuth Authentication with Flask - Connect to Google, Twitter, and Facebook](https://www.geeksforgeeks.org/python/oauth-authentication-with-flask-connect-to-google-twitter-and-facebook/)

## Install Dependencies
```
pip install -U Flask Authlib requests
```

## Create and Retrieve the Credentials from the Provider

### Google
I'm going to try using Google first to send email via a Gmail account. If I can get that working, I'll try to do the same with my Outlook.com email account.

I'm going to start with this [Google OAuth Documentation](https://developers.google.com/identity/protocols/oauth2) and see if I can figure out how to create and copy the credentials I need.

The link that the "OAuth with Flask" article includes leads me [here](https://console.cloud.google.com/apis/credentials,?pli=1&rapt=AEjHL4OwWUVe4hLVkJwUqnYo3ROKGkPBZSj9wVtsVa1RhrL9lkjCq6kBE0NZzTp-3elVjPgpr7vkrmZ438tEsb60GfyKjoMUZsZTtyoP8MZtTgDRHkPFJ7M&authuser=3) after taking me to a login page where I log in with my Gmail account.

I'm wondering if going to https://console.cloud.google.com would yield the same result... It sort of does (I think). After presenting a login screen, it takes me to the "Welcome" page and defaults to the last project I created (which, conveniently, was the project for this example - which is 'Flask OAuth2 Example'). Clcking on the link to go to my "Dashboard" does take me to the dashboard, but that has a notice that I really should use the "Cloud Hub," so from now on I'll go there instead (there was also a link on the original page for that).

#### https://console.cloud.google.com
This is the "Cloud Home Welcome Page," with default (only or most recent I'm guessing) project selected.

Projext Name    : Flask OAuth2 Example
Project Number  : 890127835115
Project ID      : flask-oauth2-example-499919

-> Click(ed) on 'Cloud Hub' link...

I chose "Enable APIs" and enabled all of them.

#### Create and Download Google OAuth 2.0 Credentials
- Go to https://console.cloud.google.com/apis to create credentials.
- Choose 'Library'
- Use search box to search for 'Gmail API'
- Click on the Gmail API box ("Google Enterprise API)
- Click "Enable" if not yet enabled, otherwise the button is "Manage"
- Click "Create Credentials"
- In 'Select an API' select 'Gmail API'
- Choose 'User Data'
- Click 'Next'
- Fill in the form
  - App name: Enter an app name of your choice (e.g., Pattie’s App).
  - User support email: Select your email address from the choices provided.
  - App logo: If you’d like, you can upload a logo for your app. This is optional.
  - Developer Contact Info (your email address)
- Click 'Save and Continue'
- Skip over 'Scopes' and click 'Save and Continue'
- In 'OAuth Client ID' fill in the form
  - Application Type: Web Application
  - Name: only used in the console for identification 
- Skip 'Authorized Javascript Origins'
- For 'Authorized Redirect URIs' use: http://localhost:5000/google/auth/
- Click 'Create'
- Download your credentials in JSON format and save them in a secure place...


#### Microsoft Bing Copilot (AI) Generated Info
```
Google API Scope for Sending Email from a Web App
To send email from a web app using the Gmail API, you need to request the https://www.googleapis.com/auth/gmail.send scope in your OAuth 2.0 authorization flow.

Why gmail.send?
gmail.send grants your app the ability to send email on behalf of the user’s Gmail account.

It is a sensitive scope, so Google requires you to complete the Restricted Scope Verification process before you can use it in production unified.to+1.

This scope is the minimal permission needed if your app’s only purpose is to send emails.

Other scopes to consider
If your app also needs to:

Read or modify messages/labels:

https://www.googleapis.com/auth/gmail.labels (non-sensitive)

https://www.googleapis.com/auth/gmail.modify (restricted)

View messages in context (e.g., for add-ons):

https://www.googleapis.com/auth/gmail.addons.current.message.action (non-sensitive)

But for pure email sending, gmail.send is the only required scope.

Implementation steps
Enable Gmail API in the Google Cloud Console.

Configure OAuth 2.0 with the gmail.send scope.

Complete Restricted Scope Verification if you plan to use it in production unified.to.

Use the OAuth token to call the Gmail API’s users.messages.send endpoint to send emails.

Example scope list for email sending:

[
  'https://www.googleapis.com/auth/gmail.send'
]
Tip: Always request the minimum scopes your app needs to reduce user trust barriers and comply with Google’s security requirements 
```
#### Helpful Docs:
[WP Mail SMTP Auth Docs](https://wpmailsmtp.com/docs/how-to-set-up-the-gmail-mailer-in-wp-mail-smtp/)

##### There is a 'Playground'
Google [OAuth 2.0 Playground](https://developers.google.com/oauthplayground/)

#### Be sure to add http://localhost:5000/google/auth/ into Authorized redirect URIs