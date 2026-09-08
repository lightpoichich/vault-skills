# Post-hoc Analyzer Agent

Analyze a blind comparison result to explain why the winner won and produce improvement suggestions for the losing skill. For the analysis of benchmark runs, see `agents/analyzer-benchmark.md`.

## Role

After the blind comparator has picked a winner, unblind the result by reading both skills and both transcripts. The output is actionable: what made the winner better, and which concrete changes would improve the loser.

## Inputs

- `winner`: `A` or `B`, from the blind comparison
- `winner_skill_path`: path to the skill that produced the winning output
- `winner_transcript_path`: path to the winner's execution transcript
- `loser_skill_path`: path to the skill that produced the losing output
- `loser_transcript_path`: path to the loser's execution transcript
- `comparison_result_path`: path to the blind comparator's JSON output
- `output_path`: where to save the analysis

## Process

### Step 1: Read the comparison result

Read `comparison_result_path`. Note the winning side, the reasoning and the scores: what the comparator valued in the winning output.

### Step 2: Read both skills

Read each SKILL.md and its key referenced files. Identify the structural differences: clarity and specificity of instructions, script and tool usage, example coverage, edge case handling.

### Step 3: Read both transcripts

Compare the execution patterns: how closely each run followed its skill, which tools were used differently, where the loser diverged from optimal behavior, whether either hit errors and how it recovered.

### Step 4: Score instruction following

For each transcript, check whether the agent followed the skill's explicit instructions, used its tools and scripts, missed opportunities to use skill content, or added steps the skill did not ask for. Score 1 to 10 and list the specific issues.

### Step 5: Explain the outcome

List what made the winner better: clearer instructions, better scripts or tools, more comprehensive examples, better error handling guidance. List what held the loser back: ambiguous instructions, missing tools that forced workarounds, gaps in edge case coverage, poor error handling. Quote the skills and transcripts; "instructions were unclear" is not a finding. Check causation: did the skill weakness cause the worse output, or is it incidental?

### Step 6: Write improvement suggestions

For the losing skill: instruction changes, tools or scripts to add or modify, examples to include, edge cases to address. Each suggestion is a concrete change with a category (`instructions`, `tools`, `examples`, `error_handling`, `structure`, `references`) and a priority (`high`: would likely have changed the outcome; `medium`: better quality, same outcome; `low`: marginal). Order by impact and prefer changes that would also help on other evals. The goal is the skill, not a critique of the agent.

### Step 7: Write the analysis

Save to `{output_path}` with the structure of `references/schemas.md`, section `analysis.json`. Report what happened, without editorializing.
