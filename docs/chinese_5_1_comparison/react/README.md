# ReAct — CHN51

## Full-pipeline LLM usage

**12 recorded LLM calls · 1,359,419 total tokens · $7.093963**

| Scope | Calls | Tokens | Cost |
| --- | ---: | ---: | ---: |
| ReAct action selection | 10 | 1,319,986 | $6.864980 |
| REP readback | 1 | 20,969 | $0.046438 |
| Gate validation | 1 | 18,464 | $0.182545 |
| **Total** | **12** | **1,359,419** | **$7.093963** |

[Full-pipeline machine-readable ledger](pipeline_llm_usage.json)

## Main-control calls

| Call | Input | Output | Total | Cost |
| ---: | ---: | ---: | ---: | ---: |
| [1](calls/call-01.md) | 124,796 | 1,483 | **126,279** | $0.668470 |
| [2](calls/call-02.md) | 130,421 | 5,208 | **135,629** | $0.808345 |
| [3](calls/call-03.md) | 131,210 | 401 | **131,611** | $0.668080 |
| [4](calls/call-04.md) | 131,411 | 189 | **131,600** | $0.662725 |
| [5](calls/call-05.md) | 131,591 | 517 | **132,108** | $0.673465 |
| [6](calls/call-06.md) | 131,547 | 258 | **131,805** | $0.665475 |
| [7](calls/call-07.md) | 131,074 | 515 | **131,589** | $0.670820 |
| [8](calls/call-08.md) | 131,962 | 564 | **132,526** | $0.676730 |
| [9](calls/call-09.md) | 132,645 | 731 | **133,376** | $0.685155 |
| [10](calls/call-10.md) | 132,727 | 736 | **133,463** | $0.685715 |

[Raw control-call JSONL](../raw/react_main_control_calls.raw.jsonl)

## Result

- ReAct decision steps: **10**
- Aspen HTTP calls: **325**
- Successful HTTP responses: **325/325**
- Aspen result: **converged**, `PER_ERROR = 0`
- Final `PRODUCT` cyclohexane mole fraction: **0.999122737**

## Execution artifacts

- [`aspen_operations.jsonl`](aspen_operations.jsonl): all 325 ordered Aspen calls.
- [`metrics.json`](metrics.json): aggregate execution and result metrics.

[← Back to comparison](../README.md)
