## Access to Akamai

This is a guide on how to get Akamai portal access with how programmatic credentials work with Akamai API.

### Akamai Portal Access

1. Ask for access to https://control.akamai.com/.

## Credentials for Programmatic Access to Akamai

There are multiple ways to programmatically authenticate to Akamai; both ways requires a set of credentials.

1. With [portal access](https://control.akamai.com), navigate to the top right of the Akamai Control Panel portal, and click on your username and go to `User Settings`.

1. Under [User and API client](https://control.akamai.com/apps/identity-management), you should see your own client access account and if you had requested an API account, you should also see an API client based account.

1. Navigate to your API client based account and [click on "Create Credentials" to create a set of credentials](https://techdocs.akamai.com/developer/docs/set-up-authentication-credentials) for accessing Akamai programmatic interface.

### Using environment variables.

1. The preferred way to authenticate is using [environment variables](https://registry.terraform.io/providers/akamai/akamai/latest/docs/guides/akamai_provider_auth#example-usage-2).

The following environment variables need to be set prior to running, and takes precedence over the .edgerc file.

```bash
AKAMAI_PAPI_HOST=akaa-XXXXXXXXXXXXXXXX-XXXXXXXXXXXXXXXX.luna.akamaiapis.net \
AKAMAI_PAPI_ACCESS_TOKEN=akaa-xxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxx \
AKAMAI_PAPI_CLIENT_TOKEN=akaa-xxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxx \
AKAMAI_PAPI_CLIENT_SECRET=aaaaaaaaaaaaaaaaaaaa12345xyz= \
```

### Using an .edgerc file

1. The simpliest way to authenticate is using a `.edgerc` file, stored in a home directory `~/.edgerc`. In this setup, the file looks a little like this:

```bash
[default]
client_secret =
host =
access_token =
client_token =
```

## Testing the credentials

Follow the [tool installation instructions](./tool-installation.md) to test credentials.
