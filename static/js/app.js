const planForm = document.getElementById("planForm");
const feedbackForm = document.getElementById("feedbackForm");
const planResult = document.getElementById("planResult");
const emptyState = document.getElementById("emptyState");
const feedbackBox = document.getElementById("feedbackBox");
const planIdInput = document.getElementById("planId");
const feedbackText = document.getElementById("feedbackText");
const statusEl = document.getElementById("status");
const nutritionTip = document.getElementById("nutritionTip");
const tipButton = document.getElementById("tipButton");

let currentGoal = "";

function escapeHtml(value) {
    return value
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function markdownToHtml(markdown) {
    let html = escapeHtml(markdown);

    html = html.replace(/^### (.*)$/gm, "<h3>$1</h3>");
    html = html.replace(/^## (.*)$/gm, "<h2>$1</h2>");
    html = html.replace(/^# (.*)$/gm, "<h1>$1</h1>");
    html = html.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
    html = html.replace(/^\- (.*)$/gm, "<li>$1</li>");
    html = html.replace(/(<li>.*<\/li>\n?)+/g, (match) => `<ul>${match}</ul>`);
    html = html.replace(/\n{2,}/g, "<br><br>");
    html = html.replace(/\n/g, "<br>");

    return html;
}

function showPlan(plan, planId) {
    emptyState.classList.add("hidden");
    planResult.classList.remove("hidden");
    feedbackBox.classList.remove("hidden");
    planResult.innerHTML = markdownToHtml(plan);
    planIdInput.value = planId;
    statusEl.textContent = "Generated";
}

planForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    statusEl.textContent = "Generating...";
    const formData = new FormData(planForm);
    currentGoal = formData.get("goal");

    try {
        const response = await fetch("/generate_plan", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Could not generate the plan.");
        }

        showPlan(data.plan, data.plan_id);
        nutritionTip.textContent = "Click “Get Tip” for a goal-specific nutrition/recovery tip.";
    } catch (error) {
        statusEl.textContent = "Error";
        alert(error.message);
    }
});

feedbackForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const data = new FormData();
    data.append("plan_id", planIdInput.value);
    data.append("feedback_text", feedbackText.value);

    statusEl.textContent = "Revising...";

    try {
        const response = await fetch("/update_plan", {
            method: "POST",
            body: data
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Could not revise the plan.");
        }

        showPlan(result.plan, result.plan_id);
        feedbackText.value = "";
        statusEl.textContent = "Revised";
    } catch (error) {
        statusEl.textContent = "Error";
        alert(error.message);
    }
});

tipButton.addEventListener("click", async () => {
    if (!currentGoal) {
        alert("Generate a plan first.");
        return;
    }

    tipButton.disabled = true;
    tipButton.textContent = "Loading...";

    try {
        const response = await fetch(
            `/nutrition_tip?goal=${encodeURIComponent(currentGoal)}`
        );
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Could not get nutrition tip.");
        }

        nutritionTip.textContent = data.tip;
    } catch (error) {
        nutritionTip.textContent = error.message;
    } finally {
        tipButton.disabled = false;
        tipButton.textContent = "Get Tip";
    }
});
