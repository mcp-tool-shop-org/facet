# E08 Task 3 — stroke 1 HALTED: the LoRA is gone from cloud, and the recipe is not the problem

**Executor session, 2026-08-04.** Amendment 30's discipline ran as specified through submission.
The job was **rejected by the cloud at validation** — before execution, so **0 credits and 0 GPU
time were consumed.** Strokes 2–8 not attempted. The halt needs a browser and a credential, both
of which this session does not do.

```
prompt_id   5d820ce8-6ac9-49fa-bb00-d50ce5e9312e
job_status  error / prompt_outputs_failed_validation
node 5      LoraLoaderModelOnly
detail      lora_name 'mikeyfrilot__saltroad-lora__saltroad_style_v2_lowlr_000001500.safetensors'
            not in (list of length 144)
```

---

## 1. The name is right. It is byte-identical to the one that worked.

Before proposing any cause, the obvious hypothesis — *the executor guessed the LoRA name* — was
checked against the artifact that proves otherwise. [E08-anchor-workflow-api.json](E08-anchor-workflow-api.json),
the 0b anchor's recipe, which **ran successfully on this cloud at ΔE 0.84**, carries:

```json
"lora_name": "mikeyfrilot__saltroad-lora__saltroad_style_v2_lowlr_000001500.safetensors"
```

**Byte-identical to what stroke 1 submitted.** So the string is not a prediction and not a typo —
it is the name that already worked. **The recipe did not change; the resource did.**

## 2. Measured, not inferred: it is absent from every list the session can read

| probe | result |
|---|---|
| `search_models q:"saltroad"` | **0 results** |
| `search_models type:lora q:"mikeyfrilot"` | **0 results** |
| `get_node LoraLoaderModelOnly` full uncapped option list | no `saltroad`, no `mikeyfrilot__*` entry anywhere |
| the cloud worker's own list, from the error | length **144**, name absent |

Two different list lengths are worth recording: the node catalog's option list is several hundred
entries, the worker reported **144**. They are different objects — the catalog is the bundled
public index, the 144 is what that worker could actually load. The name is in neither, so the
discrepancy does not rescue it.

## 3. The dry_run warning was accurate, and the record read it as benign

`submit_workflow --dry_run` returned `status: "validated"` with one warning: *"lora_name … was
not found in the bundled node index."* [E08-cloud-migration-state.md](E08-cloud-migration-state.md)
read that class of warning as *"expected for an un-imported model and is the browser-combo
staleness `comfy-cloud-run.md` gotcha #3 documents as running fine headless."*

**That reading was true for the 0b anchor and is false now.** Same warning, same name; one ran,
one was rejected. So the warning is not diagnostic on its own — it fires both when the model is
present-but-unindexed and when it is genuinely absent, and **the pre-flight cannot distinguish
them.** My step-3 pre-flight reported `validated` with *"only the expected imported-LoRA index
warning"* and treated it as cleared. It was not cleared; it was unresolvable at that stage, and I
should have said so rather than inheriting the record's reading of it.

**A dry_run PASS is a strong signal about the graph and says nothing about a private imported
model's availability.** That is the standing lesson, and the tool's own description says as much
— *"local validation uses a bundled node catalog that can lag the cloud"* — which I quoted as
reassurance when it is in fact the caveat that bit.

## 4. Why this is not mine to fix

[E08-cloud-migration-state.md](E08-cloud-migration-state.md) §0a-remaining already enumerated
exactly these three items as out of an executor's scope, and every one of them is what the fix
requires:

1. **An HF *read* token for `mikeyfrilot` in Comfy Cloud → Settings → Secrets.** The recorded
   existing secret is for `SaintEloi`, which cannot read a private `mikeyfrilot` repo. Entering a
   token is a credential action.
2. **Model Library → Import → the HF blob URL → type LoRA.** Browser-only: `upload_file`'s schema
   is `.jpg/.jpeg/.png/.webp/.gif` and the official API has no import endpoint.
3. **Read the real `lora_name` off the imported card.** Which is now doubly required — the
   previously-recorded name is the one being rejected.

Most likely causes, none of which I can distinguish from here and none of which change what the
next action is: the imported model was removed or expired from the Library; the HF read secret
was rotated or expired so a lazy fetch of the private repo now fails; or import visibility is
per-workspace and this session's worker is not the one 0b ran on. **Distinguishing them needs the
Model Library page, which is the same browser action as fixing it.**

## 5. Everything else is intact and costs nothing to resume

The halt is at exactly one step, and no work before it is wasted:

```
stage1_8cam.png / .glb                    Branch A banked, packed, untouched
state/atlas.png, holes.png, styled_mask.npy    seeded from the 8-camera atlas
state/job_y+090_e+00/                     emitted: 90,553 figure px, 19,065 hole px,
                                          12,248 withheld by --thin-extent 0.03
out/stroke_1_y+090_e+00_workflow.json     THE RECIPE, saved before submission per Amendment 30
out/run_log.jsonl                         3 ordered entries: emit, upload, submit(FAILED)
cloud inputs (uploaded, still valid names)
  render  d4a5486146580ae26f8ba7eba86d727f8fdcdecefa55b210e12ec45912ce0ae1.png
  mask    05f31fa8f9f944c63d2cad03059725533dae9fc502ce5944ffdedb369d03c90d.png
```

**Resuming is one call**: re-submit `stroke_1_y+090_e+00_workflow.json` with node 5's `lora_name`
corrected to whatever the Library card actually says. The uploaded inputs do not need re-uploading
and `emit` does not need re-running. Amendment 30's claim that the saved JSON *is* the recipe is
what makes that true — the transport failed and the recipe survived it, which is the first
practical demonstration of that ruling.

**Recorded on the way past:** both uploads returned cloud names that differ from the local file
SHA-256 (`111232f5…` → `d4a54861…`, `f37b0d5b…` → `05f31fa8…`), confirming again the
migration doc's gotcha-8 flag that the cloud content-addresses something other than the file
bytes, or re-encodes. Not chased — Task 3 claims no cross-boundary comparison, and the
first-stroke invariance check is designed to read exactly this as a uniform codec residual.

**The corner-median licence is still untested**, because no stroke output exists to test it
against. It remains an open anchor, not a passed one.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | The recipe was written to disk before submission and survived the failure intact; every parameter byte-matched to `texpass_brush.py`'s defaults; inputs, hashes, cloud names, job id and the failure all in an ordered run log. Amendment 30's relocation of the pin is what makes resumption a one-call operation |
| ANDON_AUTHORITY | **3** | The cloud's validator halted the run and the session halted with it — no retry with a guessed name, no substituted LoRA, no fallback to local execution. A guessed model name is exactly the class of improvisation this repo forbids |
| NAMED_COMPENSATORS | **3** | Nothing to undo: rejected before execution, 0 credits, 0 GPU time. Uploaded inputs are content-addressed and harmless; every local write is a new path |
| DECOMPOSE_BY_SECRETS | **2** | The failure is cleanly located in one node of one graph; `emit`/`commit`, the atlas and the prompt file are all unaffected and need no rework |
| UNCERTAINTY_GATED_HUMANS | **3** | Three candidate causes named, none chosen, with the note that distinguishing them is the same browser action as fixing it — so the choice is not worth a round-trip |
| EXTERNAL_VERIFIER | **2** | The cloud's own validator is a genuine external check and it caught what my pre-flight passed. The 0b anchor file served as an independent check on my own name, ruling out the likeliest self-inflicted cause before any cause was proposed |

---

**HALTED at stroke 1 of 8.** The graph is portable, the recipe is saved and correct, the inputs
are uploaded, the arm is bounded at 26.3%, and the one missing thing is a private LoRA that a
browser session has to restore. 0 credits spent. No local generation. No guessed names.
