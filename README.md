![](https://github.com/cr-ste-justine/clin-overture-client/workflows/Lint/badge.svg)
![](https://github.com/cr-ste-justine/clin-overture-client/workflows/Build/badge.svg)
![](https://github.com/cr-ste-justine/clin-overture-client/workflows/Publish/badge.svg)



# About

This is the overture command line client.

Its main functionality is uploading files on the overture stack.

# Known Limitations

The client runs from a container and launches another image it depends on when uploading (the Score client) to function so using in an environment where Docker runs in a separate VM from the host (MacOS, Windows) is currently not supported.

# Usage

See the **run_shell.sh** script to launch a shell inside the client container with an example batch upload setup.

Once inside the shell, look at the following commands for help (which are the two commands you need to run to perform the batch upload):

```
overturecli keycloak-login --help
overturecli batch-upload --help
```

# State Storage

The client creates a **store.db** file in the directory where it executes. It put the auth token it uses after a successful **keycloak-login** execution in this file along with the currently progress during an upload in case it gets interrupted (so that it doesn't start from scratch on the subsequent execution).

If you wish to clear the state, clear this file or alternatively, work from a different directory.