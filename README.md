# Python_RAT
Proof of Concept of a malicious Remote Administration Tool (RAT) write in Python.
Work in progress

## Discaimer

/!\ This tool is only provided for a scientific, ethical, and educational purposes.
DO NOT USE on a system that you do not own, or without the explicit permission of his owner.
First, because it's illegal, and second because of the unstable nature of this code.
It was only tested in a restricted environment, and the result may be unpredictable in a real life scenario.
I decline all responsibilities in case of misuse. /!\


## Features
- Installation script for the C2 server and the backend database coming soon.
- Multi thread architecture (It can handle a lot of clients at the same time, but their is no optimisation yet, so it just depends on your server's hardware).
- SQl database containing each client and identification information such as the OS, computer hostname, users, date of the last keep-alive, etc ... (it will make the integration of a futur web interface easier, and the architecture more resilient in case of migration).
- Custom AES encryption key for each client. The first network exchanges with the clients is done with a predefine encryption key, then a new and unique key is negociated with the client for the further transmissions.
- Strong mutex system that relies on a combination of various uuid and algorithms made from scratch.
- Custom keep-alive system. By default, you can predict the state of a client +- 2min.
- Asynchronous remote command executions on Windows systems.
- Clients can be killed from the C2 server.
- Deeper information can be gathered about clients.
- The client binary try to gain administrator privileged by popping UAC prompt on demand (It can be during the installation process, or later).
- Client persistence gained through startup execution and Windows register modification (only with admin priv).
- Custom clients builder (Static encryption key can be set and variable name can be randomly changed in order to generate a new signature of the clients binary).
- Anti-C2 hijacking technique that prevents the RAT client to be taken-over by a malicious adversary.
- Upload / download orders can be sent to the client. It means that the clients binary can be updated on the fly.
- Spreading capability inside a local area network. ( * )

## Forthcoming
- Unix client integration.
- Static AV evasion (Sandbox/VM/debugger detection & evasion).
- Dynamic AV evasion (Probably process doppelgänging technique + a custom packer for it, ( * ) but i don't know if i am really going to release it. It exposes me to a lot of trouble, and i'm already in a grey area concerning this project =D).
- More information gathering from the clients.
- More post-exploitations modules (Keylogger, screen / sound / webcam detector ( * )).
- Cabability of turning off the AV ( * ).
- Alternative communication channel (DNS tunneling and Sneaky Creeper integration).

## WARNING
I don't want to be boring, but again, using it in the wild is a mistake. On a technical level, it's not that hard to reverse the encryption key generation on the client side. The server's input from the clients are not yet sanatizes, and i'm sure that with a bit of fuzzing, it's possible to crash the server from the client, or worst, perform SQL injections and directly query the C2 database from a client. I have learned a lot of things since the beginning of this project, so it's probably poorly written and not that secure, by the server and the client point of view. Since the source code of the RAT is fully public, using it is not viable, and plenty of kill switch can be found. Also, the binary are hardcoded with the C2 address, and i'm not going to change this =D. I hope that i manage to prevent you from using it for bad purpose.
