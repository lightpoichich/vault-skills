# JSON Schemas

The only home of the JSON structures used by `vault-skill-creator` and its agents. The eval viewer and `scripts/aggregate_benchmark.py` read these field names exactly; a renamed or misplaced field shows up as empty or zero in the viewer.

Timestamps are ISO 8601 (`YYYY-MM-DDThh:mm:ssZ`); the placeholders below stand for real values.

## evals.json

Test cases of a skill. Located at `evals/evals.json` within the skill directory. Written by the orchestrator (the session running `vault-skill-creator`): prompts first, `expectations` added while the runs are in progress.

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's example prompt",
      "expected_output": "Description of expected result",
      "files": ["evals/files/sample1.pdf"],
      "expectations": [
        "The output includes X",
        "The skill used script Y"
      ]
    }
  ]
}
```

Fields:
- `skill_name`: name matching the skill's frontmatter
- `evals[].id`: unique integer identifier
- `evals[].prompt`: the task to execute
- `evals[].expected_output`: human-readable description of success
- `evals[].files`: optional list of input file paths, relative to the skill root
- `evals[].expectations`: list of verifiable statements (also called assertions)

## eval_metadata.json

One per test case, at `<workspace>/iteration-N/<eval-name>/eval_metadata.json`. Written by the orchestrator when the runs are spawned; `assertions` filled in afterwards.

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name-here",
  "prompt": "The user's task prompt",
  "assertions": []
}
```

Fields:
- `eval_id`: integer, same as `evals[].id`
- `eval_name`: descriptive name of what the case tests, also the directory name
- `prompt`: the task prompt
- `assertions`: list of verifiable statements, same content as `evals[].expectations`

## timing.json

Wall clock timing for a run. Located at `<run-dir>/timing.json`. Written by the orchestrator: `total_tokens`, `duration_ms` and `total_duration_seconds` come from the subagent completion notification and are saved as soon as it arrives, since they are persisted nowhere else; the `executor_*` and `grader_*` fields come from the orchestrator's own clock around each spawn. The grader reads this file and copies the durations into `grading.json.timing`.

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3,
  "executor_start": "<timestamp>",
  "executor_end": "<timestamp>",
  "executor_duration_seconds": 165.0,
  "grader_start": "<timestamp>",
  "grader_end": "<timestamp>",
  "grader_duration_seconds": 26.0
}
```

## metrics.json

Output from the executor agent. Located at `<run-dir>/outputs/metrics.json`.

```json
{
  "tool_calls": {
    "Read": 5,
    "Write": 2,
    "Bash": 8,
    "Edit": 1,
    "Glob": 2,
    "Grep": 0
  },
  "total_tool_calls": 18,
  "total_steps": 6,
  "files_created": ["filled_form.pdf", "field_values.json"],
  "errors_encountered": 0,
  "output_chars": 12450,
  "transcript_chars": 3200
}
```

Fields:
- `tool_calls`: count per tool type
- `total_tool_calls`: sum of all tool calls
- `total_steps`: number of major execution steps
- `files_created`: list of output files created
- `errors_encountered`: number of errors during execution
- `output_chars`: total character count of output files (proxy for tokens)
- `transcript_chars`: character count of the transcript

## grading.json

Output from the grader agent (`agents/grader.md`). Located at `<run-dir>/grading.json`, sibling of `outputs/`. The `expectations[]` entries use `text`, `passed` and `evidence`, no other names.

```json
{
  "expectations": [
    {
      "text": "The output includes the name 'John Smith'",
      "passed": true,
      "evidence": "Found in transcript Step 3: 'Extracted names: John Smith, Sarah Johnson'"
    },
    {
      "text": "The spreadsheet has a SUM formula in cell B10",
      "passed": false,
      "evidence": "No spreadsheet was created. The output was a text file."
    },
    {
      "text": "The assistant used the skill's OCR script",
      "passed": true,
      "evidence": "Transcript Step 2 shows: 'Tool: Bash - python ocr_script.py image.png'"
    }
  ],
  "summary": {
    "passed": 2,
    "failed": 1,
    "total": 3,
    "pass_rate": 0.67
  },
  "execution_metrics": {
    "tool_calls": {
      "Read": 5,
      "Write": 2,
      "Bash": 8
    },
    "total_tool_calls": 15,
    "total_steps": 6,
    "errors_encountered": 0,
    "output_chars": 12450,
    "transcript_chars": 3200
  },
  "timing": {
    "executor_duration_seconds": 165.0,
    "grader_duration_seconds": 26.0,
    "total_duration_seconds": 191.0
  },
  "claims": [
    {
      "claim": "The form has 12 fillable fields",
      "type": "factual",
      "verified": true,
      "evidence": "Counted 12 fields in field_info.json"
    },
    {
      "claim": "All required fields were populated",
      "type": "quality",
      "verified": false,
      "evidence": "Reference section was left blank despite data being available"
    }
  ],
  "user_notes_summary": {
    "uncertainties": ["Used older reference data, may be stale"],
    "needs_review": [],
    "workarounds": ["Fell back to text overlay for non-fillable fields"]
  },
  "eval_feedback": {
    "suggestions": [
      {
        "assertion": "The output includes the name 'John Smith'",
        "reason": "A hallucinated document that mentions the name would also pass. Check it appears as the primary contact with matching phone and email from the input."
      },
      {
        "reason": "No assertion checks whether the extracted phone numbers match the input. Incorrect numbers in the output went uncaught."
      }
    ],
    "overall": "Assertions check presence but not correctness. Consider adding content verification."
  }
}
```

Fields:
- `expectations[]`: graded expectations
  - `text`: the original expectation text
  - `passed`: boolean
  - `evidence`: specific quote or description supporting the verdict
- `summary`: `passed`, `failed`, `total` counts and `pass_rate` (0.0 to 1.0)
- `execution_metrics`: copied from the executor's `metrics.json` when available
- `timing`: copied from `timing.json` when available (`executor_duration_seconds`, `grader_duration_seconds`, `total_duration_seconds`)
- `claims[]`: claims extracted from the output and verified
  - `claim`: the statement being verified
  - `type`: `factual`, `process` or `quality`
  - `verified`: boolean
  - `evidence`: supporting or contradicting evidence
- `user_notes_summary`: issues flagged by the executor in `user_notes.md`
  - `uncertainties`: things the executor was not sure about
  - `needs_review`: items requiring human attention
  - `workarounds`: places where the skill did not work as expected
- `eval_feedback`: optional, present only when the grader has something to raise
  - `suggestions[]`: each with a `reason` and, when it relates to one, the `assertion` text
  - `overall`: brief assessment, or "No suggestions, evals look solid"

## feedback.json

Written by the eval viewer when the user clicks "Submit All Reviews" (served mode: in the workspace; static mode: downloaded, to copy into the workspace). Read by the orchestrator at the end of an iteration.

```json
{
  "reviews": [
    {"run_id": "eval-0-with_skill", "feedback": "the chart is missing axis labels", "timestamp": "<timestamp>"},
    {"run_id": "eval-1-with_skill", "feedback": "", "timestamp": "<timestamp>"},
    {"run_id": "eval-2-with_skill", "feedback": "perfect, love this", "timestamp": "<timestamp>"}
  ],
  "status": "complete"
}
```

Fields:
- `reviews[].run_id`: `<eval-name>-<configuration>`
- `reviews[].feedback`: free text; empty means the user found the output fine
- `status`: `complete` once submitted

## benchmark.json

Output of `scripts/aggregate_benchmark.py`, or written by hand with the same structure. Located at `<workspace>/iteration-N/benchmark.json`.

```json
{
  "metadata": {
    "skill_name": "pdf",
    "skill_path": "/path/to/pdf",
    "executor_model": "<model-id>",
    "analyzer_model": "<model-id>",
    "timestamp": "<timestamp>",
    "evals_run": [1, 2, 3],
    "runs_per_configuration": 3
  },

  "runs": [
    {
      "eval_id": 1,
      "eval_name": "Ocean",
      "configuration": "with_skill",
      "run_number": 1,
      "result": {
        "pass_rate": 0.85,
        "passed": 6,
        "failed": 1,
        "total": 7,
        "time_seconds": 42.5,
        "tokens": 3800,
        "tool_calls": 18,
        "errors": 0
      },
      "expectations": [
        {"text": "...", "passed": true, "evidence": "..."}
      ],
      "notes": [
        "Used older reference data, may be stale",
        "Fell back to text overlay for non-fillable fields"
      ]
    }
  ],

  "run_summary": {
    "with_skill": {
      "pass_rate": {"mean": 0.85, "stddev": 0.05, "min": 0.80, "max": 0.90},
      "time_seconds": {"mean": 45.0, "stddev": 12.0, "min": 32.0, "max": 58.0},
      "tokens": {"mean": 3800, "stddev": 400, "min": 3200, "max": 4100}
    },
    "without_skill": {
      "pass_rate": {"mean": 0.35, "stddev": 0.08, "min": 0.28, "max": 0.45},
      "time_seconds": {"mean": 32.0, "stddev": 8.0, "min": 24.0, "max": 42.0},
      "tokens": {"mean": 2100, "stddev": 300, "min": 1800, "max": 2500}
    },
    "delta": {
      "pass_rate": "+0.50",
      "time_seconds": "+13.0",
      "tokens": "+1700"
    }
  },

  "notes": [
    "Assertion 'Output is a PDF file' passes 100% in both configurations, may not differentiate skill value",
    "Eval 3 shows high variance (50% ± 40%), may be flaky or model-dependent",
    "Without-skill runs consistently fail on table extraction expectations",
    "Skill adds 13s average execution time but improves pass rate by 50%"
  ]
}
```

Fields:
- `metadata`: `skill_name`, `skill_path`, `executor_model`, `analyzer_model`, `timestamp`, `evals_run` (ids or names), `runs_per_configuration`
- `runs[]`: one entry per run
  - `eval_id`: numeric identifier
  - `eval_name`: human-readable name, used as section header in the viewer
  - `configuration`: exactly `with_skill` and `without_skill` (new skill), or `new_skill` and `old_skill` (improving an existing skill); the viewer groups and colours on this string
  - `run_number`: integer (1, 2, 3...)
  - `result`: `pass_rate`, `passed`, `failed`, `total`, `time_seconds`, `tokens`, `tool_calls`, `errors`, nested under `result` and not at the run's top level
  - `expectations[]`: same shape as `grading.json.expectations`
  - `notes[]`: the executor's `user_notes_summary` items, flattened
- `run_summary`: per configuration, `pass_rate`, `time_seconds` and `tokens` objects with `mean`, `stddev`, `min`, `max`; `delta` holds signed difference strings
- `notes[]`: observations from `agents/analyzer-benchmark.md`

## Analyzer notes

Output of `agents/analyzer-benchmark.md`, saved at the `output_path` given in its prompt: a JSON array of strings, merged into `benchmark.json.notes`.

```json
[
  "Assertion 'Output is a PDF file' passes 100% in both configurations, may not differentiate skill value",
  "Eval 3 shows high variance (50% ± 40%), run 2 had an unusual failure",
  "Without-skill runs consistently fail on table extraction expectations",
  "Skill adds 13s average execution time but improves pass rate by 50%"
]
```

## comparison.json

Output of the blind comparator (`agents/comparator.md`). Located at `<grading-dir>/comparison-N.json`.

```json
{
  "winner": "A",
  "reasoning": "Output A provides a complete solution with proper formatting and all required fields. Output B is missing the date field and has formatting inconsistencies.",
  "rubric": {
    "A": {
      "content": {
        "correctness": 5,
        "completeness": 5,
        "accuracy": 4
      },
      "structure": {
        "organization": 4,
        "formatting": 5,
        "usability": 4
      },
      "content_score": 4.7,
      "structure_score": 4.3,
      "overall_score": 9.0
    },
    "B": {
      "content": {
        "correctness": 3,
        "completeness": 2,
        "accuracy": 3
      },
      "structure": {
        "organization": 3,
        "formatting": 2,
        "usability": 3
      },
      "content_score": 2.7,
      "structure_score": 2.7,
      "overall_score": 5.4
    }
  },
  "output_quality": {
    "A": {
      "score": 9,
      "strengths": ["Complete solution", "Well-formatted", "All fields present"],
      "weaknesses": ["Minor style inconsistency in header"]
    },
    "B": {
      "score": 5,
      "strengths": ["Readable output", "Correct basic structure"],
      "weaknesses": ["Missing date field", "Formatting inconsistencies", "Partial data extraction"]
    }
  },
  "expectation_results": {
    "A": {
      "passed": 4,
      "total": 5,
      "pass_rate": 0.80,
      "details": [
        {"text": "Output includes name", "passed": true},
        {"text": "Output includes date", "passed": true},
        {"text": "Format is PDF", "passed": true},
        {"text": "Contains signature", "passed": false},
        {"text": "Readable text", "passed": true}
      ]
    },
    "B": {
      "passed": 3,
      "total": 5,
      "pass_rate": 0.60,
      "details": [
        {"text": "Output includes name", "passed": true},
        {"text": "Output includes date", "passed": false},
        {"text": "Format is PDF", "passed": true},
        {"text": "Contains signature", "passed": false},
        {"text": "Readable text", "passed": true}
      ]
    }
  }
}
```

Fields:
- `winner`: `A`, `B` or `TIE`
- `reasoning`: why the winner was chosen, or why it is a tie
- `rubric`: per output, `content` scores (correctness, completeness, accuracy) and `structure` scores (organization, formatting, usability) on 1 to 5; `content_score` and `structure_score` are the averages (1 to 5); `overall_score` is the combined score scaled to 1 to 10
- `output_quality`: per output, `score` (1 to 10, matching `overall_score`), `strengths[]`, `weaknesses[]`
- `expectation_results`: per output, `passed`, `total`, `pass_rate`, `details[]`; omitted entirely when no expectations were provided

## analysis.json

Output of the post-hoc analyzer (`agents/analyzer.md`). Located at `<grading-dir>/analysis.json`.

```json
{
  "comparison_summary": {
    "winner": "A",
    "winner_skill": "path/to/winner/skill",
    "loser_skill": "path/to/loser/skill",
    "comparator_reasoning": "Brief summary of why comparator chose winner"
  },
  "winner_strengths": [
    "Clear step-by-step instructions for handling multi-page documents",
    "Included validation script that caught formatting errors",
    "Explicit guidance on fallback behavior when OCR fails"
  ],
  "loser_weaknesses": [
    "Vague instruction 'process the document appropriately' led to inconsistent behavior",
    "No script for validation, agent had to improvise and made errors",
    "No guidance on OCR failure, agent gave up instead of trying alternatives"
  ],
  "instruction_following": {
    "winner": {
      "score": 9,
      "issues": ["Minor: skipped optional logging step"]
    },
    "loser": {
      "score": 6,
      "issues": [
        "Did not use the skill's formatting template",
        "Invented own approach instead of following step 3",
        "Missed the 'validate output' instruction"
      ]
    }
  },
  "improvement_suggestions": [
    {
      "priority": "high",
      "category": "instructions",
      "suggestion": "Replace 'process the document appropriately' with explicit steps: 1) Extract text, 2) Identify sections, 3) Format per template",
      "expected_impact": "Would eliminate ambiguity that caused inconsistent behavior"
    },
    {
      "priority": "high",
      "category": "tools",
      "suggestion": "Add validate_output.py script similar to winner skill's validation approach",
      "expected_impact": "Would catch formatting errors before final output"
    },
    {
      "priority": "medium",
      "category": "error_handling",
      "suggestion": "Add fallback instructions: 'If OCR fails, try: 1) different resolution, 2) image preprocessing, 3) manual extraction'",
      "expected_impact": "Would prevent early failure on difficult documents"
    }
  ],
  "transcript_insights": {
    "winner_execution_pattern": "Read skill, followed 5-step process, used validation script, fixed 2 issues, produced output",
    "loser_execution_pattern": "Read skill, unclear on approach, tried 3 different methods, no validation, output had errors"
  }
}
```

Fields:
- `comparison_summary`: `winner`, both skill paths, `comparator_reasoning`
- `winner_strengths[]`, `loser_weaknesses[]`: specific, quoted where possible
- `instruction_following`: per side, `score` (1 to 10) and `issues[]`
- `improvement_suggestions[]`: `priority` (`high`: would likely change the outcome; `medium`: better quality, same outcome; `low`: marginal), `category` (`instructions`, `tools`, `examples`, `error_handling`, `structure`, `references`), `suggestion`, `expected_impact`
- `transcript_insights`: one-line execution pattern per side

## Trigger eval set

Input of `scripts/run_loop.py` for description optimization. Written by the orchestrator, reviewed by the user through `assets/eval_review.html` (exported as `~/Downloads/eval_set.json`).

```json
[
  {"query": "the user prompt", "should_trigger": true},
  {"query": "another prompt", "should_trigger": false}
]
```

Fields:
- `query`: a realistic user prompt
- `should_trigger`: whether the skill is expected to trigger on it

## history.json

Version progression across improvement iterations. Located at the workspace root.

```json
{
  "started_at": "<timestamp>",
  "skill_name": "pdf",
  "current_best": "v2",
  "iterations": [
    {
      "version": "v0",
      "parent": null,
      "expectation_pass_rate": 0.65,
      "grading_result": "baseline",
      "is_current_best": false
    },
    {
      "version": "v1",
      "parent": "v0",
      "expectation_pass_rate": 0.75,
      "grading_result": "won",
      "is_current_best": false
    },
    {
      "version": "v2",
      "parent": "v1",
      "expectation_pass_rate": 0.85,
      "grading_result": "won",
      "is_current_best": true
    }
  ]
}
```

Fields:
- `started_at`: when improvement started
- `skill_name`: name of the skill being improved
- `current_best`: version identifier of the best performer
- `iterations[].version`: version identifier (v0, v1, ...)
- `iterations[].parent`: parent version this was derived from
- `iterations[].expectation_pass_rate`: pass rate from grading
- `iterations[].grading_result`: `baseline`, `won`, `lost` or `tie`
- `iterations[].is_current_best`: whether this is the current best version
