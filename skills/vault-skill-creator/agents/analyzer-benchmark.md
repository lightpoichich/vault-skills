# Benchmark Analyzer Agent

Surface patterns and anomalies across benchmark runs that the aggregate metrics hide. This agent does not suggest skill improvements; that belongs to the improvement step (`agents/analyzer.md` for a blind comparison, SKILL.md "Improving the skill" otherwise).

## Inputs

- `benchmark_data_path`: path to the in-progress `benchmark.json` with all run results
- `skill_path`: path to the skill being benchmarked
- `output_path`: where to save the notes

## Process

### Step 1: Read the benchmark data

Read `benchmark.json`, the configurations tested (`with_skill` and `without_skill`, or `new_skill` and `old_skill`) and the `run_summary` aggregates already computed. Do not repeat what the aggregates already say.

### Step 2: Per-assertion patterns

For each expectation across all runs:
- always passes in both configurations: may not differentiate skill value;
- always fails in both configurations: may be broken or beyond capability;
- passes with the skill, fails without: the skill adds value here;
- fails with the skill, passes without: the skill may be hurting;
- highly variable: flaky expectation or non-deterministic behavior.

### Step 3: Cross-eval patterns

Are some eval types consistently harder or easier? Do some evals show high variance while others are stable? Are there results that contradict expectations?

### Step 4: Metrics patterns

On `time_seconds`, `tokens`, `tool_calls`: does the skill increase execution time substantially, is resource usage highly variable, do outlier runs skew the aggregates?

### Step 5: Write the notes

Save to `{output_path}` as a JSON array of strings (`references/schemas.md`, section "Analyzer notes"). Each note states one specific observation, grounded in the data, naming the evals, expectations or runs concerned, and helps interpret a number the aggregates do not show. No quality judgment on the outputs, no speculation about causes without evidence.

Examples:
- "Assertion 'Output is a PDF file' passes 100% in both configurations, may not differentiate skill value"
- "Eval 3 shows high variance (50% ± 40%), run 2 had an unusual failure that may be flaky"
- "Without-skill runs consistently fail on table extraction expectations (0% pass rate)"
- "Skill adds 13s average execution time but improves pass rate by 50%"
- "Token usage is 80% higher with skill, primarily due to script output parsing"
- "All 3 without-skill runs for eval 1 produced empty output"
