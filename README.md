<p align="center"><img src="https://github.com/programmerer1/sentient-riskscan-agent/blob/main/logo.png" width="200" alt="logo"></p>
**RiskScan** is an intelligent agent built on the [Sentient Agent Framework](https://github.com/sentient-agi/Sentient-Agent-Framework) for rapid blockchain risk assessment.

It takes a wallet address and immediately scans its history to identify links with suspicious, fraudulent, or criminal transactions (AML/CTF). It instantly provides a risk level and a report to safeguard your financial operations.

## Installation
Clone the repository
```
git clone https://github.com/programmerer1/sentient-riskscan-agent.git

cd sentient-riskscan-agent

cp .env.example .env
cp .mysql_env.example .mysql_env
# Fill in the env settings

docker compose -f docker-compose.yml up -d
```

** Example POST request to http://localhost:8000/assist: **
```bash
{
    "session": 
    {
        "processor_id":"sentient-chat-client",
        "activity_id":"01K6BEMNWZFMP3RMGJTFZBND2N",
        "request_id": "01K6BEPKY12FMR1S19Y3SE01C6",
        "interactions":[]
    }, 
    "query": 
    {
        "id": "01K6BEMZ2QZQ58ADNDCKBPKD51", 
        "prompt": "What can you say about the bc1qm34lsc65zpw79lxes69zkqmk6ee3ewf0j77s3h wallet on the bitcoin network?",
        "context": ""
    }
}
```


