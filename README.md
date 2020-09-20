# wowstash

A web wallet for noobs who can't use a CLI.

## Notes


```
wownero-wallet-cli --generate-from-json e.json --restore-height 247969 --daemon-address node.suchwow.xyz:34568 --command version

wownero-wallet-rpc --non-interactive --rpc-bind-port 8888 --daemon-address node.suchwow.xyz:34568 --wallet-file wer --rpc-login user1:mypass1 --password pass
```

```
{
  "version": 1,
  "filename": "<user specific name>",
  "scan_from_height": <height>,
  "password": "<password>",
  "seed": "<seed phrase>"
}
```
