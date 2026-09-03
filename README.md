# Fabric Data Agent Hackathon Demo

## What This Repository Is

This repository provides a complete, reusable Microsoft Fabric Data Agent hackathon package.

It demonstrates how answer quality improves across a six-phase maturity journey:
1. Data readiness
2. Semantic model readiness
3. Agent configuration
4. Lakehouse source tuning
5. Routing with multiple data sources
6. Optional Implement ontology

USER_GUIDE.md implements this journey as six numbered workshop steps for one continuously-extended Data Agent.

Default example domain is UK legal Customer 360, and the package can be adapted to other industries.

## Who This Is For

- Hackathon organizers who need a repeatable Fabric Data Agent POC
- Solution architects demonstrating semantic model and routing impact
- Teams learning how to productionize agent quality step by step

## Repository Highlights

- Multi-table data assets across artifact-typed folders keyed by domain
- Semantic model and ontology configuration templates
- Routing configuration and derived-routing data generator
- Evaluation harness and sample prompt dataset
- End-user and deployment documentation
- Copilot workflow for future industry reuse

## Start Here

Choose one path:

| Role | Start with | Purpose |
| --- | --- | --- |
| Participant | [USER_GUIDE.md](USER_GUIDE.md) | Follow the six workshop steps and test one continuously improved Data Agent |
| Facilitator | [FACILITATOR_GUIDE.md](FACILITATOR_GUIDE.md) and [REUSE_FOR_NEW_INDUSTRY.md](REUSE_FOR_NEW_INDUSTRY.md) | Prepare the event, use solution checkpoints, and generate sample data, test questions, and answers for a different industry |
| Automation or troubleshooting | [deployment/README.md](deployment/README.md) | Understand deployment parameters, generated artifacts, and rerun behavior |

## Multi-Table Architecture

`LegalFirmSemanticModel` serves standard business metrics and the `LegalFirmDemo` Lakehouse serves prepared routing marts. Participants tune one continuously extended Data Agent to select between these complementary sources.

The three routing folders are intentionally separate: generated routing data, deployable agent configuration, and routing evaluation questions each have a distinct lifecycle. The semantic model plus the three derived Lakehouse marts form the final Step 5 configuration.


