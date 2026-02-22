const analyzeBtn = document.getElementById("analyzeBtn");
const resumeInput = document.getElementById("resumeText");
const experienceInput = document.getElementById("experience");
const resultEl = document.getElementById("result");

function setResult(text) {
  resultEl.textContent = text;
}

async function getActiveTabText() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab?.id) {
    throw new Error("No active tab found.");
  }

  const [{ result }] = await chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: () => {
      const main = document.querySelector("main")?.innerText || "";
      const article = document.querySelector("article")?.innerText || "";
      const body = document.body?.innerText || "";
      const merged = [main, article, body].join("\n");
      return merged.slice(0, 15000);
    },
  });

  return result || "";
}

async function runAnalysis() {
  const resumeText = resumeInput.value.trim();
  const experienceText = experienceInput.value.trim();

  if (!resumeText) {
    setResult("Resume text is required.");
    return;
  }

  analyzeBtn.disabled = true;
  setResult("Extracting JD from active tab...");

  try {
    const jdText = await getActiveTabText();
    if (!jdText) {
      throw new Error("Could not extract JD text from this page.");
    }

    setResult("Scoring against local Resumelytics API...");

    const payload = {
      resume_text: resumeText,
      jd_text: jdText,
      candidate_experience: experienceText ? Number(experienceText) : null,
    };

    const response = await fetch("http://127.0.0.1:8787/score", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Scoring failed.");
    }

    setResult(JSON.stringify(data, null, 2));
    chrome.storage.local.set({ lastResult: data, lastResumeText: resumeText });
  } catch (error) {
    setResult(`Error: ${error.message}`);
  } finally {
    analyzeBtn.disabled = false;
  }
}

analyzeBtn.addEventListener("click", runAnalysis);

chrome.storage.local.get(["lastResumeText", "lastResult"], (stored) => {
  if (stored.lastResumeText) {
    resumeInput.value = stored.lastResumeText;
  }

  if (stored.lastResult) {
    setResult(JSON.stringify(stored.lastResult, null, 2));
  }
});
