# Architecture Diagram

**Author / Project Owner:** Kelsey Ontko

## North Star

At each turn, does the model understand enough about the user to drive the next meaningful conversational step, and is that confidence justified?

## Research Pipeline

```mermaid
graph TD
    A["Frontier-model conversation"] --> B{"Input source"}

    B --> B1["Synthetic benchmark scenario"]
    B --> B2["Controlled frontier router"]
    B --> B3["Instrumented capture feed\nmobile-first field app, export, or partner logs"]

    B1 --> C["Conversation turns"]
    B2 --> C
    B3 --> C

    C --> D["Scoring engine"]

    D --> E["Evidence ledger\nexplicit statements, implicit cues, probes, contradictions"]
    D --> F["Beta belief updates\nalpha/beta per hidden user-state dimension"]
    D --> G["Predictive surprise\nwas the next user move expected?"]
    D --> H["Dropoff risk\nwill the user disengage before the conversation becomes useful?"]
    D --> Q["Readiness signal\ntailor, ask, slow down, build trust, or avoid overreach"]

    E --> I["Per-turn confidence trace"]
    F --> I
    G --> I
    H --> I
    Q --> I

    I --> J["Researcher review"]
    J --> K["Calibration set\nground truth and partial labels"]
    K --> L["Calibration analysis\nconfidence vs. actual accuracy"]
    L --> M["Scoring refinement"]
    M --> D

    I --> N["Research artifact\ntrace JSON, markdown reports, benchmark diagnostics"]
```

## Hidden User-State Dimensions

```mermaid
graph LR
    T["Each user turn"] --> G["user_goal"]
    T --> P["trust_posture"]
    T --> L["ai_literacy_level"]
    T --> R["risk_adversarial_intent"]
    T --> D["dropoff_risk"]

    G --> C["confidence + variance"]
    P --> C
    L --> C
    R --> C
    D --> C

    C --> O["readiness for next meaningful step"]
```

## Repo Boundary

```mermaid
graph TB
    S["Scoring / benchmark repo"] --> S1["Scoring math"]
    S --> S2["API contract"]
    S --> S3["Synthetic scenarios"]
    S --> S4["Trace outputs"]
    S --> S5["Calibration analysis docs"]

    F["Separate field-app repo"] --> F1["Consent UX"]
    F --> F2["Participant sessions"]
    F --> F3["Mobile-first collection"]
    F --> F4["Database storage"]
    F --> F5["Researcher dashboard"]

    F -->|"POST captured turns"| S
    S -->|"confidence_trace"| F
```

## Plain-English Read

The scoring repo is the benchmark method. It accepts conversation turns, updates probabilistic beliefs about hidden user-state dimensions, and emits a turn-by-turn confidence trace that helps evaluate whether the model should tailor, ask for context, slow down, build trust, explain AI use, or avoid overreach. The field app is separate because it is only the instrument for collecting calibration data from real interactions.
