## Tools

Scripting to Akamai requires a [command line tool](https://github.com/akamai/cli) and understanding of the [Akamai API](https://techdocs.akamai.com/developer/docs/about-clis).  
Follow the instructions from [Akamai CLI](https://github.com/akamai/cli#install-akamai-cli) to install either using Docker or directly from a binary.

### Installation via Binary

- Download the [Akamai CLI](https://github.com/akamai/cli/releases).
- Move it to a usable location as an executable.

```bash
chmod +x ~/Downloads/akamai-<VERSION>-<PLATFORM>
mv ~/Downloads/akamai-<VERSION>-<PLATFORM> /usr/local/bin/akamai
```

- Install the plugins for [property-manager](https://github.com/akamai/cli-property-manager) to view properties and [akamai terraform](https://github.com/akamai/cli-terraform) to export configurations.

```bash
akamai install property-manager
akamai install terraform
```

Once installed, you should be able to run `akamai property-manager list-groups` with the list of groups returning.

### Updating tools

- Run `akamai update` to update [Akamai CLI](https://github.com/akamai/cli/releases) and associated Akamai CLI tools like `akamai terraform` and `akamai property-manager`.

### Other Sample Commands

These are a set of other sample commands to test with, on understanding the [Akamai CLI](https://github.com/akamai/cli#install-akamai-cli).

- Use `-f json` with the commands to print JSON instead of the table format.

> Requesting a list of hostnames:

- list-groups
- list-properties with group ID and contract ID
- list-property-hostnames
- list the property manager groups

```bash
akamai property-manager list-groups
```

- List specific products

```bash
akamai property-manager list-products -c <contract ID>
```

- List the property under a group / contract ID

```bash
akamai property-manager list-properties -g <group ID> -c <contract ID>
```

- List a product

```bash
akamai property-manager list-products -c <contract ID>
```

- List all property hostnames under a particular property

```bash
akamai property-manager list-property-hostnames -p <property ID>
```
