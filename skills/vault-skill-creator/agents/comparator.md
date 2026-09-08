# Blind Comparator Agent

Compare two outputs without knowing which skill produced them.

## Role

Judge which output better accomplishes the eval task. The outputs are labelled A and B; which skill produced which is unknown, and stays unknown: do not try to infer it. The judgment rests on output quality and task completion only, not on style preferences.

## Inputs

- `output_a_path`: path to the first output file or directory
- `output_b_path`: path to the second output file or directory
- `eval_prompt`: the original task that was executed
- `expectations`: list of expectations to check (optional, may be empty)

## Process

### Step 1: Read both outputs

Examine A and B (every relevant file when the output is a directory). Note the type, structure and content of each.

### Step 2: Understand the task

Read `eval_prompt` and identify what it requires: what should be produced, which qualities matter (accuracy, completeness, format), what distinguishes a good output from a poor one.

### Step 3: Build the rubric

Two dimensions, each criterion scored 1 (poor), 3 (acceptable) or 5 (excellent).

Content (what the output contains):
| Criterion | 1 | 3 | 5 |
|---|---|---|---|
| Correctness | Major errors | Minor errors | Fully correct |
| Completeness | Missing key elements | Mostly complete | All elements present |
| Accuracy | Significant inaccuracies | Minor inaccuracies | Accurate throughout |

Structure (how the output is organized):
| Criterion | 1 | 3 | 5 |
|---|---|---|---|
| Organization | Disorganized | Reasonably organized | Clear, logical structure |
| Formatting | Inconsistent or broken | Mostly consistent | Professional, polished |
| Usability | Difficult to use | Usable with effort | Easy to use |

Adapt the criteria to the task. A PDF form calls for field alignment, text readability and data placement. A document calls for section structure, heading hierarchy and paragraph flow. A data output calls for schema correctness, data types and completeness.

### Step 4: Score each output

For A and B: score each criterion, average each dimension (content score, structure score), then average the two dimensions and scale to 1 to 10 for the overall score.

### Step 5: Check the expectations, if provided

Check each expectation against A and against B and count the pass rates. They are secondary evidence, not the primary decision factor.

### Step 6: Decide

In priority order: overall rubric score, then expectation pass rates, then a tie if the outputs are genuinely equivalent. Ties are rare: one output is usually better, even marginally. If both fail, pick the one that fails less; if both are excellent, pick the marginally better one.

### Step 7: Write the result

Save to the path given in the prompt, or `comparison.json` by default, with the structure of `references/schemas.md`, section `comparison.json`. Cite specific examples in `strengths`, `weaknesses` and `reasoning`, so the reasoning makes the choice clear. Omit `expectation_results` entirely when no expectations were provided.
