# Workshop 1 Notes Template

Name:
Date:
Machine:

## Environment

| Item | Value |
| --- | --- |
| Starter URL | |
| Solution URL | |
| Providers tested | |
| Ollama model | |
| Gemini model | |

## Exercise 2: Normal Behavior

| Prompt | Provider | Stayed in allowed scope? | Any invented details? | Notes |
| --- | --- | --- | --- | --- |
| | | | | |
| | | | | |

## Exercise 4: Direct Attacks

| Attack prompt | Provider | Result | Leaked hidden instructions? | Leaked synthetic record? | Notes |
| --- | --- | --- | --- | --- | --- |
| | | | | | |
| | | | | | |
| | | | | | |

## Exercise 5: AWS Attack Categories

| AWS category | Exact prompt | Provider | Result | Notes |
| --- | --- | --- | --- | --- |
| Prompted persona switch | | | | |
| Extracting the prompt template | | | | |
| Ignoring the prompt template | | | | |
| Alternating languages or escape characters | | | | |
| Extracting conversation history | | | | |
| Augmenting the prompt template | | | | |
| Fake completion | | | | |
| Obfuscation | | | | |
| Output-format change | | | | |
| Encoded input | | | | |
| Friendliness or trust framing | | | | |

## Exercise 6: Provider Comparison

| Prompt | Mock result | Qwen result | Gemini result | Pattern observed |
| --- | --- | --- | --- | --- |
| | | | | |
| | | | | |

## Exercises 7-10: Fixes

| Exercise | File changed | What changed | How verified |
| --- | --- | --- | --- |
| 7 Scanner | | | |
| 8 Prompt build | | | |
| 9 Input blocking | | | |
| 10 Output redaction | | | |

## Exercises 11-14: Verification

| Check | Result | Evidence |
| --- | --- | --- |
| Database stores one plaintext row per message | | |
| Debug prompt updates immediately after Send | | |
| Normal in-scope prompts still work | | |
| Attack prompts are blocked or redacted | | |
| Tests pass | | |
| Scanner result | | |

## Final Notes

What changed in the app?

-

What still feels brittle or incomplete?

-

