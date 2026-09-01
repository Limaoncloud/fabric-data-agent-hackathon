"""
Fabric Data Agent Evaluation Framework

This script supports exactly two evaluation modes. Pick one:
- --simulation: a seeded, illustrative dry-run of the framework. It does NOT call a real
  agent and must never be reported as measured accuracy.
- --sdk-mode: the real, Microsoft-recommended evaluation path using fabric-data-agent-sdk
  against an actual deployed Data Agent.

Usage examples:
    python evaluation/evaluate_agent.py --simulation --dataset evaluation/challenge/uk-legal.json --output results_simulation.json
    python evaluation/evaluate_agent.py --sdk-mode --agent-id <agent_name> --table-name demo_eval --dataset evaluation/challenge/uk-legal.json --output results.json

Requirements:
    pip install pandas
    pip install fabric-data-agent-sdk   # for --sdk-mode
"""

import argparse
import importlib
import json
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import pandas as pd
except ImportError:
    pd = None

try:
    _fabric_eval_module = importlib.import_module("fabric.dataagent.evaluation")
    evaluate_data_agent = _fabric_eval_module.evaluate_data_agent
    get_evaluation_details = _fabric_eval_module.get_evaluation_details
    get_evaluation_summary = _fabric_eval_module.get_evaluation_summary
    FABRIC_EVAL_SDK_AVAILABLE = True
    FABRIC_EVAL_SDK_IMPORT_ERROR = None
except ImportError as exc:
    evaluate_data_agent = None
    get_evaluation_details = None
    get_evaluation_summary = None
    FABRIC_EVAL_SDK_AVAILABLE = False
    FABRIC_EVAL_SDK_IMPORT_ERROR = exc


@dataclass
class QueryResult:
    """Result from a single query execution"""
    query_id: str
    question: str
    answer: Any
    source_used: Optional[str]
    response_time_ms: float
    dax_query: Optional[str]
    sql_query: Optional[str]
    error: Optional[str]
    run_steps: Optional[List[Dict]] = None


@dataclass
class EvaluationMetrics:
    """Evaluation metrics for a single query"""
    query_id: str
    exact_match: bool
    semantic_match: bool
    routing_correct: bool
    measure_selection_correct: bool
    response_time_acceptable: bool  # < 5 seconds
    verified_answer_used: bool
    error_occurred: bool
    notes: str


@dataclass
class AggregateMetrics:
    """Aggregate metrics across all queries"""
    total_queries: int
    exact_match_accuracy: float
    semantic_match_accuracy: float
    routing_accuracy: float
    measure_selection_accuracy: float
    avg_response_time_ms: float
    verified_answer_hit_rate: float
    error_rate: float
    by_category: Dict[str, Dict[str, float]]
    by_difficulty: Dict[str, Dict[str, float]]


class DataAgentEvaluator:
    """Evaluates Fabric Data Agent performance"""
    
    def __init__(
        self, 
        workspace_id: str = "<workspace_id>",
        agent_id: str = "<agent_id>",
        simulation_mode: bool = False,
        simulation_step: int = 4,
        sdk_mode: bool = False,
        workspace_name: Optional[str] = None,
        table_name: str = "evaluation_output",
        data_agent_stage: str = "production",
        critic_prompt: Optional[str] = None,
    ):
        """
        Initialize evaluator
        
        Args:
            workspace_id: Fabric workspace ID
            agent_id: Data agent ID to evaluate
            simulation_mode: If True, simulate responses instead of calling actual API
            simulation_step: Demo step to simulate (1-6)
        """
        self.workspace_id = workspace_id
        self.agent_id = agent_id
        self.simulation_mode = simulation_mode
        self.simulation_step = simulation_step
        self.sdk_mode = sdk_mode
        self.workspace_name = workspace_name
        self.table_name = table_name
        self.data_agent_stage = data_agent_stage
        self.critic_prompt = critic_prompt
        self.last_query_results: List[QueryResult] = []
        self.sdk_details_df = None

        if not self.sdk_mode and not simulation_mode:
            raise ValueError(
                "Choose exactly one mode: --simulation (illustrative dry-run) or "
                "--sdk-mode (real evaluation via fabric-data-agent-sdk)."
            )

        if self.sdk_mode:
            if not FABRIC_EVAL_SDK_AVAILABLE:
                raise RuntimeError(
                    "Could not import fabric.dataagent.evaluation. "
                    "Install or upgrade it with: pip install -U fabric-data-agent-sdk. "
                    f"Underlying import error: {FABRIC_EVAL_SDK_IMPORT_ERROR}"
                )
            if pd is None:
                raise RuntimeError("pandas is required for --sdk-mode. Install it with: pip install pandas")
            print(f"Running in SDK MODE (real evaluation) - Agent name: {agent_id}, Stage: {data_agent_stage}")
        else:
            print(
                f"Running in SIMULATION MODE - Step {simulation_step} - ILLUSTRATIVE ONLY.\n"
                "These are seeded, synthetic results for smoke-testing the framework, "
                "NOT real Data Agent answers. Use --sdk-mode for measured results."
            )
    
    def load_evaluation_dataset(self, dataset_path: str) -> Dict[str, Any]:
        """Load evaluation dataset from JSON file"""
        with open(dataset_path, 'r') as f:
            return json.load(f)
    
    def execute_query(self, question: str, ground_truth_answer=None, expected_source=None) -> QueryResult:
        """
        Simulate a single query response.

        Simulation mode is the only path that reaches this method; --sdk-mode calls the
        real Fabric Data Agent SDK instead (see evaluate_with_sdk).
        """
        # Simulate response
        time.sleep(0.05)  # Simulate processing time

        # Illustrative accuracy rates per USER_GUIDE.md step (1=semantic-model baseline,
        # 2=after Prep for AI, 3=Lakehouse attached baseline, 4=Lakehouse tuned,
        # 5=derived tables + routing, 6=bonus ontology).
        step_configs = {
            1: {"accuracy": 0.55, "routing": 0.60, "response_time": (1500, 4000), "error_rate": 0.15},  # Semantic-model baseline
            2: {"accuracy": 0.95, "routing": 0.95, "response_time": (800, 2000), "error_rate": 0.02},   # After Prep for AI
            3: {"accuracy": 0.80, "routing": 0.65, "response_time": (1200, 3000), "error_rate": 0.08},  # Lakehouse attached, untuned
            4: {"accuracy": 0.92, "routing": 0.90, "response_time": (900, 2200), "error_rate": 0.03},   # Lakehouse tuned
            5: {"accuracy": 0.96, "routing": 0.96, "response_time": (800, 1800), "error_rate": 0.01},   # Derived tables + routing
            6: {"accuracy": 0.97, "routing": 0.97, "response_time": (700, 1700), "error_rate": 0.01},   # Bonus ontology
        }

        config = step_configs.get(self.simulation_step, step_configs[2])
        import random

        # Simulate errors based on step
        if random.random() < config["error_rate"]:
            return QueryResult(
                query_id="",
                question=question,
                answer=None,
                source_used=None,
                response_time_ms=random.randint(*config["response_time"]),
                dax_query=None,
                sql_query=None,
                error="Query execution failed"
            )

        # Routing logic with configurable accuracy
        correct_source = expected_source if expected_source else "LegalFirmSemanticModel"
        if random.random() < config["routing"]:
            # Correct routing
            source = correct_source
        else:
            # Wrong routing
            source = "LegalFirmDemo" if correct_source == "LegalFirmSemanticModel" else "LegalFirmSemanticModel"

        # Answer accuracy based on step
        if ground_truth_answer is not None and random.random() < config["accuracy"]:
            answer = ground_truth_answer
        else:
            # Simulate wrong answer
            if isinstance(ground_truth_answer, (int, float)):
                answer = int(ground_truth_answer * random.uniform(0.5, 1.5))
            elif isinstance(ground_truth_answer, list):
                answer = ground_truth_answer[:len(ground_truth_answer)//2] if ground_truth_answer else []
            else:
                answer = ground_truth_answer  # For other types, use correct answer

        return QueryResult(
            query_id="",
            question=question,
            answer=answer,
            source_used=source,
            response_time_ms=random.randint(*config["response_time"]),
            dax_query=None,
            sql_query="SELECT simulated FROM query",
            error=None
        )
    
    def compare_answers(
        self, 
        actual: Any, 
        expected: Any, 
        answer_type: str
    ) -> Tuple[bool, bool]:
        """
        Compare actual answer to ground truth
        
        Returns:
            (exact_match, semantic_match)
        """
        # Exact match
        if answer_type == "number":
            # Allow small floating point tolerance
            actual_val = float(actual)
            expected_val = float(expected)
            exact = abs(actual_val - expected_val) < 0.01
            if expected_val == 0:
                semantic = exact
            else:
                semantic = abs(actual_val - expected_val) / abs(expected_val) < 0.05  # 5% tolerance
        elif answer_type == "text":
            exact = str(actual).strip().lower() == str(expected).strip().lower()
            semantic = exact
        elif answer_type == "list":
            actual_set = set(str(x).strip().lower() for x in actual)
            expected_set = set(str(x).strip().lower() for x in expected)
            exact = actual_set == expected_set
            # Semantic: at least 80% overlap
            if len(expected_set) > 0:
                overlap = len(actual_set & expected_set) / len(expected_set)
                semantic = overlap >= 0.8
            else:
                semantic = exact
        elif answer_type == "table":
            # For tables, compare as dictionaries
            exact = actual == expected
            # Semantic: all keys present and values within tolerance
            if isinstance(actual, dict) and isinstance(expected, dict):
                if set(actual.keys()) != set(expected.keys()):
                    semantic = False
                else:
                    matches = sum(
                        abs(float(actual.get(k, 0)) - float(expected.get(k, 0))) / float(expected.get(k, 1)) < 0.05
                        for k in expected.keys()
                    )
                    semantic = matches / len(expected) >= 0.8
            else:
                semantic = exact
        else:
            exact = str(actual) == str(expected)
            semantic = exact
        
        return exact, semantic
    
    def evaluate_query(
        self, 
        eval_query: Dict[str, Any], 
        result: QueryResult
    ) -> EvaluationMetrics:
        """Evaluate a single query result against ground truth"""
        
        # Check for errors
        error_occurred = result.error is not None
        
        if error_occurred:
            return EvaluationMetrics(
                query_id=eval_query["id"],
                exact_match=False,
                semantic_match=False,
                routing_correct=False,
                measure_selection_correct=False,
                response_time_acceptable=False,
                verified_answer_used=False,
                error_occurred=True,
                notes=f"Error: {result.error}"
            )
        
        # Compare answers
        exact_match, semantic_match = self.compare_answers(
            result.answer,
            eval_query["ground_truth_answer"],
            eval_query["answer_type"]
        )
        
        # Check routing
        routing_correct = True
        if eval_query.get("tests_routing", False) and result.source_used:
            routing_correct = result.source_used == eval_query["expected_source"]
        
        # Check response time
        response_time_acceptable = result.response_time_ms < 5000  # 5 seconds
        
        # Check if verified answer was used
        verified_answer_used = False
        if eval_query.get("verified_answer_id") and result.run_steps:
            # Check run steps for verified answer usage
            for step in result.run_steps:
                if step.get("type") == "VerifiedAnswer":
                    verified_answer_used = True
                    break
        
        # Check measure selection (for semantic model queries)
        measure_selection_correct = True
        if eval_query.get("tests_measure_selection", False) and result.dax_query:
            # Parse DAX to check if correct measure was used
            # This is simplified - in production, parse DAX more carefully
            measure_selection_correct = "Total Case Value" in result.dax_query or \
                                       "Average Case Value" in result.dax_query
        
        notes = []
        if not exact_match and semantic_match:
            notes.append("Semantic match but not exact")
        if not routing_correct:
            notes.append(f"Wrong source: {result.source_used} vs {eval_query['expected_source']}")
        if not response_time_acceptable:
            notes.append(f"Slow: {result.response_time_ms:.0f}ms")
        
        return EvaluationMetrics(
            query_id=eval_query["id"],
            exact_match=exact_match,
            semantic_match=semantic_match,
            routing_correct=routing_correct,
            measure_selection_correct=measure_selection_correct,
            response_time_acceptable=response_time_acceptable,
            verified_answer_used=verified_answer_used,
            error_occurred=False,
            notes="; ".join(notes) if notes else "OK"
        )
    
    def evaluate_all(self, dataset_path: str) -> Tuple[List[EvaluationMetrics], AggregateMetrics]:
        """Evaluate all queries in the dataset"""
        dataset = self.load_evaluation_dataset(dataset_path)
        queries = dataset["evaluation_queries"]
        
        print(f"\n{'='*80}")
        print(f"Starting evaluation of {len(queries)} queries")
        print(f"Agent: {self.agent_id}")
        print(f"Mode: {'SIMULATION (illustrative only)' if self.simulation_mode else 'SDK (real evaluation)'}")
        print(f"{'='*80}\n")
        
        results = []
        metrics_list = []
        
        for i, eval_query in enumerate(queries, 1):
            print(f"[{i}/{len(queries)}] {eval_query['id']}: {eval_query['question'][:60]}...")
            
            # Execute query
            result = self.execute_query(
                eval_query["question"],
                ground_truth_answer=eval_query.get("ground_truth_answer"),
                expected_source=eval_query.get("expected_source")
            )
            result.query_id = eval_query["id"]
            results.append(result)
            
            # Evaluate
            metrics = self.evaluate_query(eval_query, result)
            metrics_list.append(metrics)
            
            # Print result
            status = "PASS" if metrics.exact_match else "FAIL"
            print(f"  {status} Exact: {metrics.exact_match} | Semantic: {metrics.semantic_match} | "
                  f"Routing: {metrics.routing_correct} | Time: {result.response_time_ms:.0f}ms")
            if metrics.notes:
                print(f"     Notes: {metrics.notes}")
        
        self.last_query_results = results

        # Calculate aggregate metrics
        aggregate = self._calculate_aggregate_metrics(queries, metrics_list)
        
        return metrics_list, aggregate

    @staticmethod
    def _normalize_key(text: Any) -> str:
        return str(text).strip().lower()

    @staticmethod
    def _row_value(row: Dict[str, Any], aliases: List[str], default: Any = None) -> Any:
        lowered = {str(k).strip().lower(): v for k, v in row.items()}
        for alias in aliases:
            if alias.lower() in lowered:
                return lowered[alias.lower()]
        return default

    @staticmethod
    def _parse_official_summary(summary_df) -> Dict[str, Any]:
        if summary_df is None or len(summary_df) == 0:
            return {}

        row = summary_df.iloc[0].to_dict()
        lowered = {str(k).strip().lower(): v for k, v in row.items()}

        def pick(*aliases):
            for alias in aliases:
                if alias in lowered:
                    return lowered[alias]
            return None

        total = pick("total", "total_questions", "total_evaluated", "num_questions")
        true_count = pick("true", "true_count", "correct", "correct_count")
        false_count = pick("false", "false_count", "incorrect", "incorrect_count")
        unclear_count = pick("unclear", "unclear_count")
        accuracy = pick("accuracy", "accuracy_rate")

        return {
            "total": int(total) if total is not None else None,
            "true_count": int(true_count) if true_count is not None else None,
            "false_count": int(false_count) if false_count is not None else None,
            "unclear_count": int(unclear_count) if unclear_count is not None else None,
            "accuracy": float(accuracy) if accuracy is not None else None,
            "raw_columns": list(summary_df.columns),
        }

    def evaluate_with_sdk(self, dataset_path: str) -> Tuple[List[EvaluationMetrics], AggregateMetrics, Dict[str, Any]]:
        """Run official Fabric SDK evaluation and map results into custom metrics."""
        if pd is None:
            raise RuntimeError("pandas is required for SDK mode")

        dataset = self.load_evaluation_dataset(dataset_path)
        queries = dataset["evaluation_queries"]
        input_df = pd.DataFrame(
            {
                "question": [q["question"] for q in queries],
                "expected_answer": [q["ground_truth_answer"] for q in queries],
            }
        )

        print(f"\n{'='*80}")
        print(f"Starting SDK evaluation of {len(queries)} queries")
        print(f"Agent Name: {self.agent_id}")
        print(f"Stage: {self.data_agent_stage}")
        print(f"Output Table: {self.table_name}")
        print(f"{'='*80}\n")

        kwargs = {
            "workspace_name": self.workspace_name,
            "table_name": self.table_name,
            "data_agent_stage": self.data_agent_stage,
        }
        if self.critic_prompt:
            kwargs["critic_prompt"] = self.critic_prompt

        evaluation_id = evaluate_data_agent(input_df, self.agent_id, **kwargs)
        if evaluation_id is None:
            raise RuntimeError(
                "Fabric SDK evaluation did not start because the output table was not found. "
                "In the Fabric notebook, attach the Lakehouse that contains the evaluation "
                "table and set it as the default Lakehouse. Then set TABLE_NAME to the exact "
                "table name shown under that Lakehouse's Tables folder and rerun from the "
                "configuration cell."
            )

        summary_df = get_evaluation_summary(table_name=self.table_name, verbose=False)
        details_df = get_evaluation_details(
            evaluation_id=evaluation_id,
            table_name=self.table_name,
            get_all_rows=True,
            verbose=False,
        )
        if details_df is None:
            raise RuntimeError(
                f"Fabric SDK returned no detail rows from table {self.table_name!r}. "
                "Confirm that this exact table exists under the notebook's attached default "
                "Lakehouse, then rerun the evaluation."
            )
        self.sdk_details_df = details_df

        query_map = {(self._normalize_key(q["question"])): q for q in queries}
        metrics_list: List[EvaluationMetrics] = []
        mapped_results: List[QueryResult] = []
        mapped_query_ids = set()

        for _, row in details_df.iterrows():
            row_dict = row.to_dict()
            question = self._row_value(row_dict, ["question", "query"], "")
            eval_query = query_map.get(self._normalize_key(question))

            if not eval_query:
                continue

            mapped_query_ids.add(eval_query["id"])

            actual_answer = self._row_value(row_dict, ["actual_answer", "answer", "agent_answer"])
            source_used = self._row_value(
                row_dict,
                ["source_used", "selected_source", "data_source", "data_source_used"],
                None,
            )
            dax_query = self._row_value(row_dict, ["dax_query", "dax"], None)
            sql_query = self._row_value(row_dict, ["sql_query", "sql"], None)
            response_time_ms = self._row_value(
                row_dict,
                ["response_time_ms", "duration_ms", "latency_ms"],
                0,
            )
            evaluation_result = str(self._row_value(row_dict, ["evaluation_result"], "")).strip().lower()

            result = QueryResult(
                query_id=eval_query["id"],
                question=eval_query["question"],
                answer=actual_answer,
                source_used=source_used,
                response_time_ms=float(response_time_ms) if response_time_ms else 0.0,
                dax_query=dax_query,
                sql_query=sql_query,
                error=None,
                run_steps=None,
            )
            mapped_results.append(result)

            metric = self.evaluate_query(eval_query, result)

            # Align exact/semantic flags with official evaluator when available.
            if evaluation_result in {"true", "false", "unclear"}:
                metric.exact_match = evaluation_result == "true"
                metric.semantic_match = evaluation_result == "true"
                if evaluation_result == "unclear":
                    metric.notes = (metric.notes + "; " if metric.notes else "") + "Official evaluator returned unclear"

            # Conservative fallback if routing/measure details are not exposed by SDK row.
            if eval_query.get("tests_routing", False) and not source_used:
                metric.routing_correct = False
                metric.notes = (metric.notes + "; " if metric.notes else "") + "Routing source not exposed in SDK row"

            if eval_query.get("tests_measure_selection", False) and not dax_query:
                metric.measure_selection_correct = False
                metric.notes = (metric.notes + "; " if metric.notes else "") + "DAX not exposed in SDK row"

            metrics_list.append(metric)

        # If SDK details skipped any queries, emit explicit failures for traceability.
        for q in queries:
            if q["id"] in mapped_query_ids:
                continue
            mapped_results.append(
                QueryResult(
                    query_id=q["id"],
                    question=q["question"],
                    answer=None,
                    source_used=None,
                    response_time_ms=0.0,
                    dax_query=None,
                    sql_query=None,
                    error="No SDK detail row returned for this query",
                )
            )
            metrics_list.append(
                EvaluationMetrics(
                    query_id=q["id"],
                    exact_match=False,
                    semantic_match=False,
                    routing_correct=False,
                    measure_selection_correct=False,
                    response_time_acceptable=False,
                    verified_answer_used=False,
                    error_occurred=True,
                    notes="No SDK detail row returned for this query",
                )
            )

        self.last_query_results = mapped_results
        aggregate = self._calculate_aggregate_metrics(queries, metrics_list)
        official_summary = self._parse_official_summary(summary_df)

        sdk_context = {
            "mode": "sdk",
            "evaluation_id": str(evaluation_id),
            "table_name": self.table_name,
            "data_agent_stage": self.data_agent_stage,
            "workspace_name": self.workspace_name,
            "official_summary": official_summary,
            "details_row_count": int(len(details_df)),
        }

        return metrics_list, aggregate, sdk_context
    
    def _calculate_aggregate_metrics(
        self, 
        queries: List[Dict], 
        metrics_list: List[EvaluationMetrics]
    ) -> AggregateMetrics:
        """Calculate aggregate metrics across all queries"""
        
        total = len(metrics_list)
        
        # Overall metrics
        exact_match_acc = sum(m.exact_match for m in metrics_list) / total
        semantic_match_acc = sum(m.semantic_match for m in metrics_list) / total
        
        # Routing accuracy (only for queries that test routing)
        routing_queries = [m for m, q in zip(metrics_list, queries) if q.get("tests_routing", False)]
        routing_acc = sum(m.routing_correct for m in routing_queries) / len(routing_queries) if routing_queries else 0
        
        # Measure selection accuracy
        measure_queries = [m for m, q in zip(metrics_list, queries) if q.get("tests_measure_selection", False)]
        measure_acc = sum(m.measure_selection_correct for m in measure_queries) / len(measure_queries) if measure_queries else 0
        
        # Response time
        avg_time = sum(
            next((r.response_time_ms for r in self.last_query_results if r.query_id == m.query_id), 0)
            for m in metrics_list
        ) / total
        
        # Verified answer hit rate
        va_rate = sum(m.verified_answer_used for m in metrics_list) / total
        
        # Error rate
        error_rate = sum(m.error_occurred for m in metrics_list) / total
        
        # By category
        by_category = {}
        categories = set(q.get("category", "uncategorized") for q in queries)
        for category in categories:
            cat_metrics = [m for m, q in zip(metrics_list, queries) if q.get("category", "uncategorized") == category]
            by_category[category] = {
                "count": len(cat_metrics),
                "exact_match": sum(m.exact_match for m in cat_metrics) / len(cat_metrics),
                "semantic_match": sum(m.semantic_match for m in cat_metrics) / len(cat_metrics),
                "routing_correct": sum(m.routing_correct for m in cat_metrics) / len(cat_metrics)
            }
        
        # By difficulty (queries missing a "difficulty" field are grouped as "unlabeled")
        by_difficulty = {}
        difficulties = set(q.get("difficulty", "unlabeled") for q in queries)
        for difficulty in difficulties:
            diff_metrics = [m for m, q in zip(metrics_list, queries) if q.get("difficulty", "unlabeled") == difficulty]
            by_difficulty[difficulty] = {
                "count": len(diff_metrics),
                "exact_match": sum(m.exact_match for m in diff_metrics) / len(diff_metrics),
                "semantic_match": sum(m.semantic_match for m in diff_metrics) / len(diff_metrics)
            }
        
        return AggregateMetrics(
            total_queries=total,
            exact_match_accuracy=exact_match_acc,
            semantic_match_accuracy=semantic_match_acc,
            routing_accuracy=routing_acc,
            measure_selection_accuracy=measure_acc,
            avg_response_time_ms=avg_time,
            verified_answer_hit_rate=va_rate,
            error_rate=error_rate,
            by_category=by_category,
            by_difficulty=by_difficulty
        )
    
    def print_report(self, metrics: AggregateMetrics):
        """Print evaluation report"""
        print(f"\n{'='*80}")
        print("EVALUATION REPORT")
        print(f"{'='*80}\n")
        
        print(f"Total Queries: {metrics.total_queries}")
        print(f"\nOverall Accuracy:")
        print(f"  Exact Match:       {metrics.exact_match_accuracy*100:6.2f}%")
        print(f"  Semantic Match:    {metrics.semantic_match_accuracy*100:6.2f}%")
        print(f"  Routing:           {metrics.routing_accuracy*100:6.2f}%")
        print(f"  Measure Selection: {metrics.measure_selection_accuracy*100:6.2f}%")
        
        print(f"\nPerformance:")
        print(f"  Avg Response Time: {metrics.avg_response_time_ms:7.0f} ms")
        print(f"  Verified Answer Hit Rate: {metrics.verified_answer_hit_rate*100:6.2f}%")
        print(f"  Error Rate:        {metrics.error_rate*100:6.2f}%")
        
        print(f"\nBy Category:")
        for category, cat_metrics in metrics.by_category.items():
            print(f"  {category:25s} (n={cat_metrics['count']:2d}): "
                  f"Exact={cat_metrics['exact_match']*100:5.1f}%, "
                  f"Semantic={cat_metrics['semantic_match']*100:5.1f}%, "
                  f"Routing={cat_metrics['routing_correct']*100:5.1f}%")
        
        print(f"\nBy Difficulty:")
        for difficulty, diff_metrics in metrics.by_difficulty.items():
            print(f"  {difficulty:10s} (n={diff_metrics['count']:2d}): "
                  f"Exact={diff_metrics['exact_match']*100:5.1f}%, "
                  f"Semantic={diff_metrics['semantic_match']*100:5.1f}%")
        
        print(f"\n{'='*80}\n")

    def print_compatibility_report(self, custom_metrics: AggregateMetrics, sdk_context: Optional[Dict[str, Any]] = None):
        """Print side-by-side comparison between custom metrics and official SDK summary."""
        if not sdk_context:
            return

        official = sdk_context.get("official_summary", {})
        official_accuracy = official.get("accuracy")
        custom_accuracy = custom_metrics.semantic_match_accuracy

        print(f"\n{'='*80}")
        print("COMPATIBILITY REPORT (CUSTOM VS OFFICIAL SDK)")
        print(f"{'='*80}")
        print(f"Evaluation ID: {sdk_context.get('evaluation_id')}")
        print(f"Results Table: {sdk_context.get('table_name')}")
        print(f"SDK Detail Rows: {sdk_context.get('details_row_count')}")

        if official_accuracy is not None:
            delta = custom_accuracy - float(official_accuracy)
            print(f"Official Accuracy: {float(official_accuracy)*100:6.2f}%")
            print(f"Custom Semantic:  {custom_accuracy*100:6.2f}%")
            print(f"Delta:            {delta*100:+6.2f}%")
        else:
            print("Official accuracy was not found in summary columns.")
            print(f"Summary columns: {official.get('raw_columns', [])}")

        print("\nCustom-only diagnostics:")
        print(f"  Routing Accuracy:           {custom_metrics.routing_accuracy*100:6.2f}%")
        print(f"  Measure Selection Accuracy: {custom_metrics.measure_selection_accuracy*100:6.2f}%")
        print(f"  Verified Answer Hit Rate:   {custom_metrics.verified_answer_hit_rate*100:6.2f}%")
        print(f"  Error Rate:                 {custom_metrics.error_rate*100:6.2f}%")
        print(f"{'='*80}\n")
    
    def save_results(
        self,
        metrics_list: List[EvaluationMetrics],
        aggregate: AggregateMetrics,
        output_path: str,
        sdk_context: Optional[Dict[str, Any]] = None,
    ):
        """Save evaluation results to JSON file"""
        results = {
            "evaluation_date": datetime.now().isoformat(),
            "agent_id": self.agent_id,
            "workspace_id": self.workspace_id,
            "mode": "sdk" if self.sdk_mode else "simulation",
            "illustrative_only": bool(self.simulation_mode),
            "aggregate_metrics": asdict(aggregate),
            "detailed_metrics": [asdict(m) for m in metrics_list],
            "query_results": [asdict(result) for result in self.last_query_results],
        }

        if sdk_context:
            results["sdk_evaluation"] = {
                "evaluation_id": sdk_context.get("evaluation_id"),
                "table_name": sdk_context.get("table_name"),
                "data_agent_stage": sdk_context.get("data_agent_stage"),
                "workspace_name": sdk_context.get("workspace_name"),
                "official_summary": sdk_context.get("official_summary", {}),
                "details_row_count": sdk_context.get("details_row_count"),
            }
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"Results saved to {output_path}")

    def save_official_details_csv(self, csv_path: str):
        """Persist SDK detail rows for deeper diagnostics."""
        if self.sdk_details_df is None:
            print("No SDK details DataFrame found; skipping CSV export.")
            return
        self.sdk_details_df.to_csv(csv_path, index=False)
        print(f"Official SDK details saved to {csv_path}")


def main():
    parser = argparse.ArgumentParser(description="Evaluate Fabric Data Agent")
    parser.add_argument("--workspace-id", default="<workspace_id>", 
                       help="Fabric workspace ID")
    parser.add_argument("--agent-id", default="<agent_id>",
                       help="Data agent ID")
    parser.add_argument("--dataset", default="evaluation/challenge/uk-legal.json",
                       help="Path to evaluation dataset")
    parser.add_argument("--output", default="evaluation_results.json",
                       help="Path to output results")
    parser.add_argument("--simulation", action="store_true",
                       help="Run a seeded, illustrative dry-run (no real agent calls). Not measured accuracy.")
    parser.add_argument("--sdk-mode", action="store_true",
                       help="Use official Fabric SDK evaluation mode (real, measured accuracy)")
    parser.add_argument("--seed", type=int, default=42,
                       help="Random seed for --simulation, so illustrative runs are reproducible")
    parser.add_argument("--step", type=int, choices=[1,2,3,4,5,6], default=2,
                       help="USER_GUIDE.md step to simulate (1=semantic-model baseline, 2=after Prep for AI, "
                            "3=Lakehouse attached, 4=Lakehouse tuned, 5=derived tables+routing, 6=bonus ontology)")
    parser.add_argument("--workspace-name", default=None,
                       help="Fabric workspace name for SDK mode (optional)")
    parser.add_argument("--table-name", default="evaluation_output",
                       help="Output table name used by official SDK mode")
    parser.add_argument("--stage", choices=["production", "sandbox"], default="production",
                       help="Data agent stage for official SDK mode")
    parser.add_argument("--critic-prompt", default=None,
                       help="Custom critic prompt text for official SDK mode")
    parser.add_argument("--critic-prompt-file", default=None,
                       help="Path to a text file containing the custom critic prompt")
    parser.add_argument("--save-official-details-csv", action="store_true",
                       help="When in SDK mode, also save official detail rows to CSV")
    parser.add_argument("--official-details-output", default=None,
                       help="Optional path for official detail CSV output")
    
    args = parser.parse_args()

    if args.simulation and args.sdk_mode:
        parser.error("--simulation and --sdk-mode are mutually exclusive")
    if not args.simulation and not args.sdk_mode:
        parser.error("Choose one mode: --simulation (illustrative) or --sdk-mode (real evaluation)")

    if args.critic_prompt and args.critic_prompt_file:
        parser.error("Use either --critic-prompt or --critic-prompt-file, not both")

    critic_prompt = args.critic_prompt
    if args.critic_prompt_file:
        critic_prompt = Path(args.critic_prompt_file).read_text(encoding="utf-8")

    if args.simulation:
        import random
        random.seed(args.seed)
    
    # Initialize evaluator
    evaluator = DataAgentEvaluator(
        workspace_id=args.workspace_id,
        agent_id=args.agent_id,
        simulation_mode=args.simulation,
        simulation_step=args.step if args.simulation else 2,
        sdk_mode=args.sdk_mode,
        workspace_name=args.workspace_name,
        table_name=args.table_name,
        data_agent_stage=args.stage,
        critic_prompt=critic_prompt,
    )

    sdk_context = None
    if args.sdk_mode:
        metrics_list, aggregate, sdk_context = evaluator.evaluate_with_sdk(args.dataset)
    else:
        metrics_list, aggregate = evaluator.evaluate_all(args.dataset)
    
    # Print report
    evaluator.print_report(aggregate)
    evaluator.print_compatibility_report(aggregate, sdk_context)
    
    # Save results
    evaluator.save_results(metrics_list, aggregate, args.output, sdk_context=sdk_context)

    if args.sdk_mode and args.save_official_details_csv:
        if args.official_details_output:
            csv_path = args.official_details_output
        else:
            output_path = Path(args.output)
            csv_path = str(output_path.with_name(f"{output_path.stem}_official_details.csv"))
        evaluator.save_official_details_csv(csv_path)
    
    # Return exit code based on accuracy
    if aggregate.semantic_match_accuracy >= 0.90:
        print("PASS: Accuracy >= 90%")
        return 0
    elif aggregate.semantic_match_accuracy >= 0.75:
        print("WARNING: Accuracy between 75-90%")
        return 1
    else:
        print("FAIL: Accuracy < 75%")
        return 2


if __name__ == "__main__":
    import sys
    sys.exit(main())


