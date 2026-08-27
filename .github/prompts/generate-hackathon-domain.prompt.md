---
name: "Generate Hackathon Domain"
description: "Generate and validate a complete industry package for this Fabric Data Agent hackathon from a domain brief. Use when adapting the repo to Network Rail or another industry."
argument-hint: "Provide the domain ID, for example network-rail"
agent: "agent"
---

Use [the Fabric Data Agent Hackathon skill](../../skills/fabric-data-agent-hackathon/SKILL.md).

The user will provide a domain ID. Read `config/domain-briefs/<domain-id>.json`, then run:

```powershell
python deployment/create_domain_package.py --domain <domain-id>
```

Treat the command output as the generation contract. Generate every required local artifact, add focused tests, and run the specified validation. Do not deploy to Fabric. Do not overwrite another domain package. Surface any domain-expert assumptions about grains, keys, KPIs, relationships, privacy, security, or safety before claiming completion.

For Network Rail, the domain ID is `network-rail`.