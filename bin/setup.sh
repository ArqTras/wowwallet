echo -e "[+] Creating directories"
mkdir -p data/secrets data/wallets

if [[ ! -f "data/secrets/pass" ]];
then
  echo -e "[+] Creating new wallet secret"
  openssl rand -base64 32 > data/secrets/pass
fi

# echo -e "[+] Running wallet CLI"
# docker run --rm -it --name monero-wallet \
#     -v ~/git/lzahq/wownero-web-wallet/data:/data \
#     -p 8080:8080 \
#     --entrypoint "monero-wallet-cli" wownero-web-wallet \
#     --daemon-address crypto.int.lzahq.tech:38081 \
#     --stagenet \
#     --generate-new-wallet /data/wallets/lza-stage \
#     --use-english-language-names \
#     --password-file /data/secrets/pass \
#     --mnemonic-language english \
#     --restore-height 461618

# echo -e "[+] Running wallet RPC"
# docker run --rm -it --name monero-wallet \
#     -v ~/git/lzahq/wownero-web-wallet/data:/data \
#     -p 8080:8080 \
#     --entrypoint "monero-wallet-rpc" wownero-web-wallet \
#     --daemon-address crypto.int.lzahq.tech:38081 \
#     --stagenet \
#     --non-interactive \
#     --generate-from-json /data/wallet.json \
#     --disable-rpc-login \
#     --rpc-bind-port 8080

# docker run --rm -it --name monero-wallet \
#     -v ~/git/lzahq/wownero-web-wallet/data:/data \
#     -p 8080:8080 \
#     --entrypoint "monero-wallet-rpc" wownero-web-wallet \
#     --daemon-address crypto.int.lzahq.tech:38081 \
#     --stagenet \
#     --non-interactive \
#     --wallet-file /data/wallets/lza-stage \
#     --password-file /data/secrets/pass \
#     --rpc-bind-port 8080
