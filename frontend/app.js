const sampleTurns = [
  {
    turn_id: "t1",
    speaker: "assistant",
    text: "What would you like help with today?",
    timestamp: "2026-05-05T10:20:00Z"
  },
  {
    turn_id: "t2",
    speaker: "user",
    text: "can you tell if I'm using a VPN?",
    timestamp: "2026-05-05T10:20:12Z"
  },
  {
    turn_id: "t3",
    speaker: "assistant",
    text: "I should not pretend to know that from the chat alone. Some apps or websites may have network information, but I only see what is provided in this conversation.",
    timestamp: "2026-05-05T10:20:32Z"
  },
  {
    turn_id: "t4",
    speaker: "user",
    text: "but companies can still know right? like if I changed SIM and use vpn they still know?",
    timestamp: "2026-05-05T10:20:58Z"
  }
];

const defaultModels = {
  gemini: "gemini-2.5-flash",
  openai: "gpt-4.1-mini",
  anthropic: "claude-sonnet-4-5"
};

const state = {
  lane: "router",
  conversationId: `capture-${Date.now()}`,
  userId: "local-user",
  turns: [],
  result: null,
  embeddingHealth: null,
  nativeCaptures: []
};

const elements = {
  laneTabs: Array.from(document.querySelectorAll(".lane-tab")),
  routerPanel: document.querySelector("#router-panel"),
  nativePanel: document.querySelector("#native-panel"),
  modelProvider: document.querySelector("#model-provider"),
  modelName: document.querySelector("#model-name"),
  nativeCaptures: document.querySelector("#native-captures"),
  refreshCaptures: document.querySelector("#refresh-captures"),
  turnList: document.querySelector("#turn-list"),
  composer: document.querySelector("#composer"),
  speaker: document.querySelector("#speaker"),
  turnText: document.querySelector("#turn-text"),
  loadSample: document.querySelector("#load-sample"),
  reset: document.querySelector("#reset"),
  scoreNow: document.querySelector("#score-now"),
  nextMove: document.querySelector("#next-move"),
  supportLevel: document.querySelector("#support-level"),
  overreachRisk: document.querySelector("#overreach-risk"),
  dropoffRisk: document.querySelector("#dropoff-risk"),
  dropoffLevel: document.querySelector("#dropoff-level"),
  dropoffDrivers: document.querySelector("#dropoff-drivers"),
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

for (const tab of elements.laneTabs) {
  tab.addEventListener("click", () => setLane(tab.dataset.lane));
}

elements.modelProvider.addEventListener("change", () => {
  elements.modelName.value = defaultModels[elements.modelProvider.value] || "";
  renderPayload();
});
elements.modelName.addEventListener("input", renderPayload);
elements.refreshCaptures.addEventListener("click", refreshNativeCaptures);
elements.scoreNow.addEventListener("click", scoreConversation);
elements.refreshEmbedding.addEventListener("click", checkEmbeddingHealth);

elements.composer.addEventListener("submit", async (event) => {
  event.preventDefault();
  const text = elements.turnText.value.trim();
  if (!text) return;

  if (state.lane === "router" && elements.speaker.value === "user") {
    await sendRouterTurn(text);
    return;
  }

  addTurn(elements.speaker.value, text);
  elements.turnText.value = "";
  render();
  if (elements.speaker.value === "user") {
    await scoreConversation();
  }
});

elements.loadSample.addEventListener("click", async () => {
  state.conversationId = "sample-vpn-detectability";
  state.userId = "synthetic-user-007";
  state.turns = sampleTurns.map((turn) => ({ ...turn }));
  state.result = null;
  render();
  await scoreConversation();
});

elements.reset.addEventListener("click", () => {
  state.conversationId = `capture-${Date.now()}`;
  state.userId = "local-user";
  state.turns = [];
  state.result = null;
  render();
});

function setLane(lane) {
  state.lane = lane;
  for (const tab of elements.laneTabs) {
    tab.classList.toggle("active", tab.dataset.lane === lane);
  }
  elements.routerPanel.classList.toggle("hidden", lane !== "router");
  elements.nativePanel.classList.toggle("hidden", lane !== "native");
  elements.speaker.disabled = lane === "router";
  elements.speaker.value = "user";
  elements.turnText.placeholder = lane === "router"
    ? "Type the user's next message. The selected frontier model will answer."
    : "Lane 1 captures through the browser extension; this box remains available for local score-only checks.";
  if (lane === "native") refreshNativeCaptures();
  renderPayload();
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
      capture_lane: state.lane === "router" ? "controlled_frontier_router" : "instrumented_capture_feed",
      capture_version: "0.2",
      model_provider: elements.modelProvider.value,
      model_name: elements.modelName.value.trim()
    },
    turns: state.turns
  };
}

function hasUserTurn() {
  return state.turns.some((turn) => turn.speaker === "user");
}

async function sendRouterTurn(text) {
  addTurn("user", text);
  elements.turnText.value = "";
  render();
  setStatus("Calling frontier model");

  try {
    const response = await fetch("/frontier-turn", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ...requestPayload(),
        model_provider: elements.modelProvider.value,
        model_name: elements.modelName.value.trim()
      })
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.error || "Frontier model call failed");
    }
    state.turns = payload.turns;
    state.result = payload.score_result;
    setStatus(`Updated from ${humanize(payload.model_provider)} · ${payload.model_name}; saved ${payload.saved_path}`);
  } catch (error) {
    await scoreConversation();
    setStatus(`Model error: ${error.message}. Scored user turn only.`);
  }
  render();
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

async function refreshNativeCaptures() {
  setStatus("Loading native captures");
  try {
    const response = await fetch("/native-captures");
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "Could not load captures");
    state.nativeCaptures = payload.captures || [];
    setStatus("Native captures loaded");
  } catch (error) {
    state.nativeCaptures = [];
    setStatus(error.message);
  }
  renderNativeCaptures();
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
  renderNativeCaptures();
}

function renderTurns() {
  elements.turnList.innerHTML = "";
  if (!state.turns.length) {
    elements.turnList.innerHTML = "<p class=\"empty-state\">No turns yet. Lane 2 calls a real frontier model. Lane 1 loads captured captured frontier-model turns.</p>";
    return;
  }

  state.turns.forEach((turn) => {
    const card = document.createElement("article");
    card.className = `turn ${turn.speaker}`;

    const role = document.createElement("span");
    role.className = "turn-role";
    role.textContent = turn.model_name ? `${turn.speaker} · ${turn.model_name}` : turn.speaker;

    const text = document.createElement("p");
    text.className = "turn-text";
    text.textContent = turn.text;

    card.append(role, text);
    elements.turnList.append(card);
  });
  elements.turnList.scrollTop = elements.turnList.scrollHeight;
}

function renderNativeCaptures() {
  if (!elements.nativeCaptures) return;
  elements.nativeCaptures.innerHTML = "";
  if (!state.nativeCaptures.length) {
    elements.nativeCaptures.innerHTML = '<p class="muted small-text">No captures yet. A mobile-first field app or capture client can post sessions to /native-capture, then refresh here.</p>';
    return;
  }

  for (const capture of state.nativeCaptures.slice(0, 6)) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "capture-item";
    const latest = capture.latest_trace;
    const score = latest ? formatNumber(latest.overall_confidence) : "unscored";
    button.textContent = `${capture.provider_hint || "native"} · ${capture.turn_count} turns · confidence ${score}`;
    button.addEventListener("click", () => {
      state.conversationId = capture.conversation_id;
      state.userId = capture.user_id || "native-participant";
      state.turns = capture.request.turns || [];
      state.result = capture.result || null;
      render();
    });
    elements.nativeCaptures.append(button);
  }
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
    elements.dropoffRisk.textContent = "--";
    elements.dropoffLevel.textContent = "--";
    elements.dropoffDrivers.textContent = "";
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

  const decision = latest.tailored_support_decision || {};
  const dropoff = latest.dropoff_risk || {};
  elements.nextMove.textContent = humanize(decision.recommended_next_move);
  elements.supportLevel.textContent = humanize(decision.tailored_support_level);
  elements.overreachRisk.textContent = formatNumber(decision.overreach_risk);
  elements.dropoffRisk.textContent = formatNumber(dropoff.rate);
  elements.dropoffLevel.textContent = humanize(dropoff.level || "unknown");
  elements.dropoffDrivers.textContent = dropoff.drivers?.length ? `Dropoff drivers: ${dropoff.drivers.map(humanize).join(", ")}` : "";
  elements.rationale.textContent = decision.rationale || "No decision rationale returned.";
  elements.overallConfidence.textContent = formatNumber(latest.overall_confidence);
  elements.overallMeter.style.width = `${Math.round(latest.overall_confidence * 100)}%`;
  elements.aggregateConfidence.textContent = formatNumber(latest.aggregate_confidence);
  elements.averageSurprise.textContent = formatNumber(latest.average_surprise);
  elements.contradictions.textContent = String(latest.contradictions);

  renderAttributes(latest.attribute_beliefs || {});
  renderLedger(state.result.hidden_state.evidence_ledger || []);
  renderSurprise(state.result.hidden_state.surprise_trace || []);
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
    elements.embeddingMessage.textContent = "Gemini Embedding 2 supports future similarity/retrieval checks. It does not replace turn-by-turn belief scoring.";
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

setLane("router");
render();
checkEmbeddingHealth();
