# Evaluation loop

Quantitative loop of `vault-skill-creator`, opt-in: test cases, runs with and without the skill, grading, benchmark, viewer, blind comparison, description optimization. The full form needs subagents; see "Environments" for Claude.ai, Cowork and headless sessions. Every JSON structure lives in `schemas.md`.

The loop is one continuous sequence: run it through, and add its steps to the todo list when one is available. Do not use `/skill-test` or any other testing skill.

## 1. Test cases

Write 2 or 3 realistic prompts, the kind a real user would type. Share them: "Here are a few test cases I'd like to try. Do these look right, or do you want to add more?" Save them to `evals/evals.json`, prompts only; the assertions come while the runs are in progress.

## 2. Workspace

Results go to `<skill-name>-workspace/`, sibling of the skill directory, organized by iteration (`iteration-1/`, `iteration-2/`) and, inside each iteration, one directory per test case named after the eval. Create directories as you go.

## 3. Spawn all runs in the same turn

For each test case, spawn two subagents in the same turn, one with the skill and one baseline, so that everything finishes around the same time.

With-skill run:

```
Execute this task:
- Skill path: <path-to-skill>
- Task: <eval prompt>
- Input files: <eval files if any, or "none">
- Save outputs to: <workspace>/iteration-<N>/<eval-name>/with_skill/outputs/
- Outputs to save: <what the user cares about, e.g. "the .docx file", "the final CSV">
```

Baseline run, same prompt:
- New skill: no skill path, outputs to `without_skill/outputs/`.
- Existing skill being improved: snapshot it before editing (`cp -r <skill-path> <workspace>/skill-snapshot/`), point the baseline at the snapshot, outputs to `old_skill/outputs/`.

Write an `eval_metadata.json` per test case, with a descriptive `eval_name` (not `eval-0`) that also names the directory, assertions empty for now. New or modified prompts get new files in the new iteration; nothing carries over.

## 4. Draft assertions while the runs are in progress

Draft objectively verifiable assertions with descriptive names, readable at a glance in the viewer, and explain them to the user. If `evals/evals.json` already has assertions, review them and explain what they check. Subjective qualities (writing style, design) stay in qualitative review. Update `eval_metadata.json` and `evals/evals.json`, then tell the user what the viewer will show, qualitative outputs and quantitative benchmark.

## 5. Capture timing as the runs complete

Each subagent completion notification carries `total_tokens` and `duration_ms`. Save them at once to `timing.json` in the run directory; they are persisted nowhere else. Process each notification as it arrives rather than batching.

## 6. Grade, aggregate, analyze, launch the viewer

1. Grade each run: spawn a grader subagent reading `agents/grader.md`, or grade inline, and save `grading.json` in each run directory with the exact field names of `schemas.md`. For assertions that can be checked programmatically, write and run a script; it is faster, more reliable and reusable across iterations.
2. Aggregate, from the `vault-skill-creator` directory:
   ```bash
   python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>
   ```
   This produces `benchmark.json` and `benchmark.md` (pass rate, time and tokens per configuration, mean and stddev, delta). Put each `with_skill` version before its baseline counterpart. A hand-written `benchmark.json` follows `schemas.md`.
3. Analyst pass: read the benchmark data with `agents/analyzer-benchmark.md` to surface what the aggregates hide: assertions that pass regardless of the skill, high-variance evals, time and token tradeoffs.
4. Launch the viewer with `generate_review.py`, never with hand-written HTML:
   ```bash
   nohup python <vault-skill-creator-path>/eval-viewer/generate_review.py \
     <workspace>/iteration-N \
     --skill-name "my-skill" \
     --benchmark <workspace>/iteration-N/benchmark.json \
     > /dev/null 2>&1 &
   VIEWER_PID=$!
   ```
   From iteration 2, add `--previous-workspace <workspace>/iteration-<N-1>`. Without a display or `webbrowser.open()`, use `--static <output_path>` to write a standalone HTML file; "Submit All Reviews" then downloads `feedback.json`, to copy into the workspace for the next iteration.
5. Tell the user: the results are open in the browser; the "Outputs" tab walks through each test case with a feedback box, the "Benchmark" tab shows the quantitative comparison; come back when done.

Generate the viewer before evaluating the outputs yourself: the human review comes first.

What the user sees:
- "Outputs" shows one test case at a time: the prompt, the output rendered inline where possible, a feedback box that auto-saves. From iteration 2, the previous output and the previous feedback appear collapsed; when graded, the formal grades appear collapsed too.
- "Benchmark" shows pass rates, timing and tokens per configuration, per-eval breakdowns and the analyst notes.
- Navigation by prev/next buttons or arrow keys; "Submit All Reviews" writes `feedback.json`.

## 7. Read the feedback

When the user is done, read `feedback.json`. Empty feedback means the output was fine; focus the improvements on the cases with specific complaints. Then stop the server: `kill $VIEWER_PID 2>/dev/null`.

## 8. Iterate

1. Apply the improvements (SKILL.md, "Improving the skill").
2. Rerun all test cases into `iteration-<N+1>/`, baselines included. For a new skill the baseline stays `without_skill`; for an existing skill, choose between the version the user came in with and the previous iteration.
3. Launch the viewer with `--previous-workspace` pointing at the previous iteration.
4. Wait for the user's review, read the feedback, improve again.

Stop when the user is happy, the feedback is all empty, or progress stalls.

## 9. Blind comparison

For "is the new version actually better?": give two outputs to an independent agent without telling it which is which (`agents/comparator.md`), then analyze why the winner won (`agents/analyzer.md`). Requires subagents; the human review loop is usually enough.

## 10. Description optimization

Requires the `claude -p` CLI and consumes API budget. Offer it only for a much-reused transverse skill or on reported triggering problems, once the skill is finished and the user agrees it is in good shape.

How triggering works: skills appear in `available_skills` by name and description, and Claude consults a skill only for tasks it cannot handle directly. A one-step query ("read this PDF") rarely triggers a skill whatever the description; a multi-step or specialized query does when the description matches. Eval queries have to be substantive enough for the skill to matter.

1. Write 20 queries, 8 to 10 should-trigger and 8 to 10 should-not-trigger, in the trigger eval set format of `schemas.md`. Realistic, concrete and detailed: file paths, job context, column names, company names, URLs, some backstory; mixed lengths, some lowercase, typos or casual speech; edge cases rather than clear-cut ones, the user signs off on them. Should-trigger: varied phrasings, formal and casual, cases that name neither the skill nor the file type, uncommon uses, cases where the skill competes with another and should win. Should-not-trigger: near misses that share keywords or concepts but need something else, adjacent domains, contexts where another tool fits better. An obviously irrelevant negative tests nothing.
   Bad: "Format this data". Good: "ok so my boss just sent me this xlsx file (its in my downloads, called something like 'Q4 sales final FINAL v2.xlsx') and she wants me to add a column that shows the profit margin as a percentage. The revenue is in column C and costs are in column D i think".
2. Review with the user through `assets/eval_review.html`: replace `__EVAL_DATA_PLACEHOLDER__` with the JSON array (unquoted, it is a JS assignment), `__SKILL_NAME_PLACEHOLDER__` and `__SKILL_DESCRIPTION_PLACEHOLDER__`; write to `/tmp/eval_review_<skill-name>.html` and open it. The user edits queries, toggles should-trigger, adds or removes entries, then clicks "Export Eval Set"; the file lands in `~/Downloads/eval_set.json` (take the most recent if several, such as `eval_set (1).json`). Bad queries give bad descriptions.
3. Save the eval set to the workspace, tell the user it takes time, and run in the background:
   ```bash
   python -m scripts.run_loop \
     --eval-set <path-to-trigger-eval.json> \
     --skill-path <path-to-skill> \
     --model <model-id-powering-this-session> \
     --max-iterations 5 \
     --verbose
   ```
   Use the model id of the current session (from the system prompt) so the test matches what the user experiences. Tail the output periodically to report the iteration and the scores. The script splits the set 60% train and 40% held-out test, then evaluates the current description, each query 3 times for a stable trigger rate. It asks Claude with extended thinking for an improved description from the failures and re-evaluates it on train and test, up to 5 iterations. It ends by opening an HTML report and returning JSON with `best_description`, selected on the test score to avoid overfitting.
4. Put `best_description` in the SKILL.md frontmatter, show before and after, report the scores. Check the result against the description template of SKILL.md.

## Environments

- Claude.ai: no subagents. Run each test case yourself, one at a time, by reading the skill and following it; skip the baselines and the benchmark. Present each prompt and output in the conversation, saving files to disk and giving the path when the user has to inspect them, and ask for feedback inline. No browser viewer, no `claude -p` (so no description optimization), no blind comparison. Packaging works.
- Cowork: subagents available; run in series on severe timeouts. No display: `--static <output_path>`, then give the user a link to open the HTML; `feedback.json` is downloaded, read it from there (access may have to be requested). Generate the viewer before revising the skill yourself. Packaging works; description optimization works (`claude -p` via subprocess), after the skill is finished.
- Remote or headless Claude Code: same as Cowork for the viewer.
