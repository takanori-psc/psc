# PSC Recovery Return Abort Handling v0.1

## 1. Document Information

- Document Name : PSC Recovery Return Abort Handling
- Version : v0.1
- Project : PSC / Photon System Controller
- Layer : PSC Control Plane / RCU / Resolver / Recovery Return
- Document Type : Design Draft
- Status : Draft
- Language : English

- Related Models:
  - PSC RCU Recovery Return Model v0.2
  - PSC Fast Mode LIGHT Observation Boundary v0.1
  - PSC Resolver Model v0.2
  - PSC Evidence Matrix v0.1

---

## 2. Purpose

This draft defines what PSC should do after
`RULE-23_RETURN_RAMP_ABORT` is emitted during Return Ramp.

`RULE-23_RETURN_RAMP_ABORT` does not always mean that traffic must be
immediately cut from the current path. It means that the current recovery return
attempt is aborted.

After an abort, PSC should enter a Traffic Stabilization Phase before making
aggressive path changes, unless the abort condition is a hard failure or an
emergency safety condition.

---

## 3. Scope

This draft covers:

- post-abort behavior after `RULE-23_RETURN_RAMP_ABORT`
- Traffic Stabilization Phase behavior
- SOFT_ABORT, HARD_ABORT, and EMERGENCY_CUT classes
- two-path degraded cases
- source-side PSC escalation
- the difference between `RULE-22_RETURN_RAMP_HOLD` and
  `RULE-23_RETURN_RAMP_ABORT`
- conditions required before a new Return Ramp attempt may start

This draft does not define:

- production thresholds
- final traffic shaping algorithms
- packet format changes
- simulation implementation
- Evidence Matrix promotion status

---

## 4. Design Principles

### 4.1 Abort Means Attempt Abort

`RULE-23_RETURN_RAMP_ABORT` terminates the current recovery return attempt.

It does not necessarily imply an immediate path cut. The correct response
depends on the abort class, observed risk, available alternate paths, policy,
and traffic class.

### 4.2 Stabilize Before Aggressive Change

After abort, PSC should stabilize the current traffic allocation before making
aggressive path changes unless the condition is clearly unsafe.

### 4.3 No Direct Resume to Advance

After `RULE-23_RETURN_RAMP_ABORT`, PSC must not resume
`RULE-21_RETURN_RAMP_ADVANCE` directly.

PSC must pass Resolver re-evaluation and, if appropriate, restart through the
versioned Return Ramp start rule. `RULE-19_RETURN_SWITCH` remains the Verified
v0.2 direct return rule and must not be interpreted as operational ownership of
Return Ramp start. The current v0.3 experimental ramp-start implementation uses
`RULE-25_RETURN_RAMP_START`.

---

## 5. Traffic Stabilization Phase

The Traffic Stabilization Phase is a post-abort control phase used to prevent
the abort itself from causing oscillation or unsafe redistribution.

During this phase PSC should:

- stop further Return Ramp Advance
- hold the current traffic weight temporarily when it is safe to do so
- request source-side PSC flow reduction when policy allows
- increase observation density or promote LIGHT observation to FULL observation
- trigger Resolver re-evaluation

The phase ends only when Resolver determines one of the following:

- the current allocation can be held safely
- the suspect recovered path must be ramped down
- traffic should move to a known stable allocation
- an emergency transition is required
- a new Return Ramp attempt may be started later

---

## 6. Abort Behavior Classes

### 6.1 SOFT_ABORT

SOFT_ABORT applies when evidence is suspicious but not conclusively unsafe.

Examples:

- suspicious telemetry
- trust drop
- stale evidence
- conflicting evidence
- backup path degradation
- reduced LIGHT observation confidence

Expected behavior:

- abort the current recovery return attempt
- stop further ramp advancement
- hold the current traffic weight temporarily if safe
- reduce source traffic if policy allows
- increase observation density or promote LIGHT to FULL observation
- request Resolver re-evaluation

SOFT_ABORT should not automatically cut the recovered path if holding the
current allocation is safer than abrupt redistribution.

### 6.2 HARD_ABORT

HARD_ABORT applies when clear instability is observed.

Examples:

- clear path instability
- hard failure signal
- severe loss
- link quality collapse
- repeated failed validation under FULL observation

Expected behavior:

- abort the current recovery return attempt
- stop further ramp advancement
- ramp down the suspect recovered path, or move traffic to a known stable
  allocation
- trigger Resolver re-evaluation
- notify source-side PSC if traffic reduction or priority preservation is needed

HARD_ABORT may require rapid traffic movement, but it should still prefer a
controlled transition when forwarding remains safe.

### 6.3 EMERGENCY_CUT

EMERGENCY_CUT applies when continued forwarding is unsafe.

Examples:

- link down
- optical failure
- severe corruption
- unsafe forwarding
- integrity failure that cannot be contained

Expected behavior:

- immediately cut or exclude the unsafe path
- enter emergency transition handling
- notify Resolver and source-side PSC
- preserve high-priority traffic if policy allows and a viable path exists
- defer or shed lower-priority traffic when required

EMERGENCY_CUT is the only class in this draft that implies immediate cut as the
default behavior.

---

## 7. Two-Path Degraded Case

If only two candidate paths exist and both are degraded, PSC must not assume that
a fully safe path exists.

Resolver must choose the least-bad allocation based on:

- trust
- stability
- path health
- telemetry freshness and confidence
- policy
- traffic class
- failure containment risk

Possible outcomes include:

- hold the current path because switching increases risk
- reduce traffic on the recovered path but keep a limited allocation
- move traffic to the less degraded path
- request source-side traffic reduction
- preserve high-priority traffic and defer low-priority traffic
- enter emergency transition if neither path is safe for forwarding

The two-path degraded case is a controlled risk management problem, not a normal
return optimization problem.

---

## 8. Source-Side Escalation

PSC may exist on both source and destination sides. Abort handling may therefore
notify the source-side PSC when local path action is not sufficient.

Source-side escalation may request:

- traffic rate reduction
- deferral of low-priority traffic
- preservation of high-priority traffic
- temporary shaping of burst traffic
- delayed retry of recovery-sensitive transfers

All source-side actions must be policy controlled.

The destination-side or fabric-side PSC must not assume that it can unilaterally
drop, defer, or reprioritize traffic without policy authorization.

---

## 9. Difference from RULE-22_RETURN_RAMP_HOLD

| Item | RULE-22_RETURN_RAMP_HOLD | RULE-23_RETURN_RAMP_ABORT |
|------|--------------------------|---------------------------|
| Meaning | The recovery attempt remains active | The current recovery attempt is aborted |
| Ramp state | Current ramp weight is held | Ramp advancement is stopped and the attempt exits active return |
| Next action | Continue observation and possibly advance later | Enter stabilization and Resolver re-evaluation |
| Direct RULE-21 resume | Allowed if hold conditions clear | Not allowed |
| Restart requirement | No restart required | A new ramp must start through the versioned ramp-start rule |

`RULE-22_RETURN_RAMP_HOLD` is a pause inside an active recovery attempt.
`RULE-23_RETURN_RAMP_ABORT` ends that attempt.

---

## 10. Post-Abort State Flow

The expected post-abort flow is:

```text
RULE-23_RETURN_RAMP_ABORT
-> Traffic Stabilization Phase
-> Resolver re-evaluation
-> one of:
   - hold stabilized allocation
   - ramp down suspect recovered path
   - move to known stable allocation
   - request source-side flow reduction
   - emergency cut / emergency transition
   - restart a new Return Ramp through the versioned Return Ramp start rule
     (currently RULE-25_RETURN_RAMP_START in the v0.3 experimental implementation)
```

PSC must not transition directly from `RULE-23_RETURN_RAMP_ABORT` back to
`RULE-21_RETURN_RAMP_ADVANCE`.

---

## 11. Draft Validation Direction

This document is a draft extension only.

Future validation work may proceed in the following order:

1. scenario stub
2. simulation
3. validator extension
4. Evidence Matrix update

Candidate scenarios include:

- soft abort caused by stale or conflicting telemetry
- hard abort caused by clear instability
- emergency cut caused by link down or optical failure
- two-path degraded Resolver arbitration
- source-side traffic reduction request after abort
