## How It Works
1. Generate Authorization URL — The user visits the link and logs in.
2. Redirect with Code — The provider redirects to your REDIRECT_URI with an authorization code.
3. Exchange Code for Token — The script exchanges the code for an access token.
4. Access Protected Resources — Use the token to call APIs.

## Security Notes
- Never hardcode CLIENT_SECRET in public code; use environment variables.
- Use HTTPS for all OAuth endpoints.
- Store and refresh tokens securely.
