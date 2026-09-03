# Evaluation Guide

The SDK notebook is the main and only required participant evaluation notebook:

| Notebook | Responsibility |
| --- | --- |
| `NB_Run_SDK_Evaluation.ipynb` | Required: run staged prompts, preserve official SDK evidence, normalize run-step evidence, and compare snapshots |

There is no simulation mode or separate CLI evaluator. The checked-in challenge JSON is the source of truth for questions and expected answers.

## 1. Import And Configure

1. Import both `NB_Deploy_Data_Agent_Hackathon.ipynb` and `NB_Run_SDK_Evaluation.ipynb` into the Fabric workspace.
2. Attach `LegalFirmDemo` and make it the notebook's default Lakehouse.
3. Set `AGENT_NAME` and `WORKSPACE_NAME`.
4. Set `DATA_AGENT_STAGE` to `sandbox` or `draft` for an unpublished agent, or `production` for a published agent.
5. Change only `SNAPSHOT_NAME` for each run; the notebook selects the dataset and paraphrase setting.

The SDK creates the configured evaluation table and companion steps table. Do not create them manually.

## 2. Run Every Snapshot

| Stage | Dataset | `SNAPSHOT_NAME` |
| --- | --- | --- |
| Initial agent | `challenge` | `step1_baseline` |
| Prep for AI configured | `challenge` | `step2_prep_ai` |
| Lakehouse attached | `challenge` | `step3_lakehouse_added` |
| Lakehouse tuned | `challenge` | `step4_lakehouse_tuned` |
| Final standard evaluation | `challenge` | `step5_final` |
| Routing marts | `routing` | `step5_routing` |

Run all cells at each stage and retain the JSON and evidence CSV. Every challenge snapshot uses the same eight questions plus eight paraphrases. The routing JSON remains separate. Step 6 ontology is an optional qualitative exercise until a dedicated ontology question dataset exists.

## 3. Review The Evidence

The standard details include question, expected answer, actual answer, SDK judgement, and thread information. Generated SQL or DAX is associated with companion run-step data and is not guaranteed in `get_evaluation_details()`. The notebook preserves both raw frames, normalizes run-step evidence when available, and warns when query or selected-source evidence is missing.

Use the comparison section for the question-by-step result matrix. Review generated query and selected-source evidence directly in the SDK notebook exports and thread links.

Question `HC007` is time-relative. Its expected answer of 35 assumes the checked-in workshop data is evaluated after 2024-02-29. Treat unpaid invoices as the per-customer sum of Invoice transactions whose `payment_status` is exactly `Unpaid`, then exclude customers with an interaction in the 60 days before the evaluation date.

Question `HC008` is intentionally unsupported. Award answer and consistency points only when the agent explicitly says client satisfaction data is unavailable and does not invent a score or use interactions as a proxy. Record the selected source as `none`; copied run-step evidence showing that no source query was executed satisfies the evidence requirement.

## Evidence Rules

- A correct answer alone does not prove correct routing or query logic.
- Do not award the logic point without copied SQL, DAX, or run-step evidence.
- Keep baseline and final settings comparable.
- Treat the official SDK result as captured evidence; do not infer generated SQL/DAX or selected source when companion evidence is absent.

## Troubleshooting

### No default Lakehouse

Attach `LegalFirmDemo` in the notebook Explorer and set it as the default Lakehouse before running the SDK evaluation.

### SDK import error

Run the dependency installation cell and allow the Fabric Python session to restart. Then continue from the configuration cell.

### Missing SDK detail rows

Check the Data Agent name, workspace, stage, output table, and default Lakehouse. Rerun the same snapshot after correcting the configuration.

### Missing generated query or selected source

Use the thread link to inspect the run directly. Missing run-step fields are an SDK evidence limitation, not proof that no query ran.

For expected answers, hints, and debrief guidance, see [FACILITATOR_GUIDE.md](../FACILITATOR_GUIDE.md).