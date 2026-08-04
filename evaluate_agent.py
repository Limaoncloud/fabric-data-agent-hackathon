"""
Fabric Data Agent Evaluation Framework

This script evaluates a Fabric Data Agent's performance across multiple dimensions:
- Query accuracy (exact match, semantic match)
- Routing accuracy (correct data source selection)
- Measure selection accuracy (for semantic models)
- Response consistency
- Response time

Usage:
    python evaluate_agent.py --config evaluation_config.json --output results.json

Requirements:
    pip install azure-identity azure-ai-projects pandas numpy
"""

import json
import time
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import argparse

# Optional imports for actual Fabric API calls
try:
    from azure.identity import DefaultAzureCredential
    # from azure.ai.projects import DataAgentClient  # Hypothetical - replace with actual SDK
    AZURE_SDK_AVAILABLE = True
except ImportError:
    AZURE_SDK_AVAILABLE = False
    print("Warning: Azure SDK not available. Running in simulation mode.")


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
        simulation_step: int = 4
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
        
        if not simulation_mode and AZURE_SDK_AVAILABLE:
            self.credential = DefaultAzureCredential()
            # self.client = DataAgentClient(credential=self.credential)
            print(f"Initialized evaluator for agent {agent_id}")
        else:
            print(f"Running in SIMULATION MODE - Step {simulation_step}")
    
    def load_evaluation_dataset(self, dataset_path: str) -> Dict[str, Any]:
        """Load evaluation dataset from JSON file"""
        with open(dataset_path, 'r') as f:
            return json.load(f)
    
    def execute_query(self, question: str, ground_truth_answer=None, expected_source=None) -> QueryResult:
        """
        Execute a single query against the data agent
        
        In production, this would call the actual Fabric Data Agent API.
        In simulation mode, it returns mock results.
        """
        start_time = time.time()
        
        if self.simulation_mode:
            # Simulate response
            time.sleep(0.05)  # Simulate processing time
            
            # Define accuracy rates per step
            step_configs = {
                1: {"accuracy": 0.40, "routing": 0.50, "response_time": (2000, 5000), "error_rate": 0.30},  # Raw data
                2: {"accuracy": 0.55, "routing": 0.60, "response_time": (1800, 4500), "error_rate": 0.20},  # Cleaned data
                3: {"accuracy": 0.65, "routing": 0.70, "response_time": (1500, 4000), "error_rate": 0.15},  # Basic model
                4: {"accuracy": 0.95, "routing": 0.95, "response_time": (800, 2000), "error_rate": 0.02},   # Optimized model
                5: {"accuracy": 0.96, "routing": 0.96, "response_time": (700, 1800), "error_rate": 0.02},   # With ontology
                6: {"accuracy": 0.93, "routing": 0.92, "response_time": (900, 2200), "error_rate": 0.03}    # Multi-source routing
            }
            
            config = step_configs.get(self.simulation_step, step_configs[4])
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
            correct_source = expected_source if expected_source else "ClientCasePortfolio"
            if random.random() < config["routing"]:
                # Correct routing
                source = correct_source
            else:
                # Wrong routing
                source = "FinancialTransactions" if correct_source == "ClientCasePortfolio" else "ClientCasePortfolio"
            
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
        else:
            # TODO: Replace with actual Fabric Data Agent API call
            # Example structure:
            # response = self.client.query(
            #     workspace_id=self.workspace_id,
            #     agent_id=self.agent_id,
            #     question=question
            # )
            
            result = QueryResult(
                query_id="",
                question=question,
                answer="Not implemented - add actual API call",
                source_used=None,
                response_time_ms=(time.time() - start_time) * 1000,
                dax_query=None,
                sql_query=None,
                error="Actual API integration not implemented"
            )
        
        return result
    
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
            exact = abs(float(actual) - float(expected)) < 0.01
            semantic = abs(float(actual) - float(expected)) / float(expected) < 0.05  # 5% tolerance
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
        print(f"Mode: {'SIMULATION' if self.simulation_mode else 'PRODUCTION'}")
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
            status = "✓" if metrics.exact_match else "✗"
            print(f"  {status} Exact: {metrics.exact_match} | Semantic: {metrics.semantic_match} | "
                  f"Routing: {metrics.routing_correct} | Time: {result.response_time_ms:.0f}ms")
            if metrics.notes:
                print(f"     Notes: {metrics.notes}")
        
        # Calculate aggregate metrics
        aggregate = self._calculate_aggregate_metrics(queries, metrics_list)
        
        return metrics_list, aggregate
    
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
            next((r.response_time_ms for r in results if r.query_id == m.query_id), 0)
            for m in metrics_list
        ) / total
        
        # Verified answer hit rate
        va_rate = sum(m.verified_answer_used for m in metrics_list) / total
        
        # Error rate
        error_rate = sum(m.error_occurred for m in metrics_list) / total
        
        # By category
        by_category = {}
        categories = set(q["category"] for q in queries)
        for category in categories:
            cat_metrics = [m for m, q in zip(metrics_list, queries) if q["category"] == category]
            by_category[category] = {
                "count": len(cat_metrics),
                "exact_match": sum(m.exact_match for m in cat_metrics) / len(cat_metrics),
                "semantic_match": sum(m.semantic_match for m in cat_metrics) / len(cat_metrics),
                "routing_correct": sum(m.routing_correct for m in cat_metrics) / len(cat_metrics)
            }
        
        # By difficulty
        by_difficulty = {}
        difficulties = set(q["difficulty"] for q in queries)
        for difficulty in difficulties:
            diff_metrics = [m for m, q in zip(metrics_list, queries) if q["difficulty"] == difficulty]
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
    
    def save_results(self, metrics_list: List[EvaluationMetrics], 
                     aggregate: AggregateMetrics, output_path: str):
        """Save evaluation results to JSON file"""
        results = {
            "evaluation_date": datetime.now().isoformat(),
            "agent_id": self.agent_id,
            "workspace_id": self.workspace_id,
            "aggregate_metrics": asdict(aggregate),
            "detailed_metrics": [asdict(m) for m in metrics_list]
        }
        
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"Results saved to {output_path}")


# Global variable to store results (hack for simulation)
results = []


def main():
    parser = argparse.ArgumentParser(description="Evaluate Fabric Data Agent")
    parser.add_argument("--workspace-id", default="<workspace_id>", 
                       help="Fabric workspace ID")
    parser.add_argument("--agent-id", default="<agent_id>",
                       help="Data agent ID")
    parser.add_argument("--dataset", default="evaluation_dataset.json",
                       help="Path to evaluation dataset")
    parser.add_argument("--output", default="evaluation_results.json",
                       help="Path to output results")
    parser.add_argument("--simulation", action="store_true",
                       help="Run in simulation mode (no actual API calls)")
    parser.add_argument("--step", type=int, choices=[1,2,3,4,5,6], default=4,
                       help="Demo step to simulate (1=raw, 2=cleaned, 3=basic, 4=optimized, 5=ontology, 6=routing)")
    
    args = parser.parse_args()
    
    # Initialize evaluator
    evaluator = DataAgentEvaluator(
        workspace_id=args.workspace_id,
        agent_id=args.agent_id,
        simulation_mode=args.simulation,
        simulation_step=args.step if args.simulation else 4
    )
    
    # Run evaluation
    metrics_list, aggregate = evaluator.evaluate_all(args.dataset)
    
    # Print report
    evaluator.print_report(aggregate)
    
    # Save results
    evaluator.save_results(metrics_list, aggregate, args.output)
    
    # Return exit code based on accuracy
    if aggregate.semantic_match_accuracy >= 0.90:
        print("✓ PASS: Accuracy >= 90%")
        return 0
    elif aggregate.semantic_match_accuracy >= 0.75:
        print("⚠ WARNING: Accuracy between 75-90%")
        return 1
    else:
        print("✗ FAIL: Accuracy < 75%")
        return 2


if __name__ == "__main__":
    import sys
    sys.exit(main())
