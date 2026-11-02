// Theme & Interactive Sub-Tab / Search Controller for whatember
(function () {
  const root = document.documentElement;
  const savedTheme = localStorage.getItem("whatember-theme");
  if (savedTheme === "dark" || savedTheme === "light") {
    root.setAttribute("data-theme", savedTheme);
  } else if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
    root.setAttribute("data-theme", "dark");
  }

  document.addEventListener("DOMContentLoaded", () => {
    // 1. Theme toggle button
    const themeBtn = document.getElementById("theme-toggle");
    if (themeBtn) {
      const updateLabel = () => {
        const isDark = root.getAttribute("data-theme") === "dark";
        themeBtn.textContent = isDark ? "☀" : "◐";
        themeBtn.setAttribute("aria-label", isDark ? "Switch to light theme" : "Switch to dark theme");
      };
      updateLabel();
      themeBtn.addEventListener("click", () => {
        const next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
        root.setAttribute("data-theme", next);
        localStorage.setItem("whatember-theme", next);
        updateLabel();
      });
    }

    // 2. Interactive sub-tabs within each page
    const subtabButtons = document.querySelectorAll(".subtab-btn[data-tab-target]");
    const tabPanels = document.querySelectorAll(".tab-panel[id]");

    function activateTab(targetId, pushHash = false) {
      let found = false;
      tabPanels.forEach((panel) => {
        if (panel.id === targetId) {
          panel.classList.add("active");
          found = true;
        } else {
          panel.classList.remove("active");
        }
      });
      if (!found) return;
      subtabButtons.forEach((btn) => {
        const isMatch = btn.getAttribute("data-tab-target") === targetId;
        btn.setAttribute("aria-selected", isMatch ? "true" : "false");
      });
      if (pushHash) {
        history.replaceState(null, "", "#" + targetId);
      }
    }

    subtabButtons.forEach((btn) => {
      btn.addEventListener("click", () => {
        const target = btn.getAttribute("data-tab-target");
        activateTab(target, true);
      });
    });

    // Activate tab from URL hash if present
    if (window.location.hash) {
      const hashId = window.location.hash.slice(1);
      const directPanel = document.getElementById(hashId);
      if (directPanel && directPanel.classList.contains("tab-panel")) {
        activateTab(hashId, false);
      } else if (directPanel) {
        const parentPanel = directPanel.closest(".tab-panel");
        if (parentPanel && parentPanel.id) {
          activateTab(parentPanel.id, false);
          setTimeout(() => directPanel.scrollIntoView({ behavior: "smooth" }), 50);
        }
      }
    }

    // 3. Filterable tables & cards
    document.querySelectorAll("[data-filter-container]").forEach((container) => {
      const input = container.querySelector("[data-filter-input]");
      const select = container.querySelector("[data-filter-select]");
      const countEl = container.querySelector("[data-filter-count]");
      const items = container.querySelectorAll("[data-filter-item]");

      function applyFilter() {
        const q = (input ? input.value : "").trim().toLowerCase();
        const cat = select ? select.value : "all";
        let visible = 0;
        items.forEach((item) => {
          const text = item.textContent.toLowerCase();
          const itemCat = item.getAttribute("data-category") || "";
          const matchesQuery = !q || text.includes(q);
          const matchesCat = cat === "all" || itemCat.split(/\s+/).includes(cat);
          if (matchesQuery && matchesCat) {
            item.style.display = "";
            visible++;
          } else {
            item.style.display = "none";
          }
        });
        if (countEl) {
          countEl.textContent = `${visible} of ${items.length} shown`;
        }
      }

      if (input) input.addEventListener("input", applyFilter);
      if (select) select.addEventListener("change", applyFilter);
      applyFilter();
    });

    // 4. Built-in Dossier Reader Modal for sources/*.md links
    const mdLinks = document.querySelectorAll('a[href^="sources/"][href$=".md"]');
    if (mdLinks.length > 0) {
      const modal = document.createElement("div");
      modal.className = "dossier-modal";
      modal.setAttribute("role", "dialog");
      modal.setAttribute("aria-modal", "true");
      modal.innerHTML = `
        <div class="dossier-dialog">
          <div class="dossier-header">
            <span class="dossier-title" id="dossier-modal-title">Primary-Source Dossier</span>
            <div class="dossier-actions">
              <a class="btn btn-ghost" id="dossier-github-link" target="_blank" rel="noopener">View on GitHub ↗</a>
              <a class="btn btn-ghost" id="dossier-raw-link" target="_blank" rel="noopener">Raw .md ↗</a>
              <button class="btn btn-primary" id="dossier-close-btn" type="button">Close ✕</button>
            </div>
          </div>
          <div class="dossier-body" id="dossier-modal-body">Loading primary-source dossier...</div>
        </div>
      `;
      document.body.appendChild(modal);

      const titleEl = document.getElementById("dossier-modal-title");
      const bodyEl = document.getElementById("dossier-modal-body");
      const rawLink = document.getElementById("dossier-raw-link");
      const ghLink = document.getElementById("dossier-github-link");
      const closeBtn = document.getElementById("dossier-close-btn");

      const closeModal = () => modal.classList.remove("open");
      closeBtn.addEventListener("click", closeModal);
      modal.addEventListener("click", (e) => {
        if (e.target === modal) closeModal();
      });
      document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") closeModal();
      });

      mdLinks.forEach((link) => {
        link.addEventListener("click", async (e) => {
          if (e.metaKey || e.ctrlKey || e.shiftKey) return;
          e.preventDefault();
          const href = link.getAttribute("href");
          titleEl.textContent = href;
          rawLink.href = href;
          ghLink.href = "https://github.com/emberian/whatember/blob/main/" + href;
          bodyEl.textContent = "Loading " + href + " ...";
          modal.classList.add("open");
          try {
            const res = await fetch(href);
            if (!res.ok) throw new Error("HTTP " + res.status);
            bodyEl.textContent = await res.text();
          } catch (err) {
            window.location.href = href;
          }
        });
      });
    }
  });
})();
