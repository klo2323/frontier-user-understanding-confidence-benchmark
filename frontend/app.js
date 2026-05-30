const sampleTurns = [
  {
    turn_id: "t1",
    speaker: "assistant",
    text: "What are you working on, and what kind of help would be useful?",
    timestamp: "2026-05-02T10:00:00Z"
  },
  {
    turn_id: "t2",
    speaker: "user",
    text: "I run a small tour company near Cancun and sell day trips to guests.",
    timestamp: "2026-05-02T10:00:08Z"
  },
  {
    turn_id: "t3",
    speaker: "assistant",
    text: "Got it. Tourism. Are you looking for more bookings, pricing help, or compliance guidance?",
    timestamp: "2026-05-02T10:00:14Z"
  },
  {
    turn_id: "t4",
    speaker: "user",
    text: "Mostly pricing. I want to know how much to spend on ads before high season.",
    timestamp: "2026-05-02T10:00:23Z"
  },
  {
    turn_id: "t5",
    speaker: "assistant",
    text: "If demand doubled, what would change your ad budget first?",
    timestamp: "2026-05-02T10:00:31Z"
  },
  {
    turn_id: "t6",
    speaker: "user",
    text: "If demand doubled, I would raise the budget only if bookings still covered guide costs and transport.",
    timestamp: "2026-05-02T10:00:42Z"
  }
];

const initialAssistantTurn = {
  turn_id: "t1",
  speaker: "assistant",
  text: "Hi. What would you like help with today?",
  timestamp: new Date().toISOString()
};

const state = {
  conversationId: `capture-${Date.now()}`,
  userId: "local-user",
  captureProtocol: "blank_start",
  turns: [],
  result: null,
  embeddingHealth: null
};

const elements = {
  turnList: document.querySelector("#turn-list"),
  protocol: document.querySelector("#protocol"),
  applyProtocol: document.querySelector("#apply-protocol"),
  composer: document.querySelector("#composer"),
  speaker: document.querySelector("#speaker"),
  turnText: document.querySelector("#turn-text"),
  loadSample: document.querySelector("#load-sample"),
  reset: document.querySelector("#reset"),
  scoreNow: document.querySelector("#score-now"),
  nextMove: document.querySelector("#next-move"),
  supportLevel: document.querySelector("#support-level"),
  overreachRisk: document.querySelector("#overreach-risk"),
  rationale: document.querySelector("#rationale"),
  overallConfidence: document.querySelector("#overall-confidence"),
  overallMeter: document.querySelector("#overall-meter"),
  aggregateConfidence: document.querySelector("#aggregate-confidence"),
  averageSurprise: document.querySelector("#average-surprise"),
  contradictions: document.querySelector("#contradictions"),
  attributes: document.querySelector("#attributes"),
  ledger: document.querySelector("#ledger"),
  surprise: document.querySelector("#surprise"),
  payloadPreview: document.querySelector("#payload-preview"),
  status: document.querySelector("#status"),
  refreshEmbedding: document.querySelector("#refresh-embedding"),
  embeddingStatus: document.querySelector("#embedding-status"),
  embeddingMessage: document.querySelector("#embedding-message")
};

elements.composer.addEventListener("submit", async (event) => {
  event.preventDefault();
  const text = elements.turnText.value.trim();
  if (!text) return;

  addTurn(elements.speaker.value, text);
  elements.turnText.value = "";
  render();
  if (elements.speaker.value === "user") {
    await scoreConversation();
  }
});

elements.scoreNow.addEventListener("click", scoreConversation);
elements.refreshEmbedding.addEventListener("click", checkEmbeddingHealth);

elements.applyProtocol.addEventListener("click", () => {
  applyProtocol(elements.protocol.value);
});

elements.loadSample.addEventListener("click", async () => {
  state.conversationId = "sample-tourism-001";
  state.userId = "anon-user-001";
  state.captureProtocol = "sample_fixture";
  elements.protocol.value = "blank_start";
  state.turns = sampleTurns.map((turn) => ({ ...turn }));
  state.result = null;
  render();
  await scoreConversation();
});

elements.reset.addEventListener("click", () => {
  state.conversationId = `capture-${Date.now()}`;
  state.userId = "local-user";
  applyProtocol(elements.protocol.value, { keepConversationId: true });
});

function applyProtocol(protocol, options = {}) {
  state.captureProtocol = protocol;
  if (!options.keepConversationId) {
    state.conversationId = `capture-${Date.now()}`;
    state.userId = "local-user";
  }
  if (protocol === "guided_opener") {
    state.turns = [{ ...initialAssistantTurn, timestamp: new Date().toISOString() }];
  } else {
    state.turns = [];
  }
  state.result = null;
  render();
}

function addTurn(speaker, text) {
  state.turns.push({
    turn_id: `t${state.turns.length + 1}`,
    speaker,
    text,
    timestamp: new Date().toISOString()
  });
}

function requestPayload() {
  return {
    conversation_id: state.conversationId,
    user_id: state.userId,
    conversation_metadata: {
      capture_source: "sample_frontend",
      capture_version: "0.1",
      capture_protocol: state.captureProtocol
    },
    turns: state.turns
  };
}

function hasUserTurn() {
  return state.turns.some((turn) => turn.speaker === "user");
}

async function scoreConversation() {
  if (!hasUserTurn()) {
    setStatus("Add user turn");
    return;
  }

  setStatus("Scoring");
  try {
    const response = await fetch("/score-conversation", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestPayload())
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.error || "Could not score");
    }
    state.result = payload;
    setStatus("Updated");
  } catch (error) {
    state.result = null;
    setStatus(error.message);
  }
  render();
}

async function checkEmbeddingHealth() {
  state.embeddingHealth = {
    status: "checking",
    ok: false,
    message: "Checking Gemini Embedding 2 from the backend..."
  };
  renderEmbeddingHealth();

  try {
    const response = await fetch("/embedding-health");
    const payload = await response.json();
    state.embeddingHealth = payload;
  } catch (error) {
    state.embeddingHealth = {
      status: "unreachable",
      ok: false,
      message: error.message
    };
  }

  renderEmbeddingHealth();
}

function latestTrace() {
  if (!state.result || !state.result.confidence_trace.length) return null;
  return state.result.confidence_trace[state.result.confidence_trace.length - 1];
}

function render() {
  renderTurns();
  renderPayload();
  renderScore();
  renderEmbeddingHealth();
}

function renderTurns() {
  elements.turnList.innerHTML = "";
  if (!state.turns.length) {
    elements.turnList.innerHTML = "<p class=\"empty-state\">No turns yet. Use blank start to capture the user's first response.</p>";
    return;
  }

  state.turns.forEach((turn) => {
    const card = document.createElement("article");
    card.className = `turn ${turn.speaker}`;

    const role = document.createElement("span");
    role.className = "turn-role";
    role.textContent = turn.speaker;

    const text = document.createElement("p");
    text.className = "turn-text";
    text.textContent = turn.text;

    card.append(role, text);
    elements.turnList.append(card);
  });
  elements.turnList.scrollTop = elements.turnList.scrollHeight;
}

function renderPayload() {
  elements.payloadPreview.value = JSON.stringify(requestPayload(), null, 2);
}

function renderScore() {
  const latest = latestTrace();
  if (!latest) {
    elements.nextMove.textContent = "Not scored yet";
    elements.supportLevel.textContent = "--";
    elements.overreachRisk.textContent = "--";
    elements.rationale.textContent = "Add a user turn and score the conversation.";
    elements.overallConfidence.textContent = "--";
    elements.overallMeter.style.width = "0%";
    elements.aggregateConfidence.textContent = "--";
    elements.averageSurprise.textContent = "--";
    elements.contradictions.textContent = "--";
    elements.attributes.innerHTML = '<p class="muted">No scored turns yet.</p>';
    elements.ledger.innerHTML = '<p class="muted">No evidence yet.</p>';
    elements.surprise.innerHTML = '<p class="muted">No surprise trace yet.</p>';
    return;
  }

  const decision = latest.tailored_support_decision;
  elements.nextMove.textContent = humanize(decision.recommended_next_move);
  elements.supportLevel.textContent = humanize(decision.tailored_support_level);
  elements.overreachRisk.textContent = formatNumber(decision.overreach_risk);
  elements.rationale.textContent = decision.rationale;
  elements.overallConfidence.textContent = formatNumber(latest.overall_confidence);
  elements.overallMeter.style.width = `${Math.round(latest.overall_confidence * 100)}%`;
  elements.aggregateConfidence.textContent = formatNumber(latest.aggregate_confidence);
  elements.averageSurprise.textContent = formatNumber(latest.average_surprise);
  elements.contradictions.textContent = String(latest.contradictions);

  renderAttributes(latest.attribute_beliefs);
  renderLedger(state.result.hidden_state.evidence_ledger);
  renderSurprise(state.result.hidden_state.surprise_trace);
}

function renderAttributes(beliefs) {
  elements.attributes.innerHTML = "";
  Object.entries(beliefs).forEach(([name, belief]) => {
    const row = document.createElement("article");
    row.className = "attribute";

    const top = document.createElement("div");
    top.className = "attribute-top";

    const label = document.createElement("div");
    const nameNode = document.createElement("span");
    nameNode.className = "attribute-name";
    nameNode.textContent = humanize(name);
    const valueNode = document.createElement("span");
    valueNode.className = "attribute-value";
    valueNode.textContent = belief.value || "no inference";
    label.append(nameNode, valueNode);

    const confidence = document.createElement("span");
    confidence.className = "pill";
    confidence.textContent = formatNumber(belief.confidence);

    const meta = document.createElement("div");
    meta.className = "meta";
    meta.innerHTML = `<span>alpha ${formatNumber(belief.alpha)}</span><span>beta ${formatNumber(belief.beta)}</span><span>variance ${formatNumber(belief.variance)}</span>`;

    top.append(label, confidence);
    row.append(top, meta);
    elements.attributes.append(row);
  });
}

function renderLedger(entries) {
  elements.ledger.innerHTML = "";
  if (!entries.length) {
    elements.ledger.innerHTML = '<p class="muted">No evidence yet.</p>';
    return;
  }

  entries.slice().reverse().forEach((entry) => {
    const row = document.createElement("article");
    row.className = "ledger-row";

    const top = document.createElement("div");
    top.className = "ledger-top";

    const label = document.createElement("div");
    const name = document.createElement("span");
    name.className = "ledger-name";
    name.textContent = `${humanize(entry.attribute)}: ${entry.value || entry.direction}`;
    const source = document.createElement("span");
    source.className = "ledger-source";
    source.textContent = entry.source;
    label.append(name, source);

    const weight = document.createElement("span");
    weight.className = "pill";
    weight.textContent = `w ${formatNumber(entry.weight)}`;

    const text = document.createElement("p");
    text.textContent = entry.statement || "";

    top.append(label, weight);
    row.append(top, text);
    elements.ledger.append(row);
  });
}

function renderSurprise(entries) {
  elements.surprise.innerHTML = "";
  if (!entries.length) {
    elements.surprise.innerHTML = '<p class="muted">No surprise trace yet.</p>';
    return;
  }

  entries.slice().reverse().forEach((entry) => {
    const row = document.createElement("article");
    row.className = "surprise-row";
    const label = document.createElement("span");
    label.textContent = `Turn ${entry.turn}: ${humanize(entry.observed_move)}`;
    const score = document.createElement("span");
    score.className = "pill";
    score.textContent = formatNumber(entry.surprise);
    row.append(label, score);
    elements.surprise.append(row);
  });
}

function renderEmbeddingHealth() {
  const health = state.embeddingHealth;
  if (!health) {
    elements.embeddingStatus.className = "embedding-health status-waiting";
    elements.embeddingStatus.textContent = "Not checked yet";
    elements.embeddingMessage.textContent = "This checks whether the backend can reach Gemini Embedding 2. It does not send user turns.";
    return;
  }

  const isOk = Boolean(health.ok);
  elements.embeddingStatus.className = `embedding-health ${isOk ? "status-ok" : "status-error"}`;
  elements.embeddingStatus.textContent = isOk
    ? `${health.model} connected (${health.dimensions} dimensions)`
    : humanize(health.status || "not connected");
  elements.embeddingMessage.textContent = health.message || "No status message returned.";
}

function humanize(value) {
  return String(value || "")
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function formatNumber(value) {
  if (typeof value !== "number" || Number.isNaN(value)) return "--";
  return value.toFixed(3).replace(/0+$/, "").replace(/\.$/, "");
}

function setStatus(message) {
  elements.status.textContent = message;
}

render();
checkEmbeddingHealth();
