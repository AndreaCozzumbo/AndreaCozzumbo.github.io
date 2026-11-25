// "BibTeX" buttons on publications: copy the citation to the clipboard.
document.addEventListener("click", async (event) => {
  const button = event.target.closest("[data-bibtex]");
  if (!button) {
    return;
  }
  const label = button.textContent;
  const bibtex = button.dataset.bibtex.replace(/\s*␤\s*/g, "\n  ").replace(/\s*\}\s*$/, "\n}\n");
  try {
    await navigator.clipboard.writeText(bibtex);
    button.textContent = "Copied";
  } catch (error) {
    window.prompt("Copy the BibTeX entry:", bibtex);
    return;
  }
  setTimeout(() => {
    button.textContent = label;
  }, 1500);
});
