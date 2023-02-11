## Importing Akamai Configurations

These are simple and effective commands to use the [Akamai CLI](https://github.com/akamai/cli/releases) to extract configurations and properties.

```bash
akamai property-manager list-groups -f json
akamai property-manager list-properties -g <groupId> -c <contractId> -f json
akamai terraform export-domain <domain>
akamai terraform export-appsec <domain>
akamai terraform export-property <domain>
akamai terraform export-cloudlets-policy <domain>
akamai terraform export-cloudlets-policy <domain>
akamai terraform export-edgekv <domain>
akamai terraform export-iam <domain>
akamai terraform export-iam all <domain>
akamai terraform export-imaging <domain>
akamai terraform export-zone <domain>
```
