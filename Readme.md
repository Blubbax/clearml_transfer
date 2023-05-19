# ClearML Transfer

This project is a transfer script for ClearML tasks.
It facilitates the operation of multiple ClearML instances.
This might be necessary in case of university industry collborations
where a single ClearML instance might not be possible.

This script has been implemented in context of my master's thesis
to enable the artifact transfer from the LNU to Aimo fit.

## How it works

Two ClearML configuration files are required - one for each instance.
The configurations files are identically with the ClearML configuration files on client computers.
Therefore, they just need to be copied.


Run the api.py script and hand over the pathes to the configuration files within the environment variables.
